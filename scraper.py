import urllib.request
from bs4 import BeautifulSoup

# pip install bs4


class NewsScraper:

    def __init__(self, url: str, html_tags: list):
        self.url = url
        self.html_tags = html_tags
        self.headline_list = []

    def scraper(self):
        data = urllib.request.urlopen(self.url).read()
        soup = BeautifulSoup(data, "html.parser")
        headlines = soup.find_all(self.html_tags)

        for i in headlines:
            headline_text = i.text.strip()
            if len(headline_text.split()) > 1:
                self.headline_list.append(headline_text)

        return self.headline_list


if __name__ == "__main__":

    headlines = NewsScraper('https://www.bbc.com', ['h3']).scraper()
    for i in headlines:
        print(i)
