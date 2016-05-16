#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os
import numpy as np
import re

#from matplotlib import pyplot as plt

# count articles / ads that have some particular word

#basepath = "/srv/data/newspapers/newspapers/fin/"
basepath = "testdata/fin/"


def count_items_with_word(items, word):
    cnt = 0
    for a in items:
        with open(a, 'r') as f:
            text = f.read()
            text = text.lower()
            tokens = text.split()
            for t_i, token in enumerate(tokens):
                if token.startswith(word):
                    cnt += 1
                    break
    return cnt

def get_word_counts(items, word):
    d = dict()
    for a in items:
        a_word_cnt = 0
        with open(a, 'r') as f:
            text = f.read()
            text = text.lower()
            tokens = text.split()
            for t_i, token in enumerate(tokens):
                if token.startswith(word):
                    a_word_cnt += 1
        d[a] = a_word_cnt
    return d

rep = re.compile(r".*\/([0-9]*)\/(.*)\/.*_([0-9]*-[0-9]*-[0-9]*)_(.*)\/extracted\/(.*).txt")

def get_info_for_item(filename):
    """
    returns tuple (iss, year, date, number, date_number, item)
    """
    print filename
    m = rep.match(filename)
    if m:
        year, iss, date, number, item = m.groups()
        date_number = date + "_" + number
        return year, iss, date, number, date_number, item
    else:
        return None

def get_info_for_items(items):
    d = dict()
    for a in items:
        d[a] = get_info_for_item(a)
    return d


if __name__ == "__main__":
    # ...
    word = sys.argv[1]
    start_year = 1880
    end_year = 1905
    print "range", start_year, end_year
    all_years = os.listdir(basepath)
    years = [y for y in all_years if int(y) >= start_year and int(y) <= end_year]
    years = np.sort(years)
    ads_with_word = dict()
    ads_infos = dict()
    for y_i, year in enumerate(years):
        print year
        ads = glob.glob(basepath + str(year) + '/*/*/extracted/*adver*.txt')
        ads_with_word.update(get_word_counts(ads, word))
        print "counts", ads_with_word
        ads_infos.update(get_info_for_items(ads))
        print "infos", ads_infos

