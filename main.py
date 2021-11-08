#!/usr/bin/env python
# -*- coding: utf-8 -*-

import modeling

if __name__ == '__main__':
    csv_text_col = (18, 24)

    topic = modeling.TopicModeling(csv_text_col)

    topic.custom_stopwords['ru'].extend(['это', 'й', 'также', 'на', 'это', ''])
    topic.custom_stopwords['uk'].extend(['із', 'не', 'на', 'що', 'за', 'до', 'це', 'про', 'та'])
    topic.custom_stopwords['en'].extend([])
    topic.update_stopwords()

    topic.csv_text_col = (18, 24)
    topic.N = 2
    topic.word_lim = 5

    nr_topics = 'auto'
    topic.nr_topics = nr_topics

    filter_type = 'white'
    filter_list = ['NOUN + NOUN',

                   'NOUN + NONE',
                   'NONE + NOUN',

                   'NOUN + VERB',
                   'VERB + NOUN',

                   'NOUN + INFN',
                   'INFN + NOUN',

                   'NOUN + ADJF',
                   'ADJF + NOUN',

                   'NOUN + ADJS',
                   'ADJS + NOUN',

                   ]

#    topic.proceed_txt('data/1.csv.ru.txt')
#    topic.create_csv_texts('result/1/texts.csv')
#    topic.create_csv_topics('result/1/topics.csv')
#    topic.create_csv_topics_simple('result/1/simple.csv')
#    topic.merge_csv(['result/1/texts.csv', 'result/1/topics.csv', 'result/1/simple.csv'], 'result/1.xlsx')

    for i in ['publications_07.11.2021-21_53_39.csv', 'publications_07.11.2021-19_29_47.csv']:
        topic.full_pipeline(f'data/{i}', ['ru', 'uk'], 'result',
                            filter_list=filter_list, filter_type=filter_type,
                            if_exist=True,
                            preprocess=True)
