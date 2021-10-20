#!/usr/bin/env python
# -*- coding: utf-8 -*-

def word_filter(pos_tags, filter_type: str, filter_list: list) -> bool:
    if filter_type == 'none':
        return True

    elif filter_type == 'white':
        if pos_tags in filter_list:
            return True
        else:
            return False

    elif filter_type == 'black':
        if pos_tags not in filter_list:
            return True
        else:
            return False

    else:
        raise NotImplementedError
