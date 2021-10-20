#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
import os
import errno


def folder_check(path: str):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


def if_exists(path):
    if os.path.exists(path):
        return True
    else:
        return False


def remove(path):
    os.remove(path)
    return True


def remove_if_exists(path):
    if if_exists(path):
        remove(path)
        return True
    else:
        return False
