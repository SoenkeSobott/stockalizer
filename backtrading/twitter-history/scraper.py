import json
import re
import urllib
from csv import writer
from urllib.request import urlopen, Request
from datetime import datetime

"""
This scraper scrapes the stocktwits api for historical tweets for a specified company
"""


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


def scrape_tweets():
    time_interval = 263781899
    date = datetime(2020, 12, 1)

    while date > datetime(2019, 12, 1):
        company = 'NFLX'
        file_name = 'nflx'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        values = {'name': 'Michael Foord',
                  'location': 'Northampton',
                  'language': 'english'}

        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')
        url = 'https://api.stocktwits.com/api/2/streams/symbol/{0}.json?filter=top&limit=30&max={1}'.format(company,
                                                                                                            str(
                                                                                                                time_interval))
        req = Request(url=url, headers=headers, data=data)
        response = urlopen(req).read().decode('utf-8')
        response_json = json.loads(response)
        time_interval = response_json['cursor']['max'] - 10
        print('test')
        for item in response_json['messages']:
            date = datetime.strptime(item['created_at'], '%Y-%m-%dT%H:%M:%SZ')
            date_string = datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
            if item['user']['like_count'] < 200:
                # Clean tweet
                tweet = clean_tweet(item['body'])
                data = [
                    date_string,
                    tweet
                ]
                with open('../../data/files/{0}_tweets.csv'.format(file_name), 'a', newline='', encoding='utf-8') as file:
                    csv_writer = writer(file)
                    csv_writer.writerow(data)
                    print('row added')


if __name__ == "__main__":
    scrape_tweets()
