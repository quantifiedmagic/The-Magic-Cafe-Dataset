# The Magic Café Dataset

This repository contains the web scraping software, data cleaning code, and a Jupyter Notebook file exploring basic charactistics of the dataset. See the Quantified Magic Blog Post "[The Magic Café Dataset](https://quantifiedmagic.com/datasets/2021/06/24/the-magic-cafe.html)" for high-level details.

If you are just interested in the Dataset, downlad it via the link below:

https://drive.google.com/file/d/1H1fNp01wsk8rL16BReMHX6xcr38UeE5Z/view?usp=sharing

# Usage

The web scraping code is built using Scrapy and contains two scrapers: forum and guest. The forum scraper pulls all publically available threads/posts. The code does not scrape subforums that require special access (e.g., Secret sessions). The guest scraper scrapes the special guest of honor pages.

```
scrapy crawl forum -O themagiccafe.jsonlines
```

```
scrapy crawl guest -O guests.jsonlines
```

The scraping procedure will result in two jsonlines files: themagiccafe.jsonlines and guests.jsonlines. The basic json structure is listed below:

```json
{
    "posts":
        [{"username": "Tony", "date": "Posted: Dec 1, 2011 11:11 pm", "post": "Post 1 Text Here"},
         {"username": "Tony", "date": "Posted: Dec 1, 2011 11:12 pm", "post": "Post 2 Text Here"},
         {"username": "Tony", "date": "Posted: Dec 1, 2011 11:13 pm", "post": "Post 3 Text Here"},
         ...
         {"username": "Tony", "date": "Posted: Dec 1, 2011 11:14 pm", "post": "Post N Text Here"}],
    "link": "https://www.themagiccafe.com/forums/viewtopic.php?topic=534879&forum=41&start=0",
    "page": "1",
    "title": ["The Magic Cafe Forum Index", "New to magic?", "What should every magician own?"]
}
```

The key "page" is optional, and only appears when a thread contains more than one page.

Next, combine both files with the following command:

```
cat guests.jsonlines >> themagiccafe_all.jsonlines
```

There is one issue with the scraped data. If a thread has multiple pages, it will be split into seperate json objects. This makes analyzing thread-specific structures difficult. Thus, to join all pages into a single json object run the following code:

```
    python clean.py themagiccafe_all.jsonlines > themagiccafe_all_clean.jsonlines
```

See the basic-statistics.ipynb file to see the code used to generate the basic information on the blog.

# More Information
Created by Tony (quantifiedmagic.com)

Contact: quantfiedmagic@gmail.com
