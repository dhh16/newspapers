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
    file = sys.argv[2]
    with codecs.open(file, 'r', encoding="utf-8") as f:
        paths = [l for l in f]
    random_sample = random.sample(paths, n)
    for r in random_sample:
        print r



