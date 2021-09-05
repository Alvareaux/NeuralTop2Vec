#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Interface
from addons.interface import i_preprocess

# Base
import regex as re

import string
import unicodedata
import html


class Preprocess(i_preprocess.ClearText):

    @staticmethod
    def normalize(text):
        return unicodedata.normalize("NFKD", text)

    @staticmethod
    def remove_control_characters(text):
        new_text = ''

        for ch in text:
            if unicodedata.category(ch)[0] == "C":
                new_text += ' '
            else:
                new_text += ch

        return new_text

    @staticmethod
    def remove_punctuation(text):
        text = text.replace('“', '').replace('”', '').replace('«', '').replace('»', '')
        return text.translate(str.maketrans('', '', string.punctuation))

    @staticmethod
    def remove_digits(text):
        new_text = ''

        for ch in text:
            if ch.isdigit():
                new_text += ' '
            else:
                new_text += ch

        return new_text

    @staticmethod
    def remove_single(text):
        """
        Удаляет одинокие символы, окруженные пробелами
        Необходимо для увеличения точности отчистки, они так или иначе отсекаются лемматизацией
        """

        text = re.sub(r' . ', ' ', text)
        return text

    @staticmethod
    def letter_check(text):
        """
        Проверяет, остались ли только буквы(любой язык)
        """

        text = text.replace('ї', 'ї').replace('й', 'й')
        text = [token for token in text.split() if token.isalpha()]

        return ' '.join(text)

    @staticmethod
    def remove_html(text):
        return html.unescape(text)

    def clear_text(self, text: str) -> str:
        text = text.replace('\n', ' ')
        text = self.normalize(text)

        text = self.remove_html(text)
        text = self.remove_digits(text)

        text = self.remove_control_characters(text)
        text = self.remove_punctuation(text)
        text = self.remove_single(text)

        text = self.letter_check(text)

        text = text.replace('\xa0', ' ').replace('\xa0', ' ')

        t = ''
        for ch in text:
            if ch.isalpha():
                t += ch.lower()
            else:
                t += ch

        text = t

        return text
