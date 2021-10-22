#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
import os.path

# Modules
import addons.morph
import addons.neural
import addons.topic
import addons.preprocess
import addons.xlsx

import pipeline.prepare
import pipeline.proceed
import pipeline.create_csv.csv_texts
import pipeline.create_csv.csv_topics
import pipeline.create_csv.csv_topics_simple_h
import pipeline.create_csv.csv_topics_simple_v

# External libs
from nltk.corpus import stopwords


class TopicModeling:
    __model = None

    __result = None

    prepare = None
    proceed = None

    create_csv_texts = None
    create_csv_topics = None
    create_csv_topics_simple_v = None
    create_csv_topics_simple_h = None

    word_lim = 5  # Limit of words mentions
    threshold = 0.85  # Sim threshold

    custom_stopwords = {'ru': [],
                        'uk': [],
                        'en': [],
                        }

    def __init__(self, csv_text_col):
        self.__model = addons.topic.BERTopicEngine()

        self.csv_text_col = csv_text_col
        self.N = max(self.__model.n_gram_range)
        self.top_n_words = self.__model.top_n_words

        self.morph = addons.morph.PyMorphyEngine()
        self.neural = addons.neural.FastTextLang('lid.176.bin')
        self.preprocess = addons.preprocess.Preprocess()
        self.xlsx = addons.xlsx.PandasXLSX()

        english_stopwords = stopwords.words("english")
        russian_stopwords = stopwords.words("russian")
        ukrainian_stopwords = stopwords.words("ukrainian")

        self.stopwords = {'ru': russian_stopwords + self.custom_stopwords['ru'],
                          'uk': ukrainian_stopwords + self.custom_stopwords['uk'],
                          'en': english_stopwords + self.custom_stopwords['en'],
                          }

        self.setup_pipeline()

    def setup_pipeline(self):
        self.prepare = pipeline.prepare.PrepareCSV(self.csv_text_col, self.threshold,
                                                   self.preprocess, self.neural)
        self.proceed = pipeline.proceed.ProceedDB(self.__model)

        self.create_csv_texts = pipeline.create_csv.csv_texts.CsvTexts()
        self.create_csv_topics = pipeline.create_csv.csv_topics.CsvTopics(self.N, self.word_lim, self.stopwords,
                                                                          self.morph)
        self.create_csv_topics_simple_v = pipeline.create_csv.csv_topics_simple_v.CsvTopicsSimpleV(self.top_n_words,
                                                                                                   self.morph)
        self.create_csv_topics_simple_h = pipeline.create_csv.csv_topics_simple_h.CsvTopicsSimpleH(self.morph)

    def merge_csv(self, files, output):
        self.xlsx.merge(files, output)

    def preprocess_docs(self, docs):
        lang = self.neural.get_lang(docs[0])

        new_docs = []
        for doc in docs:
            doc_words = doc.split()

            new_doc = []
            for word in doc_words:
                if word not in self.stopwords[lang]:
                    new_doc.append(word)

            new_docs.append(' '.join(new_doc))

        return new_docs

    def update_stopwords(self):
        english_stopwords = stopwords.words("english")
        russian_stopwords = stopwords.words("russian")
        ukrainian_stopwords = stopwords.words("ukrainian")

        self.stopwords = {'ru': russian_stopwords + self.custom_stopwords['ru'],
                          'uk': ukrainian_stopwords + self.custom_stopwords['uk'],
                          'en': english_stopwords + self.custom_stopwords['en'],
                          }

    def full_pipeline(self, file: str, langs: list[str], output_folder: str,
                      filter_type: str = 'none', filter_list: list = None, preprocess: bool = False):
        if filter_list is None:
            filter_list = []

        file_base = os.path.splitext(os.path.basename(file))[0]

        # self.prepare.if_exist = True
        # self.proceed.if_exist = True

        self.prepare.run(file)  # Data preparation

        for lang in langs:
            try:
                self.__result = self.proceed.run(file, lang)  # Model setup

                self.create_csv_texts.run(self.__result, lang,
                                          f'{output_folder}/{file_base}-{lang}/texts.csv', file)
                self.create_csv_topics.run(self.__result, lang,
                                           f'{output_folder}/{file_base}-{lang}/topics.csv',
                                           filter_type, filter_list)
                self.create_csv_topics_simple_v.run(self.__result,
                                                    f'{output_folder}/{file_base}-{lang}/simple_v.csv',
                                                    filter_type, filter_list)
                self.create_csv_topics_simple_h.run(self.__result,
                                                    f'{output_folder}/{file_base}-{lang}/simple_h.csv',
                                                    filter_type, filter_list)

                self.merge_csv([f'{output_folder}/{file_base}-{lang}/texts.csv',
                                f'{output_folder}/{file_base}-{lang}/topics.csv',
                                f'{output_folder}/{file_base}-{lang}/simple_v.csv',
                                f'{output_folder}/{file_base}-{lang}/simple_h.csv'],
                               f'{output_folder}/{file_base}-{lang}.xlsx')

                fig = self.__model.visualize_topics()
                fig.write_html(f'{output_folder}/{file_base}-{lang}.html')

            except ValueError as err:
                print(f'Bad learn data in {file}')
                print(err)

            except TypeError as err:
                print(f'Bad learn data in {file}')
                print(err)

            # TODO remake errors
