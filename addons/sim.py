from collections import defaultdict
from collections import Counter

from tqdm import tqdm

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

import gc

import numpy as np


class Sim:

    def __init__(self, filter_type: str = 'none', filter_list: list = None):
        self.filter_type = filter_type
        self.filter_list = filter_list

    def bad_texts(self, texts: list[str], threshold: float, stopwords: list[str] = None, min_df=1, max_df=1.0):
        new_texts = self.clear(texts, threshold, stopwords, min_df, max_df)

        return [text for text in texts if text not in new_texts]

    def clear(self, texts: list[str], threshold: float, stopwords: list[str] = None, min_df=1, max_df=1.0):
        vect = TfidfVectorizer(min_df=min_df, max_df=max_df, stop_words=stopwords)
        tfidf = vect.fit_transform(texts)
        sim = tfidf * tfidf.T
        sim = sim.tocoo()

        pop_list = []
        for i, j, score in zip(sim.row, sim.col, sim.data):
            if i != j:
                if score > threshold:
                    i_len = len(texts[i])
                    j_len = len(texts[j])

                    if i_len > j_len:
                        smaller_text = i
                    else:
                        smaller_text = j

                    pop_list.append(smaller_text)

        new_texts = []
        for i in range(len(texts)):
            if i not in pop_list:
                new_texts.append(texts[i])

        return new_texts

