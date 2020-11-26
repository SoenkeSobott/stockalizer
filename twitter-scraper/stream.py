import tweepy

from textblob import TextBlob
from datetime import datetime

from ssh.keys import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import json
from pprint import pprint
from pip._vendor import requests


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
        put_data = {
            "tweetId": data['id'],
            "owner": data['user']['screen_name'],
            "text": tweet,
            "prediction": 0.12}  # TODO: predict value from model
        print(put_data)
        response = requests.put(
            'https://stockalizer.azurewebsites.net/api/tweets?code=lZjlUl6QSaCXDJJANyhM8xAMtQUk6i1B90qzliaxKmNdLywWxfzUWw==', data=json.dumps(put_data))
        print(response)

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
