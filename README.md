# stub-hub-event-crawler

This project is a Python-based web scraper using Scrapy to collect event data from the StubHub website. It stores each event in MongoDB and saves raw response data in JSON files.

---

## What This Code Does

### 1. MongoDB Connection

```python
mongo_connection = pymongo.MongoClient('mongodb://localhost:27017/')
db_name = mongo_connection['stubhub_db']
output_table = db_name['stubhub_events']
```

- Connects to MongoDB on your local machine.
- Prepares a database named `stubhub_db` and a collection `stubhub_events`.

---

### 2. Starts Scrapy Spider

```python
class StubHubSpider(scrapy.Spider):
    name = 'stubhub'
```

- A spider named `stubhub` is created which Scrapy uses to start scraping.

---

### 3. Sends Initial Request

```python
def start_requests(self):
    url = 'https://www.stubhub.com/explore?...'
    yield scrapy.Request(url=url, callback=self.parse)
```

- Hits the StubHub API and sends the response to the `parse()` function.

---

### 4. Parses the Response

```python
selector = response.json()
events = selector['events']
page = selector['page']
```

- Converts the response to JSON and extracts the event list and page number.

---

### 5. Saves JSON Page

```python
file_path = f"D:\pagesave\stubhub\event_{page + 1}.json"
```

- Saves the entire response JSON into a local directory for reference or backup.

---

### 6. Extracts and Saves Event Data

```python
item = {'title': ..., 'datetime': ..., 'location': ..., 'image': ...}
```

- For each event, collects title, datetime, location, and image URL.
- Saves 5 events at a time to MongoDB.

---

### 7. Pagination Handling

- Checks if more pages exist.
- If yes, either reads from saved file or requests the next page from the API.

---

### 8. Run the Spider

```python
if __name__ == '__main__':
    execute('scrapy crawl stubhub'.split())
```

- Runs the spider when the script is executed directly.

---

## How to Run

1. Make sure MongoDB is running locally.
2. Install requirements:
```bash
pip install scrapy pymongo
```
3. Run the spider:
```bash
python stubhub_spider.py
```

---

## Folder Structure

```
project_folder/
├── stubhub_spider.py
├── pagesave/
│   └── stubhub/
│       └── event_page_1.json
│       └── event_page_2.json
```

---

## Sample Output Format

```json
{
  "events": [
    {
      "title": "Concert A",
      "datetime": "June 10 Sunday 7 PM",
      "location": "New York, NY",
      "image": "http://..."
    }
  ]
}
```
