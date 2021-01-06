import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


"""
Script that uses history twitter data from an csv file in the format [date, title] to
calculate an sentiment score for each title. The sentiment score is then appended
to the file.

Output of this script is a file with the format [date, compound]
"""


def vader_compound_mapping(compound):
    """
    This maps a vader compound value to our sentiment score format (0-1)

    :return:
        the mapped sentiment score
    """
    if compound < -0.15:
        return 0
    elif compound > 0.15:
        return 1
    else:
        return 0.5


def calculate_sentiment_scores(source_csv, target_csv):
    print('Calculating scores ...')

    # Get csv file and load into pandas data frame
    df = pd.read_csv(source_csv, header=None)
    df.columns = ['date', 'title']

    # Get vader model
    sia = SIA()

    # Add compound to each entry
    sentiment_function_vader = lambda title: (sia.polarity_scores(title)['compound'])
    df['compound'] = df['title'].apply(sentiment_function_vader)

    # Remove unnecessary columns
    del df['title']

    # Calculate mean sentiment_scores for one hour intervals, if no sentiment_score for an hour is available, add time
    # and set default sentiment_score 0.5 (= neutral).
    df['date'] = df['date'].apply(lambda date: pd.to_datetime(date, format='%d/%m/%Y %H:%M'))
    df = df.set_index('date').groupby(pd.Grouper(freq='H')).mean()
    df.dropna(subset=['compound'], inplace=True)

    # Map compound to sentiment score
    map_compound = lambda compound: (vader_compound_mapping(compound))
    df['compound'] = df['compound'].apply(map_compound)

    # Change date back to old format
    df.index = df.index.strftime('%d/%m/%Y %H:%M')

    # Save to csv file
    df.to_csv(target_csv, index=True)
    print('Successfully calculated sentiment scores and stored to: ' + str(target_csv))


def calculate_sentiment_score_for(ticker):
    calculate_sentiment_scores('../../data/files/' + str(ticker) + '/' + str(ticker).lower() + '_tweets.csv',
                               '../../data/files/' + str(ticker) + '/' + str(ticker).lower() + '_tweets_with_scores.csv')


if __name__ == "__main__":
    calculate_sentiment_score_for('NFLX')
    calculate_sentiment_score_for('ORCL')
    calculate_sentiment_score_for('TSLA')




