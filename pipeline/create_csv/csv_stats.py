#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
import csv
import collections

# External libs
import sklearn
import numpy as np

# Modules
import addons.files
import addons.db.db_texts


class CsvStats:
    model = None

    def __init__(self, model):
        self.model = model

    def run(self, result: dict, lang: str, file: str, dbfile: str):
        addons.files.folder_check(file)

        db = addons.db.db_texts.TextDB(dbfile)
        texts = db.get_all(lang)

        label_stats = collections.Counter()
        len_stats = collections.defaultdict(list)
        for doc_line in result['docs_rating']:
            o_text = texts[doc_line[0]]['text']
            topic = doc_line[1]
            if topic != -1:
                len_stats[topic].append(len(o_text))
                label_stats[topic] += 1

        all_texts = sum(label_stats.values())
        distance_matrix = self.__get_distance_matrix()

        with open(file, 'w', encoding='utf-8', newline='') as result_file:
            csv_writer = csv.writer(result_file, delimiter=';')
            csv_writer.writerow(['Тема', 'Оценка', 'Количество текстов', '% текстов', 'Средняя длина', 'Дельта длины'])

            for topic in result['topics_info']:
                if topic != -1:
                    # topic_distance = list(distance_matrix[topic])
                    # topic_distance.remove(min(topic_distance))

                    topic_value = result['topics_info'][topic][0][1]
                    # mst = list(topic_distance).index(min(topic_distance))
                    text_prc = (label_stats[topic] / all_texts) * 100
                    avg_len = int(sum(len_stats[topic]) / len(len_stats[topic]))
                    delta_len = abs(min(len_stats[topic]) - max(len_stats[topic]))

                    csv_writer.writerow([topic, topic_value, label_stats[topic], text_prc, avg_len, delta_len])

    def __get_distance_matrix(self):
        topic_model = self.model

        embeddings = np.array(topic_model.model.topic_embeddings)
        topics = sorted(list(topic_model.model.get_topics().keys()))

        all_topics = sorted(list(topic_model.model.get_topics().keys()))
        indices = np.array([all_topics.index(topic) for topic in topics])
        embeddings = embeddings[indices]

        distance_matrix = 1 - sklearn.metrics.pairwise.cosine_similarity(embeddings)

        return distance_matrix
