import urllib.request
from bs4 import BeautifulSoup
import json
import datetime as dt
import re

# pip install bs4


class NewsScraper:

    def __init__(self, html_tags: list):
        self.url = ['https://www.bbc.com', 'https://www.nytimes.com', 'https://www.latimes.com']
        self.html_tags = html_tags
        self.headline_list = []

    def add_url(self, url: str):
        self.url.append(url)
        self.clean_cache()

    def scraper(self):

        with open('cache.json', "r") as file:
            cache_data = json.load(file)

        if (dt.datetime.today().date() - dt.datetime.strptime(cache_data['date'], "%Y-%m-%d").date()) > dt.timedelta(days=0):
            for i in self.url:
                data = urllib.request.urlopen(i).read()
                soup = BeautifulSoup(data, "html.parser")
                headlines = soup.find_all(self.html_tags)

                for i in headlines:
                    headline_text = i.text.strip()
                    if len(headline_text.split()) > 1:
                        self.headline_list.append(re.sub(r'[-_<>›]', '', headline_text))
            self.cache(self.headline_list)
        else:
            self.headline_list = cache_data['headlines']

        return self.headline_list

    def cache(self, headlines):
        cache_data = {
            'date': dt.datetime.today().strftime('%Y-%m-%d'),
            'headlines': headlines
        }
        with open('cache.json', "w") as file:
            json.dump(cache_data, file)
        return True

    @staticmethod
    def clean_cache():
        with open('cache.json', "w") as file:
            cache_data = {'date': dt.date(year=1, month=1, day=1).strftime('%Y-%m-%d'),
                          'headlines': []}
            json.dump(cache_data, file)
        return True

if __name__ == "__main__":

    test_scraper = NewsScraper(['h3'])
    test_scraper.add_url('https://www.washingtonpost.com')
    headlines = test_scraper.scraper()

    for i in headlines:
        print(i)

