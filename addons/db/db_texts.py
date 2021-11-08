#!/usr/bin/env python
# -*- coding: utf-8 -*-

# External libs
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy import insert

base = declarative_base()

# ---------------------------------------------------------------------------------------------------------------------
# Объявление базы данных


class Texts(base):
    __tablename__ = 'texts'

    text_id = Column(Integer, primary_key=True, nullable=False)
    text_original = Column(String, nullable=False)
    text_modified = Column(String, nullable=False)
    lang = Column(String, nullable=False)


class TextDB:

    def __init__(self, path):
        engine = create_engine(f'sqlite:///{path}.db')
        base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        self.session = session()

    def add_text(self, text_id, text_original, text_modified, lang):
        text = Texts(text_id=text_id, text_original=text_original, text_modified=text_modified, lang=lang)
        self.session.add(text)

    def get_texts(self, lang):
        rows = self.session.query(Texts).filter(Texts.lang == lang).all()
        return [row.text_modified for row in rows]

    def get_all(self, lang):
        rows = self.session.query(Texts).filter(Texts.lang == lang).all()
        return {row.text_modified: {'id': row.text_id, 'text': row.text_original, 'lang': row.lang} for row in rows}

    def commit(self):
        self.session.commit()

    def close(self):
        self.session.close()
