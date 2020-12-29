import pandas as pd
import tensorflow as tf
from util import word_index


"""
Script that uses history news data from an csv file in the format [date, title] to
calculate an sentiment score for each title. The sentiment score is then appended
to the file.

Output of this script is a file with the format [date, title, sentiment_score]
"""


def encode_title(title):
    """
    Encodes the passed array. This means that the words from the array are mapped
    to their referenced values in the word_index dictionary.
    Example: in: ["this", "is", "a", "test"]   out: [3244, 345, 4, 23444]

    Args:
        title: The array with all the words that need to be encoded.

    Returns:
        The encoded array.
    """
    encoded = [1]
    for word in title:
        if word.lower() in word_index:
            encoded.append(word_index[word.lower()])
        else:
            encoded.append(2)
    return encoded


def prepare_news_title(title):
    """
    Prepares the passed text. That means removing unnecessary chars and then transforming it to an array and
    encoding the array. Also the maximum length is set and all empty spaces to this maximum are filled with the
    placeholder value <PAD>.

    Args:
        title: The text that needs preparation.

    Returns:
        The encoded array.
    """
    title = title.replace(".", "").replace(",", "").replace(":", "").split()  # remove more values !?*"" ...
    encoded_title = encode_title(title)
    encoded_title = tf.keras.preprocessing.sequence.pad_sequences([encoded_title], value=word_index["<PAD>"],
                                                                  padding="post",
                                                                  maxlen=100)
    return encoded_title


def calculate_sentiment_scores(source_csv, target_csv):
    print('Calculating scores ...')
    # Get csv file and load into pandas data frame
    df = pd.read_csv(source_csv, header=None)
    df.columns = ['date', 'title']

    # Load model
    model = tf.keras.models.load_model('../../data/models/text_classification.h5')

    # Encode title for each row
    df['encoded_title'] = df['title'].apply(lambda title: prepare_news_title(title))

    # Add sentiment score to each row
    sentiment_function = lambda encoded_title: (model.predict(encoded_title)[0])[0]
    df['sentiment_score'] = df['encoded_title'].apply(sentiment_function)

    # Remove unnecessary columns
    del df['encoded_title']
    del df['title']

    # Calculate mean sentiment_scores for one hour intervals, if no sentiment_score for an hour is available, add time
    # and set default sentiment_score 0.5 (= neutral).
    df['date'] = df['date'].apply(lambda date: pd.to_datetime(date, format='%d/%m/%Y %H:%M'))
    df = df.set_index('date').groupby(pd.Grouper(freq='H'), dropna=False).mean()
    df['sentiment_score'].fillna(0.5, inplace=True)

    # Change date back to old format
    df.index = df.index.strftime('%d/%m/%Y %H:%M')

    # Save to csv file
    df.to_csv(target_csv, index=True)
    print('Successfully calculated sentiment scores and stored to: ' + str(target_csv))


def calculate_sentiment_score_for(ticker):
    calculate_sentiment_scores('../../data/files/' + str(ticker) + '/' + str(ticker).lower() + '_news.csv',
                               '../../data/files/' + str(ticker) + '/' + str(ticker).lower() + '_news_with_scores.csv')


if __name__ == "__main__":
    calculate_sentiment_score_for('AMZN')
    #calculate_sentiment_score_for('NFLX')
    #calculate_sentiment_score_for('ORCL')
    #calculate_sentiment_score_for('TSLA')




