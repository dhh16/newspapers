#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import random
import numpy as np
import glob
import codecs

basepath = "/srv/data/newspapers/newspapers/fin/"

# pick random articles/adverts/etc (in some time range, uniformly from the whole corpora)
# first parameter: number
# second parameter: substring in the filename (e.g. article, page, advert)
# prints line by line to stdout


if __name__ == "__main__":
    n = sys.argv[1]
    substr = sys.argv[2]

    rep = re.compile(r".*\/[0-9]*\/.*\/.*_[0-9]*-[0-9]*-[0-9]*_.*\/extracted\/.*" + substr + ".*.txt")

    start_year = 1870
    end_year = 1910
    print "range", start_year, end_year
    all_years = os.listdir(basepath)
    years = [y for y in all_years if int(y) >= start_year and int(y) <= end_year]
    years = np.sort(years)
    found_path_names = []
    corpora_match_subset = []
    for y_i, year in enumerate(years):
        all_in_year = glob.glob(basepath + str(year) +'/*/*/extracted/*.txt')
        for path in all_in_year:
            m = rep.match(path)
            if m:
                corpora_match_subset.append(path)
    random_sample = random.sample(corpora_match_subset, n)
    for r in random_sample:
        print r



