import tweepy
from ssh.keys import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import json
from pprint import pprint
from pip._vendor import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_sentiment_score(sentence):
    analyzer = SentimentIntensityAnalyzer()

    sentiment = analyzer.polarity_scores(sentence)
    print("Overall sentiment dictionary is : ", sentiment)
    print("sentence was rated as ", sentiment['neg'] * 100, "% Negative")
    print("sentence was rated as ", sentiment['neu'] * 100, "% Neutral")
    print("sentence was rated as ", sentiment['pos'] * 100, "% Positive")
    return sentiment['compound']


class StreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        if 'delete' in data:
            print('deleted tweet')
        else:
            self.process_data(data)

    def process_data(self, data):
        pprint(data)
        tweet = data['text']
        sentiment_score = get_sentiment_score(tweet)
        put_data = {
            "tweetId": data['id'],
            "owner": data['user']['screen_name'],
            "text": tweet,
            "prediction": sentiment_score}
        print(put_data)
        response = requests.put(
            'https://stockalizer.azurewebsites.net/api/tweets?code=lZjlUl6QSaCXDJJANyhM8xAMtQUk6i1B90qzliaxKmNdLywWxfzUWw==',
            data=json.dumps(put_data))
        print(response)  # TODO: remove the API key from here

    def on_error(self, status_code):
        if status_code == 420:
            return False


class Stream():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self):
        # das ist meine id
        self.stream.filter(follow=["2418840943"], is_async=True)


if __name__ == "__main__":
    listener = StreamListener()

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    try:
        stream.start()
    except Exception as e:
        print(e)
