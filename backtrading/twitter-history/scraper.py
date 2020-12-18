import json
import urllib
from csv import writer
from urllib.request import urlopen, Request
from datetime import datetime

"""
This scraper scrapes the stocktwits api for historical tweets for a specified company
"""


def scrape_tweets():
    time_interval = 263781899
    date = datetime(2020, 12, 1)
    while date > datetime(2017, 12, 1):
        company = 'TSLA'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        values = {'name': 'Michael Foord',
                  'location': 'Northampton',
                  'language': 'Python'}
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
            if item['user']['like_count'] > 1000:
                data = [
                    date_string,
                    item['body']
                ]
                with open('../../data/files/twitter-news.csv', 'a', newline='', encoding='utf-8') as file:
                    csv_writer = writer(file)
                    csv_writer.writerow(data)
                    print('row added')


if __name__ == "__main__":
    scrape_tweets()
