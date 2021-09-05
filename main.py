#!/usr/bin/env python
# -*- coding: utf-8 -*-

import modeling

if __name__ == '__main__':
    topic = modeling.TopicModeling()

    topic.custom_stopwords['ru'].extend(['это', 'й', 'также', 'на', 'это', ''])
    topic.custom_stopwords['uk'].extend(['із', 'не', 'на', 'що', 'за', 'до'])
    topic.custom_stopwords['en'].extend([])

    topic.csv_text_col = (4, 5)
    topic.N = 2
    topic.word_lim = 5

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

    from bertopic import BERTopic
    for i in ['ceo_dev.csv', 'ceo_ecommerce.csv', 'ceo_ecommerce_co.csv', 'ceo_retail.csv', 'dev.csv', 'retail.csv']:
        topic.full_pipeline(f'data/{i}', ['ru', 'uk'], 'result',
                            filter_type=filter_type,
                            filter_list=filter_list,
                            preprocess=True)
