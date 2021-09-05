#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Interface
from addons.interface import i_morph

# External libs
import pymorphy2


class PyMorphyEngine(i_morph.MorphEngine):
    morph = pymorphy2.MorphAnalyzer()

    def get_pos(self, phrase):
        phrase = phrase.split(' ')
        pos_tags = ''

        for word in phrase:
            p = self.morph.parse(word)[0]
            try:
                pos_tags += p.tag.POS
            except TypeError:
                pos_tags += 'NONE'

            if word != phrase[-1]:
                pos_tags += ' + '

        return pos_tags
