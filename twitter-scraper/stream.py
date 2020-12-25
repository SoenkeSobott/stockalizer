import re
import tweepy
from ssh.keys import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import json
from pprint import pprint
from pip._vendor import requests


def clean_tweet(text):
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', '')
    text = text.replace('\xa0', '')
    text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
    text = re.sub('#', '', text)  # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text)  # Removing RT
    text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink
    return text


def process_data(data):
    pprint(data)
    tweet = clean_tweet(data['text'])
    put_data = {
        "tweetId": data['id'],
        "text": tweet,
        "date": data['created_at']}
    print(put_data)
    response = requests.put(
        'https://stockalizer.azurewebsites.net/api/tweets?code'
        '=lZjlUl6QSaCXDJJANyhM8xAMtQUk6i1B90qzliaxKmNdLywWxfzUWw==',
        data=json.dumps(put_data))
    print(response)  # TODO: remove the API key from here


class StreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        if 'delete' in data:
            print('deleted tweet')
        else:
            process_data(data)

    def on_error(self, status_code):
        if status_code == 420:
            return False


class Stream:
    def __init__(self, auth_token, stream_listener):
        self.stream = tweepy.Stream(auth=auth_token, listener=stream_listener)

    def start(self):
        # das ist meine id
        self.stream.filter(track=["$ORCL"], is_async=True)


if __name__ == "__main__":
    listener = StreamListener()

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    try:
        stream.start()
    except Exception as e:
        print(e)
