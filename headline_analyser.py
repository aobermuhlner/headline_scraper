import spacy
import scraper
import difflib
from collections import Counter
nlp_de = spacy.load('de_core_news_sm')
nlp_en = spacy.load('en_core_web_sm')


class HeadlineAnalyser:
    def __init__(self, headlines):
        self.headlines = headlines
        self.topics = ["Politics", "Economy", "Sports", "Culture", "Science", "Technology", "Education", "Environment"]

    def find_most_common_nouns(self, n=10):
        nouns = Counter()
        for text in self.headlines:
            doc = nlp_en(text)
            nouns.update([token.text.lower() for token in doc if token.pos_ == 'NOUN'])
        return nouns.most_common(n)

    def categorize_headlines(self):
        categorized_headlines = {topic: [] for topic in self.topics}

        for headline in self.headlines:
            similarities = [difflib.SequenceMatcher(None, headline.lower(), topic.lower()).ratio() for topic in self.topics]
            best_match_topic = self.topics[similarities.index(max(similarities))]
            categorized_headlines[best_match_topic].append(headline)

        return categorized_headlines


if __name__ == "__main__":
    test_headlines = scraper.NewsScraper('https://www.bbc.com', ['h3']).scraper()
    test_headlines += scraper.NewsScraper('https://www.nytimes.com', ['h3']).scraper()
    test_headlines += scraper.NewsScraper('https://www.latimes.com',  ['h2', 'h3']).scraper()

    analyser = HeadlineAnalyser(test_headlines)
    #print(analyser.find_most_common_nouns())

    test_data = analyser.categorize_headlines()

    for i in test_data['Politics']:
        print(i)