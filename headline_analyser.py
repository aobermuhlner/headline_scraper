import spacy
import scraper
import difflib
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from textblob import TextBlob

# pip install spacy
# pip install textblob
# python -m spacy download en_core_web_sm


class HeadlineAnalyser:
    def __init__(self, headlines: list):
        self.headlines = headlines
        self.nlp_en = spacy.load('en_core_web_sm')
        self.topics = ["Politics", "Business", "Sports", "Culture", "Science", "Tech", "Health", "Lifestyle"]

    def get_most_common_persons(self, n=10):
        persons = Counter()
        for text in self.headlines:
            doc = self.nlp_en(text)
            person_names = [ent.text.lower() for ent in doc.ents if ent.label_ == 'PERSON']
            full_names = [name.replace("'s", "").title() for name in person_names]
            persons.update(full_names)
        return persons.most_common(n)

    def get_categorized_headlines(self):
        categorized_headlines = {topic: [] for topic in self.topics}

        for headline in self.headlines:
            similarities = [difflib.SequenceMatcher(None, headline.lower(), topic.lower()).ratio() for topic in
                            self.topics]
            best_match_topic = self.topics[similarities.index(max(similarities))]
            categorized_headlines[best_match_topic].append(headline)

        return categorized_headlines

    def get_topic_sentiments(self):
        topic_sentiments = {}
        for topic, headlines in self.get_categorized_headlines().items():
            sentiment_scores = []
            for headline in headlines:
                headline_blob = TextBlob(headline)
                sentiment_scores.append(headline_blob.sentiment.polarity)
            topic_sentiments[topic] = sentiment_scores
        return topic_sentiments

    def get_visualization(self):
        most_common_names = self.get_most_common_persons()
        categorized_headlines = self.get_categorized_headlines()
        topic_sentiments = self.get_topic_sentiments()
        # preparing data
        # most common nouns
        df_names = pd.DataFrame(most_common_names, columns=['Names', 'Number'])
        # percentage by topic
        cat_headline_dict = {}
        for i in categorized_headlines:
            cat_headline_dict[i] = len(categorized_headlines[i])
        df_cat_headline = pd.DataFrame(list(cat_headline_dict.items()), columns=['Category', 'Numbers of headlines'])
        df_cat_headline['Numbers of headlines'] \
            = df_cat_headline['Numbers of headlines'] / df_cat_headline['Numbers of headlines'].sum()
        # create subplot
        fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
        # plot most common nouns
        axs[0].bar(df_names['Names'], df_names['Number'])
        axs[0].set_ylabel('Absolute numbers')
        axs[0].set_title('Most common Names')
        axs[0].tick_params(axis='x', rotation=45)
        # plot percentage by topic
        axs[1].bar(df_cat_headline['Category'], df_cat_headline['Numbers of headlines'])
        axs[1].set_ylabel('Percentage by Topic')
        axs[1].set_title('Categorized Headlines')
        # plot sentiment by topic
        axs[2].boxplot(topic_sentiments.values())
        axs[2].set_xticklabels(topic_sentiments.keys())
        axs[2].set_ylabel('Sentiment [-1, 1]')
        axs[2].set_title('Sentiment Analysis by Topic')
        # save and show plot
        plt.tight_layout()
        plt.savefig('headline_analysis.png')
        plt.show()
        plt.close()

if __name__ == "__main__":

    test_scraper = scraper.NewsScraper(['h2', 'h3'])
    test_scraper.clear_cache()
    test_headlines = test_scraper.scraper()
    analyser = HeadlineAnalyser(test_headlines)
    analyser.get_visualization()
    print(analyser.get_most_common_persons())

