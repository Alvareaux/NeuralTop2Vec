#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
import csv

# Modules
import addons.files
import addons.db.db_texts


class CsvTexts:

    @staticmethod
    def run(result: dict, lang: str, file: str, dbfile: str):
        addons.files.folder_check(file)

        db = addons.db.db_texts.TextDB(dbfile)
        texts = db.get_all(lang)

        with open(file, 'w', encoding='utf-8', newline='') as result_file:
            csv_writer = csv.writer(result_file, delimiter=';')
            csv_writer.writerow(['topic', 'best', 'text', 'prob', 'len'])

            for doc_line in result['docs_rating']:
                text = doc_line[0]
                o_text = texts[doc_line[0]]['text']
                topic = doc_line[1]
                prob = doc_line[2]

                best = ''
                if text in result['topics_repr'][topic]:
                    best = '+'

                csv_writer.writerow([topic, best, o_text, prob, len(text)])
