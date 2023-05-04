__author__ = "Adrian Obermühlner", "Linus Stuhlmann"

import urllib.request
from bs4 import BeautifulSoup
import json
import datetime as dt
import re


class NewsScraper:

    # Linus Stuhlmann
    def __init__(self, html_tags: list):
        self.url = []
        self.html_tags = html_tags
        self.headline_list = []

    def add_url(self, url: str):
        self.url.append(url)
        self.clear_cache()


    def scraper(self):

        with open('cache.json', "r") as file:
            cache_data = json.load(file)

        if (dt.datetime.today() - dt.datetime.strptime(cache_data['date'],
                                                       "%Y-%m-%d %H:%M:%S")) > dt.timedelta(minutes=10):
            for i in self.url:
                data = urllib.request.urlopen(i).read()
                soup = BeautifulSoup(data, "html.parser")
                headlines = soup.find_all(self.html_tags)

                for i in headlines:
                    headline_text = i.text.strip()
                    if len(headline_text.split()) > 1:
                        self.headline_list.append(re.sub(r'[-_<>›]', '', headline_text))
            self.cache(self.headline_list)
            print('--> Daten aus Internet bezogen')
        else:
            print('--> Daten aus Cache bezogen')
            self.headline_list = cache_data['headlines']

        return self.headline_list

    @staticmethod
    def cache(headlines):
        cache_data = {
            'date': dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
            'headlines': headlines
        }
        with open('cache.json', "w") as file:
            json.dump(cache_data, file)
        return True

    # Linus Stuhlmann
    @staticmethod
    def clear_cache():
        with open('cache.json', "w") as file:
            cache_data = {'date': dt.datetime(year=1, month=1, day=1).strftime("%Y-%m-%d %H:%M:%S"),
                          'headlines': []}
            json.dump(cache_data, file)
        return True

if __name__ == "__main__":

    test_scraper = NewsScraper(['h2'])
    test_scraper.clear_cache()
    test_scraper.add_url('https://www.nzz.ch')
    headlines = test_scraper.scraper()

    for i in headlines:
        print(i)

    print(len(headlines))
