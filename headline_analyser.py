import spacy
from collections import Counter
nlp_de = spacy.load('de_core_news_sm')
nlp_en = spacy.load('en_core_web_sm')
import scraper

class HeadlineAnalyser:
    def __init__(self, headlines):
        self.headlines = headlines

    def find_most_common_nouns(self, n=10):
        nouns = Counter()
        for text in self.headlines:
            doc = nlp_en(text)
            nouns.update([token.text.lower() for token in doc if token.pos_ == 'NOUN'])
        return nouns.most_common(n)

if __name__ == "__main__":
    test_headlines = scraper.NewsScraper('https://www.bbc.com', ['h3']).scraper()
    test_headlines += scraper.NewsScraper('https://www.nytimes.com', ['h3']).scraper()
    test_headlines += scraper.NewsScraper('https://www.latimes.com',  ['h2', 'h3']).scraper()

    analyser = HeadlineAnalyser(test_headlines)
    print(analyser.find_most_common_nouns())
