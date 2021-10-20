#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base
import functools


def perf_count(f):
    import timeit
    from datetime import timedelta

    @functools.wraps(f)
    def perf_timer(*args, **kwargs):
        start = timeit.default_timer()

        value = f(*args, **kwargs)

        end = timeit.default_timer()
        print(f'{f.__name__} {timedelta(seconds=end - start)}')

        return value

    return perf_timer
