#!/usr/bin/env python
# -*- coding: utf-8 -*-

pos_loc = {
    'NOUN': 'Имя существительное',
    'ADJF': 'Имя прилагательное (полное)',
    'ADJS': 'Имя прилагательное (краткое)',
    'COMP': 'Компаратив',
    'VERB': 'Глагол (личная форма)',
    'INFN': 'Глагол (инфинитив)',
    'PRTF': 'Причастие (полное)',
    'PRTS': 'Причастие (краткое)',
    'GRND': 'Деепричастие',
    'NUMR': 'Числительное',
    'ADVB': 'Наречие',
    'NPRO': 'Местоимение',
    'PRED': 'Предикатив',
    'PREP': 'Предлог',
    'CONJ': 'Ссоюз',
    'PRCL': 'Частица',
    'INTJ': 'Междометие',
    'NONE': 'Не часть',
}

pos_simple = {
    'ADJF': 'NOUN', 'ADJS': 'NOUN',
    'INFN': 'VERB',
    'PRTS': 'PRTF',
}


def localize_pos(pos,
                 if_ru=True, if_simple=False):
    if if_simple:
        try:
            pos = pos_simple[pos]
        except KeyError:
            pass

    if if_ru:
        try:
            pos = pos_loc[pos]
        except KeyError:
            pass

    return pos
