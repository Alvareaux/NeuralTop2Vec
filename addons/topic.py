#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Interface
from addons.interface import i_topic

# Base
from dataclasses import dataclass
import pickle

# External libs
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer



@dataclass
class ModelSettings:
    language: str = 'multilingual'

    top_n_words: int = 30
    n_gram_range: tuple = (1, 2)
    calculate_probabilities: bool = False

    low_memory: bool = True
    verbose: bool = True

    min_df: int = 10
    nr_topics: str = 'auto'


class BERTopicEngine(i_topic.TopicEngine):
    model = None
    vectorizer = None

    model_path = None

    def create_vectorizer(self, settings: ModelSettings):
        self.vectorizer = CountVectorizer(ngram_range=settings.n_gram_range,
                                          #min_df=settings.min_df
                                          )

    def create_model(self, settings: ModelSettings):
        self.model = BERTopic(
                              language=settings.language,
                              top_n_words=settings.top_n_words,
                              n_gram_range=settings.n_gram_range,
                              calculate_probabilities=settings.calculate_probabilities,
                              verbose=settings.verbose,
                              low_memory=settings.low_memory,
                              #nr_topics=settings.nr_topics,
                              )

    def load_model(self, path: str):
        self.model = BERTopic.load(path)
        self.model_path = path

        return self.get_model_result(path)

    def save_model(self, path: str):
        self.model.save(path)
        self.model_path = path

    def fit_model(self, docs: list, path: str):
        result = self.model.fit_transform(docs)

        self.save_model(path)

        with open(path + '.dat', 'wb') as fp:
            pickle.dump(result, fp)

        return result

    def get_model_result(self, path: str):
        with open(path + '.dat', 'rb') as fp:
            return pickle.load(fp)

    def get_topics(self):
        return self.model.get_topics()

    def get_representative_docs(self, topic):
        return self.model.get_representative_docs(topic)

    def visualize_topics(self):
        return self.model.visualize_topics()

    def visualize_heatmap(self):
        return self.model.visualize_heatmap()
