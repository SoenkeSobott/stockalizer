from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

finviz_url = 'https://finviz.com/quote.ashx?t='
# TODO: make time range configurable
# TODO: find way to run in background and track buy/sell decisions (maybe in DB)


def get_news_table_for_ticker(ticker):
    url = finviz_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = BeautifulSoup(response, features="html.parser")

    return html.find(id='news-table')


def parse_data(data, ticker):
    parsed_data = []
    for row in data.find_all('tr'):
        title = row.a.get_text()
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])

    return parsed_data


def predict_for_ticker(ticker):
    amzn_data = get_news_table_for_ticker(ticker)
    parsed_amzn_data = parse_data(amzn_data, ticker)

    df = pd.DataFrame(parsed_amzn_data, columns=['ticker', 'date', 'time', 'title'])

    vader = SentimentIntensityAnalyzer()

    df['compound'] = df['title'].apply(lambda title: vader.polarity_scores(title)['compound'])
    df['date'] = pd.to_datetime(df.date).dt.date

    days = len(df.groupby(['date']))

    mean_sentiment = df.mean()['compound']
    print("Mean sentiment in past " + str(days) + " days was: " + str(mean_sentiment))

    if mean_sentiment > 0.05:
        print(ticker + " has a positive sentiment - Bot says: BUY")
    elif mean_sentiment < -0.05:
        print(ticker + " has a negative sentiment - Bot says: DON'T BUY")
    else:
        print(ticker + " has a neutral sentiment - Bot says: WAIT")


predict_for_ticker('AMZN')