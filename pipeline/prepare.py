#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
import csv

# Modules
from addons.perf_count import perf_count

import addons.sim
import addons.files

import addons.db.db_texts


class PrepareCSV:
    if_header: bool = True  # Skip header row
    if_exist: bool = False  # Use old DB if exist
    if_sim_remove: bool = True  # Use Sim algorithm for duplicates checking
    if_remove_stopwords: bool = False  # TODO NOT IMPLEMENTED Remove stopwords

    def __init__(self, csv_text_col, threshold, preprocess, neural):
        self.csv_text_col = csv_text_col
        self.threshold = threshold

        self.preprocess = preprocess
        self.neural = neural

        self.sim = addons.sim.Sim()

    @perf_count
    def run(self, file: str):

        result_path = f'{file}.db'

        if self.if_exist:
            if addons.files.if_exists(result_path):
                return
        else:
            addons.files.remove_if_exists(result_path)

        documents = {}

        with open(file, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')

            if self.if_header:
                next(csv_reader)

            for row in csv_reader:
                id = int(row[0])

                o_text = ''
                for col in range(self.csv_text_col[0], self.csv_text_col[1]):
                    try:
                        o_text = o_text + row[col] + ' '
                    except IndexError:
                        pass

                text = self.preprocess.clear_text(o_text)
                lang = self.neural.get_lang(text)

                documents[text] = {'id': id,
                                   'text': o_text,
                                   'lang': lang}

        if self.if_sim_remove:
            bad_texts = self.sim.bad_texts(list(documents.keys()), self.threshold)
        else:
            good_texts = list(set(documents.keys()))
            bad_texts = [text for text in documents.keys() if text not in good_texts]

        for text in bad_texts:
            documents.pop(text)

        db = addons.db.db_texts.TextDB(file)

        for doc in documents:
            db.add_text(documents[doc]['id'], documents[doc]['text'], doc, documents[doc]['lang'])

        db.commit()
        db.close()
