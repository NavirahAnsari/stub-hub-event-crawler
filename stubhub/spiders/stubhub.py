
import os

import pymongo
import scrapy
from scrapy.cmdline import execute

# MongoDB connection details
mongo_connection = pymongo.MongoClient('mongodb://localhost:27017/')
db_name = mongo_connection['stubhub_db']
output_table = db_name['stubhub_events']


class StubhubSpider(scrapy.Spider):
    name = 'stubhub'  # Name of the spider

    def start_requests(self):
        url = 'https://www.stubhub.com/explore?method=getExploreEvents&lat=NDAuNzEyOA%3D%3D&lon=LTc0LjAwNg%3D%3D&to=253402300799999&tlcId=2'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Convert the response to JSON
        selector = response.json()
        events = selector['events']
        page = selector['page']

        # File path to save the JSON response
        file_path = f"D:\\pagesave\\stubhub\\event_page_{page + 1}.json"
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(response.text)
        except Exception as e:
            file_path = ''
            print("Error in pagesave", e)

        # Loop through all events and extract fields
        for event in events:
            try:
                title = event['name']
            except:
                title = ''

            try:
                datewithoutyear = event['formattedDateWithoutYear']
            except:
                datewithoutyear = ''

            try:
                day_of_week = event['dayOfWeek']
            except:
                day_of_week = ''

            try:
                formatted_time = event['formattedTime']
            except:
                formatted_time = ''

            date_str = f"{datewithoutyear} {day_of_week} {formatted_time}".strip()
            try:
                image = event['imageUrl']
            except:
                image = ''

            try:
                venue = event['formattedVenueLocation']
            except:
                venue = ''

            # Item for MongoDB insertion
            item = {'title': title, 'datetime': date_str, 'location': venue, 'image': image, 'html_page': file_path}

            # Check if there are more pages to crawl
            try:
                output_table.insert_one(item)
                print('data inserted.....')
            except Exception as e:
                print(e)

        remaining = selector['remaining']
        page = selector['page']
        if remaining == 1:
            page += 1
            next_page_url = f'https://www.stubhub.com/explore?method=getExploreEvents&lat=NDAuNzEyOA%3D%3D&lon=LTc0LjAwNg%3D%3D&to=253402300799999&page={page}&tlcId=2'
            print('page_url', next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)


if __name__ == '__main__':
    execute('scrapy crawl stubhub'.split())
