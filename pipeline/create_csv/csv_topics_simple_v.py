#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
import csv

# Modules
import addons.files

import addons.word_filter


class CsvTopicsSimpleV:
    def __init__(self, top_n_words, morph):
        self.top_n_words = top_n_words

        self.morph = morph

    def run(self, result: dict, file: str, filter_type: str = 'none', filter_list: list = None):
        if filter_list is None:
            filter_list = []

        addons.files.folder_check(file)

        with open(file, 'w', encoding='utf-8', newline='') as info_file:
            csv_writer_info = csv.writer(info_file, delimiter=';')

            csv_writer_info.writerow([' '] * (self.top_n_words + 1))

            for topic in result['topics_info']:

                lines = ([int(topic)], [' '], [' '])

                for topic_info in result['topics_info'][topic]:
                    phrase = topic_info[0]
                    prob = topic_info[1]
                    pos_tags = self.morph.get_pos(phrase)

                    if addons.word_filter.word_filter(pos_tags, filter_type, filter_list):
                        lines[0].append(phrase)
                        lines[1].append(prob)
                        lines[2].append(pos_tags)

                for line in lines:
                    csv_writer_info.writerow(line)

                csv_writer_info.writerow([''])
