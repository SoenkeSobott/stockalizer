from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pandas as pd

sia = SIA()

# Get csv file and load into pandas data frame
df = pd.read_csv('../../data/files/news.csv', header=None)
df.columns = ['date', 'title']

sentiment_function_vader = lambda title: (sia.polarity_scores(title)['compound'])

df['compound'] = df['title'].apply(sentiment_function_vader)

df['sentiment_score'] = 0.5
df.loc[df['compound'] > 0.2, 'sentiment_score'] = 1
df.loc[df['compound'] < -0.2, 'sentiment_score'] = 0

# Remove unnecessary columns
del df['title']

df.to_csv('../../data/files/news_with_scores_vader.csv', index=False)
