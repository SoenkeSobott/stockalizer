import json
from csv import writer
from urllib.request import urlopen
from datetime import datetime

"""
This scraper scrapes the reuters api for historical news for a specified company
"""


def stream_news():
    # 1606780800000000000 01/12/2020
    # 1512086400000000000 01/12/2017

    exception_counter = 0
    time_interval = 1606780800000000000
    while time_interval > 1512086400000000000:
        company = 'AMZN'
        try:
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
                date_string = template_data['updated_at'][0:19]
                date = datetime.strftime(datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                data = [
                    date,
                    template_data['hed']
                ]
                with open('news.csv', 'a', newline='') as file:
                    csv_writer = writer(file)
                    csv_writer.writerow(data)

                if count == item_count:
                    time_interval = int(item['wireitem_id']) - 1
                    break
                count = count + 1
        except Exception as e:
            exception_counter = exception_counter + 1
            if exception_counter == 1:
                time_interval = 1514764800000000000  # to reach 06th december because of weird emoji encoding
            elif exception_counter == 2:
                time_interval = 1512432000000000000
            else:
                break
            print(e)


if __name__ == "__main__":
    stream_news()
