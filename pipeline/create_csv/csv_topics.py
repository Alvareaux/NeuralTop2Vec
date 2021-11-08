#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
import csv
import collections

# Modules
from local.pos import localize_pos

import addons.files
import addons.word_filter

import addons.db.db_texts


class CsvTopics:
    def __init__(self, N, word_lim, stopwords, morph):
        self.N = N
        self.word_lim = word_lim
        self.stopwords = stopwords

        self.morph = morph

    def run(self, result: dict, lang: str, file: str, filter_type: str = 'none', filter_list: list = None):
        if filter_list is None:
            filter_list = []

        addons.files.folder_check(file)

        with open(file, 'w', encoding='utf-8', newline='') as topics_file:
            csv_writer = csv.writer(topics_file, delimiter=';')
            #csv_writer.writerow(['topic', 'word', 'mentions', 'POS'])
            csv_writer.writerow(['Тема', 'Слова', 'Упоминаний', 'Часть речи'])

            for doc_line in result['docs_rating']:
                text = doc_line[0]
                topic = doc_line[1]

                if topic != -1:

                    words_check = collections.Counter()

                    text = text.split(' ')

                    for word in text:
                        if word not in self.stopwords[lang]:
                            words_check[word] += 1

                    grams = [text[i:i + self.N] for i in range(len(text) - self.N + 1)]
                    for gram in grams:
                        words_check[' '.join(gram)] += 1

                    word_list = collections.Counter(e for e in words_check.elements() if words_check[e] >= self.word_lim)

                    for pair in word_list.most_common():
                        phrase = pair[0]
                        mentions = pair[1]
                        pos_tags = self.morph.get_pos(phrase)

                        if addons.word_filter.word_filter(pos_tags, filter_type, filter_list):
                            csv_writer.writerow([topic, phrase, mentions, localize_pos(pos_tags)])