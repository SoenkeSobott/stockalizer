import json
from csv import writer
from urllib.request import urlopen
from datetime import datetime

"""
This scraper scrapes the reuters api for historical news for a specified company
"""

def stream_news():
    # 1543224497000000000 26/11/2018
    # 1605105256

    time_interval = 1607515708000000000  # 09/12/2020 as an integer value
    while time_interval > 1603515708000000000:
        company = 'AMZN'
        response = urlopen(
            'https://wireapi.reuters.com/v8/feed/rcom/us/marketnews/ric:{0}.OQ?until={1}'.format(company, str(
                time_interval))).read().decode('utf-8')
        response_json = json.loads(response)
        item_count = len(response_json['wireitems']) - 1
        count = 0
        for item in response_json['wireitems']:
            if item['wireitem_type'] != 'story':
                print('ad found')
                count = count + 1
                continue

            template_data = item['templates'][0]['story']
            date_string = template_data['updated_at'][:10]
            date = datetime.strftime(datetime.strptime(date_string, '%Y-%m-%d'), '%b-%d-%m')
            data = [
                template_data['hed'],
                date
            ]
            with open('news.csv', 'a') as file:
                csv_writer = writer(file)
                csv_writer.writerow(data)

            if count == item_count:
                time_interval = int(item['wireitem_id']) - 1
                break
            count = count + 1


if __name__ == "__main__":
    stream_news()
