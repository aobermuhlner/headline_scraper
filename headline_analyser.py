import spacy
import scraper
import difflib
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from textblob import TextBlob

# pip install spacy
# python -m spacy download de_core_news_sm
# python -m spacy download en_core_web_sm

nlp_de = spacy.load('de_core_news_sm')
nlp_en = spacy.load('en_core_web_sm')
nlp = spacy.load('en_core_web_sm')


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
            similarities = [difflib.SequenceMatcher(None, headline.lower(), topic.lower()).ratio() for topic in
                            self.topics]
            best_match_topic = self.topics[similarities.index(max(similarities))]
            categorized_headlines[best_match_topic].append(headline)

        return categorized_headlines

    def find_most_common_adjectives(self, n=10):
        adjectives = Counter()
        for text in self.headlines:
            doc = nlp_en(text)
            adjectives.update([token.text.lower() for token in doc if token.pos_ == 'ADJ'])
        return adjectives.most_common(n)

    def get_topic_sentiments(self, categorized_headlines):
        topic_sentiments = {}
        for topic, headlines in categorized_headlines.items():
            sentiment_scores = []
            for headline in headlines:
                headline_blob = TextBlob(headline)
                sentiment_scores.append(headline_blob.sentiment.polarity)
            topic_sentiments[topic] = sentiment_scores
        return topic_sentiments

    def get_visualization(self):
        categorized_headlines = self.get_categorized_headlines()
        topic_sentiments = self.get_topic_sentiments(categorized_headlines)


        fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

        # Plot categorized headlines
        data_dict = {}
        for i in categorized_headlines:
            data_dict[i] = len(categorized_headlines[i])

        df = pd.DataFrame(list(data_dict.items()), columns=['Kategorie', 'Anzahl der Schlagzeilen'])
        axs[0].bar(df['Kategorie'], df['Anzahl der Schlagzeilen'])
        axs[0].set_ylabel('Anzahl der Schlagzeilen')
        axs[0].set_xticklabels(df['Kategorie'], rotation=45)
        axs[0].set_title('Categorized Headlines')

        # Plot sentiment by topic
        axs[1].boxplot(topic_sentiments.values())
        axs[1].set_xticklabels(topic_sentiments.keys())
        axs[1].set_ylabel('Sentiment')
        axs[1].set_title('Sentiment Analysis by Topic')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    test_headlines = scraper.NewsScraper('https://www.bbc.com', ['h3']).scraper()
    test_headlines += scraper.NewsScraper('https://www.nytimes.com', ['h3']).scraper()
    test_headlines += scraper.NewsScraper('https://www.latimes.com',  ['h2', 'h3']).scraper()

    analyser = HeadlineAnalyser(test_headlines)
    test_data = analyser.get_categorized_headlines()

    analyser.get_visualization()

    print('Science')
    for i in test_data['Science']:
        print(i)
    print()
    print('Sport')
    for i in test_data['Sports']:
        print(i)
    print()
    for i in test_data:
        print(f'{i}:', len(test_data[i]))
