import spacy
import scraper
import difflib
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# pip install spacy
# python -m spacy download de_core_news_sm
# python -m spacy download en_core_web_sm

nlp_de = spacy.load('de_core_news_sm')
nlp_en = spacy.load('en_core_web_sm')


class HeadlineAnalyser:
    def __init__(self, headlines: list):
        self.headlines = headlines
        self.topics = ["Politics", "Business", "Sports", "Culture", "Science",
                       "Technology", "Health", "Lifestyle"]

    def find_most_common_nouns(self, n=10):
        nouns = Counter()
        for text in self.headlines:
            doc = nlp_en(text)
            nouns.update([token.text.lower() for token in doc if token.pos_ == 'NOUN'])
        return nouns.most_common(n)

    def get_categorized_headlines(self):
        categorized_headlines = {topic: [] for topic in self.topics}

        for headline in self.headlines:
            similarities = [difflib.SequenceMatcher(None, headline.lower(), topic.lower()).ratio() for topic in self.topics]
            best_match_topic = self.topics[similarities.index(max(similarities))]
            categorized_headlines[best_match_topic].append(headline)

        return categorized_headlines

    def get_visualization(self):
        # generates visualization in html file
        data = self.get_categorized_headlines()
        data_dict = {}
        for i in data:
            data_dict[i] = len(data[i])

        df = pd.DataFrame(list(data_dict.items()), columns=['Kategorie', 'Anzahl der Schlagzeilen'])

        ax = df.plot(kind='bar', x='Kategorie', y='Anzahl der Schlagzeilen', legend=False)
        ax.set_ylabel('Anzahl der Schlagzeilen')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        plt.close()


if __name__ == "__main__":
    test_headlines = scraper.NewsScraper('https://www.bbc.com', ['h3']).scraper()
    test_headlines += scraper.NewsScraper('https://www.nytimes.com', ['h3']).scraper()
    test_headlines += scraper.NewsScraper('https://www.latimes.com',  ['h2', 'h3']).scraper()

    analyser = HeadlineAnalyser(test_headlines)

    test_data = analyser.get_categorized_headlines()

    analyser.get_visualization()

'''
    print('Science')
    for i in test_data['Science']:
        print(i)
    print()
    print('Technology')
    for i in test_data['Technology']:
        print(i)
    print()
    for i in test_data:
        print(f'{i}:', len(test_data[i]))
'''