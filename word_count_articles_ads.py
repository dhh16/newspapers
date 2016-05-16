#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os
import numpy as np
from matplotlib import pyplot as plt

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

if __name__ == "__main__":
    # ...
    word = sys.argv[1]
    start_year = 1880
    end_year = 1910
    print "Range", start_year, end_year
    all_years = os.listdir(basepath)
    years = [y for y in all_years if int(y) >= start_year and int(y) <= end_year]
    years = np.sort(years)
    yearly_articles = np.zeros(years.shape)
    articles_sum = 0
    yearly_ads = np.zeros(years.shape)
    ads_sum = 0
    for y_i, year in enumerate(years):
        articles = glob.glob(basepath + str(year) + '/*/*/extracted/*article*.txt')
        yearly_articles[y_i] = count_items_with_word(articles, word)
        articles_sum+=yearly_articles[y_i]
        ads = glob.glob(basepath + str(year) + '/*/*/extracted/*adver*.txt')
        yearly_ads[y_i] = count_items_with_word(ads, word)
        ads_sum+=yearly_ads[y_i]
    print "articles", articles_sum
    print "ads", ads_sum









