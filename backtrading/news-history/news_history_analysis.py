import pandas as pd
import tensorflow as tf
from util import word_index


# Script that uses history news data from an csv file in the format [date, title] to
# calculate an sentiment score for each title. The sentiment score is then appended
# to the file.
# Output of this script is a file with the format [date, title, sentiment_score]


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


# Get csv file and load into pandas data frame
df = pd.read_csv('../../data/files/news.csv', header=None)
df.columns = ['date', 'title']

# Load model
model = tf.keras.models.load_model('../../data/models/text_classification.h5')

# Encode title for each row in file
df['encoded_title'] = df['title'].apply(lambda title: prepare_news_title(title))

# Add sentiment score to each row in file
df['sentiment_score'] = df['encoded_title'].apply(lambda encoded_title: (model.predict(encoded_title)[0])[0])

# Remove unnecessary column
del df['encoded_title']
del df['title']

# Save to csv file
df.to_csv('../../data/files/news_with_scores.csv', index=False)
