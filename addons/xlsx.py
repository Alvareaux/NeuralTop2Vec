#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Interface
from addons.interface import i_xlsx

# Base
import sys
import os

# External libs
import pandas as pd


class PandasXLSX(i_xlsx.XLSX):

    @staticmethod
    def merge(files: list[str], output: str, sep=';'):
        writer = pd.ExcelWriter(output)
        for file in files:
            df = pd.read_csv(file, sep=';')
            df.to_excel(writer, sheet_name=os.path.splitext(os.path.basename(file))[0], index=False)

        writer.save()
