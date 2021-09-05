#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Interface
from addons.interface import i_neural

# External libs
import fasttext


class FastTextLang(i_neural.LangNeural):
    model = None

    def __init__(self, path):
        self.model = fasttext.load_model(path)

    @staticmethod
    def fasttext_zip(result):
        zip_result = []
        for i in range(len(result[0])):
            zip_result.append([result[0][i].replace('__label__', ''), result[1][i]])

        return zip_result

    def get_lang(self, text: str, lang_count: int = 1) -> str:
        lang = self.model.predict(text.replace('\n', ''), k=lang_count)

        lang_list = self.fasttext_zip(lang)

        return list(list(zip(*lang_list))[0])[0]

    def get_lang_prob(self, text: str, lang_count: int = 1) -> list:
        lang = self.model.predict(text.replace('\n', ''), k=lang_count)

        lang_list = self.fasttext_zip(lang)

        return lang_list
