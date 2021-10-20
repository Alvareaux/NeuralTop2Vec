#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Interface
from addons.interface import i_topic

# Base
import pickle

# External libs
from bertopic import BERTopic

from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer


class BERTopicEngine(i_topic.TopicEngine):
    model = None
    model_path = None

    models = {
        'vectorizer_model': True,
        'embedding_model': False,
        'umap_model': False,
        'hdbscan_model': False
    }

    vectorizer_model = None
    embedding_model = None
    umap_model = None
    hdbscan_model = None

    # Base model
    language = 'multilingual'  # 'english'

    top_n_words = 30  # 10
    n_gram_range = (1, 2)  # (1, 1)
    min_topic_size = 10  # 10
    nr_topics = None  # None /'auto'

    low_memory = True  # False
    calculate_probabilities = False  # False

    seed_topic_list = None  # None /List[List[str]]

    verbose = True  # False

    # Vectorizer
    stop_words = []
    # max_df is used for removing terms that appear too frequently, also known as "corpus-specific stop words"
    max_df = 0.7  # 1.0
    # min_df is used for removing terms that appear too infrequently
    min_df = 0.2  # 1

    # Embedding
    embedding_model_name = None

    # UMAP
    n_neighbors = 15,
    n_components = 10,
    min_dist = 0.0,
    u_metric = 'cosine'

    # HDBSCAN
    min_cluster_size = 5
    min_samples = None
    cluster_selection_epsilon = 0.0
    hdb_metric = 'euclidean'
    alpha = 1.0
    p = None,
    algorithm = 'best'
    leaf_size = 40,
    cluster_selection_method = 'eom'

    def create_model(self):
        if self.models['vectorizer_model']:
            self.create_vectorizer()
        else:
            self.vectorizer_model = None

        if self.models['embedding_model']:
            self.create_embedding()
        else:
            self.embedding_model = None

        if self.models['umap_model']:
            self.create_umap()
        else:
            self.umap_model = None

        if self.models['hdbscan_model']:
            self.create_hdbscan()
        else:
            self.hdbscan_model = None

        self.create_bertopic()

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

    def create_vectorizer(self):
        self.vectorizer_model = CountVectorizer(ngram_range=self.n_gram_range,
                                                stop_words=self.stop_words,
                                                min_df=self.min_df,
                                                max_df=self.max_df
                                                )

    def create_embedding(self):
        if self.embedding_model_name is not None:
            self.embedding_model = SentenceTransformer(self.embedding_model_name)

    def create_umap(self):
        self.umap_model = UMAP(n_neighbors=self.n_neighbors,
                               n_components=self.n_components,
                               min_dist=self.min_dist,
                               metric=self.u_metric)

    def create_hdbscan(self):
        self.hdbscan_model = HDBSCAN(min_cluster_size=self.min_cluster_size,
                                     min_samples=self.min_samples,
                                     cluster_selection_epsilon=self.cluster_selection_epsilon,
                                     metric=self.hdb_metric,
                                     alpha=self.alpha,
                                     p=self.p,
                                     algorithm=self.algorithm,
                                     leaf_size=self.leaf_size,
                                     cluster_selection_method=self.cluster_selection_method
                                     )

    def create_bertopic(self):
        self.model = BERTopic(embedding_model=self.embedding_model,
                              vectorizer_model=self.vectorizer_model,
                              umap_model=self.umap_model,
                              hdbscan_model=self.hdbscan_model,

                              language=self.language,

                              top_n_words=self.top_n_words,
                              n_gram_range=self.n_gram_range,
                              min_topic_size=self.min_topic_size,
                              nr_topics=self.nr_topics,

                              low_memory=self.low_memory,
                              calculate_probabilities=self.calculate_probabilities,

                              seed_topic_list=self.seed_topic_list,

                              verbose=self.verbose,

                              )
