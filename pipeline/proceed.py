#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Modules
from addons.perf_count import perf_count

import addons.files

import addons.db.db_texts


class ProceedDB:
    if_exist: bool = False   # Use old model if exist

    def __init__(self, model):
        self.__model = model

    @perf_count
    def run(self, file: str, lang: str):

        model_path = f'{file}.{lang}.model'

        load_model = False
        if self.if_exist:
            load_model = addons.files.if_exists(model_path)

        db = addons.db.db_texts.TextDB(file)
        docs = db.get_texts(lang)

        if not load_model:
            self.__model.create_model()
            result = self.__model.fit_model(docs, model_path)

        else:
            result = self.__model.load_model(model_path )

        docs_rating = self.zip_texts(docs, result)
        topics_info = self.__model.get_topics()
        topics_list = topics_info.keys()
        topics_repr = {topic: self.__model.get_representative_docs(topic) for topic in topics_list
                       if topic > -1}
        topics_repr[-1] = []

        return {'docs_rating': docs_rating,
                'topics_info': topics_info,
                'topics_list': topics_list,
                'topics_repr': topics_repr}

    @staticmethod
    def zip_texts(docs: list[str], result: list[[int], [float]]) -> list[(str, int, float)]:
        return list(zip(docs, result[0], result[1]))
