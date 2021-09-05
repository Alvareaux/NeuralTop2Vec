#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
import os.path
import errno

import csv

import functools
import collections

# Modules
import addons.morph
import addons.neural
import addons.topic
import addons.preprocess
import addons.xlsx

# External libs
from nltk.corpus import stopwords


def perf_count(f):
    import timeit
    from datetime import timedelta

    @functools.wraps(f)
    def perf_timer(*args, **kwargs):
        start = timeit.default_timer()

        value = f(*args, **kwargs)

        end = timeit.default_timer()
        print(f'{f.__name__} {timedelta(seconds=end - start)}')

        return value

    return perf_timer


def folder_check(path: str):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


class TopicModeling:

    __model = None

    __docs_rating = None
    __topics_list = None
    __topics_info = None
    __topics_repr = None

    N = 2
    word_lim = 5
    top_n_words = 30  # TODO get from model settings object

    # Default shukach csv values
    csv_text_col = (18, 24)

    custom_stopwords = {'ru': [],
                        'uk': [],
                        'en': [],
                        }  # TODO reload stopwords func

    def __init__(self):
        self.__model = addons.topic.BERTopicEngine()

        self.settings = addons.topic.ModelSettings()

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
                          'all': russian_stopwords + ukrainian_stopwords  # TODO stopwords for all lang
                          }

    def set_settings(self):
        pass

    @perf_count
    def prepare_csv(self, file: str, header: bool = True, if_all: bool = True):
        documents = collections.defaultdict(list)

        with open(file, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')

            if header:
                next(csv_reader)

            for row in csv_reader:
                text = ''
                for col in range(self.csv_text_col[0], self.csv_text_col[1]):
                    try:
                        text = text + row[col] + ' '
                    except IndexError:
                        pass

                text = self.preprocess.clear_text(text)

                documents[self.neural.get_lang(text)].append(text)
                if if_all:
                    documents['all'].append(text)

        for lang in documents:
            documents[lang] = list(set(documents[lang]))

        for lang in documents:
            with open(f'{file}.{lang}.txt', 'w', encoding='utf-8') as doc_file:
                doc_file.writelines('\n'.join(documents[lang]))

    @perf_count
    def proceed_txt(self, file: str, load_if_exist: bool = True, preprocess: bool = False):
        self.__model = addons.topic.BERTopicEngine()

        model_path = file + '.model'

        doc_file = open(file, 'r', encoding='utf-8')
        docs = doc_file.readlines()

        load_model = False
        if load_if_exist:
            load_model = os.path.isfile(model_path)

        if not load_model:
            if preprocess:
                docs = self.preprocess_docs(docs)

            self.__model.create_vectorizer(self.settings)
            self.__model.create_model(self.settings)

            result = self.__model.fit_model(docs, model_path)

        else:
            result = self.__model.load_model(file + '.model')

        self.__docs_rating = self.zip_texts(docs, result)
        self.__topics_info = self.__model.get_topics()
        self.__topics_list = self.__topics_info.keys()
        self.__topics_repr = {topic: self.__model.get_representative_docs(topic) for topic in self.__topics_list
                              if topic > -1}
        self.__topics_repr[-1] = []

    def create_csv_texts(self, file: str):
        folder_check(file)

        with open(file, 'w', encoding='utf-8', newline='') as result_file:
            csv_writer = csv.writer(result_file, delimiter=';')
            csv_writer.writerow(['topic', 'best', 'text', 'prob', 'len'])

            for doc_line in self.__docs_rating:
                text = doc_line[0]
                topic = doc_line[1]
                prob = doc_line[2]

                best = ''
                if text in self.__topics_repr[topic]:
                    best = '+'

                csv_writer.writerow([topic, best, text, prob, len(text)])

    def create_csv_topics(self, file: str, filter_type: str = 'none', filter_list: list = []):
        folder_check(file)

        with open(file, 'w', encoding='utf-8', newline='') as topics_file:
            csv_writer = csv.writer(topics_file, delimiter=';')
            csv_writer.writerow(['topic', 'word', 'mentions', 'POS'])

            for doc_line in self.__docs_rating:
                text = doc_line[0]
                topic = doc_line[1]

                words_check = collections.Counter()

                lang = self.neural.get_lang(text)
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

                    if self.word_filter(pos_tags, filter_type, filter_list):
                        csv_writer.writerow([topic, phrase, mentions, pos_tags])

    def create_csv_topics_simple_v(self, file: str, filter_type: str = 'none', filter_list: list = []):
        folder_check(file)

        with open(file, 'w', encoding='utf-8', newline='') as info_file:
            csv_writer_info = csv.writer(info_file, delimiter=';')
            csv_writer_info.writerow(['topic', 'word', 'prob', 'POS'])

            for topic in self.__topics_info:
                for topic_info in self.__topics_info[topic]:
                    phrase = topic_info[0]
                    prob = topic_info[1]
                    pos_tags = self.morph.get_pos(phrase)

                    if self.word_filter(pos_tags, filter_type, filter_list):
                        csv_writer_info.writerow([topic, phrase, prob, pos_tags])

    def create_csv_topics_simple_h(self, file: str, filter_type: str = 'none', filter_list: list = []):
        folder_check(file)

        with open(file, 'w', encoding='utf-8', newline='') as info_file:
            csv_writer_info = csv.writer(info_file, delimiter=';')

            csv_writer_info.writerow([' '] * (self.top_n_words + 1))

            for topic in self.__topics_info:

                lines = ([int(topic)], [' '], [' '])

                for topic_info in self.__topics_info[topic]:
                    phrase = topic_info[0]
                    prob = topic_info[1]
                    pos_tags = self.morph.get_pos(phrase)

                    if self.word_filter(pos_tags, filter_type, filter_list):
                        lines[0].append(phrase)
                        lines[1].append(prob)
                        lines[2].append(pos_tags)

                for line in lines:
                    csv_writer_info.writerow(line)

                csv_writer_info.writerow([''])

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


    @staticmethod
    def word_filter(pos_tags, filter_type: str, filter_list: list) -> bool:
        if filter_type == 'none':
            return True

        elif filter_type == 'white':
            if pos_tags in filter_list:
                return True
            else:
                return False

        elif filter_type == 'black':
            if pos_tags not in filter_list:
                return True
            else:
                return False

        else:
            raise NotImplementedError

    @staticmethod
    def zip_texts(docs: list[str], result: list[[int], [float]]) -> list[(str, int, float)]:
        return list(zip(docs, result[0], result[1]))

    def full_pipeline(self, file: str, langs: list[str], output_folder: str,
                      filter_type: str = 'none', filter_list: list = [], preprocess: bool = False):
        file_base = os.path.splitext(os.path.basename(file))[0]

        self.prepare_csv(file)
        for lang in langs:
            try:
                self.proceed_txt(f'{file}.{lang}.txt', preprocess=preprocess)
                self.create_csv_texts(f'{output_folder}/{file_base}-{lang}/texts.csv')
                self.create_csv_topics(f'{output_folder}/{file_base}-{lang}/topics.csv',
                                       filter_type, filter_list)
                self.create_csv_topics_simple_v(f'{output_folder}/{file_base}-{lang}/simple_v.csv',
                                                filter_type, filter_list)
                self.create_csv_topics_simple_h(f'{output_folder}/{file_base}-{lang}/simple_h.csv',
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