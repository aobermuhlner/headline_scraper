import urllib.request
from bs4 import BeautifulSoup


class NewsScraper:

    def __init__(self, url, html_tags):
        self.url = url
        self.html_tags = html_tags
        self.headline_list = []
    def scraper(self):
        data = urllib.request.urlopen(self.url).read()
        soup = BeautifulSoup(data, "html.parser")
        headlines = soup.find_all(self.html_tags)

        for i in headlines:
            self.headline_list.append(i.text.strip())

        return self.headline_list


if __name__ == "__main__":

    headlines = NewsScraper('https://www.nytimes.com', ['h3']).scraper()

    for i in headlines:
        print(i)
