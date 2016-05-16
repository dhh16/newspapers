#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os
import numpy as np
# from matplotlib import pyplot as plt


def check_env():
    if os.uname()[1] == 'dhh':
        return "/srv/data/newspapers/newspapers/fin/"
    else:
        return "../testdata/fin/"


# local or production?
basepath = check_env()
output_file = "output.txt"
input_file = "input.txt"
if len(sys.argv) > 1:
    input_file = sys.argv[1]


def get_words_to_find(input_file):
    f = open(input_file, 'r')
    words_in_input = f.read().lower()
    # text1 = text2.lower()
    tokens = words_in_input.split()
    print "looking for: ", tokens
    return tokens


def count_articles_with_word(articles, word):
    count = 0
    for a in articles:
        with open(a, 'r') as f:
            text = f.read()
            text = text.lower()
            tokens = text.split()
            for t_i, token in enumerate(tokens):
                if token.startswith(word):
                    count += 1
    return count


start_year = 1880
end_year = 1885
print ("range", start_year, end_year)
all_years = os.listdir(basepath)
years = [y for y in all_years if int(y) >= start_year and int(y) <= end_year]
years = np.sort(years)
yearly_articles = np.zeros(years.shape)
articles_sum = 0
# yearly_ads = np.zeros(years.shape)
# ads_sum = 0


def year_hits_for_words(year, tokens):

    wordhits_dict = {}

    for word in tokens:
        articles = glob.glob(basepath + str(year) + '/*/*/extracted/*article*.txt')
        hits_for_word = count_articles_with_word(articles, word)
        wordhits_dict[word] = hits_for_word

    return wordhits_dict


tokens = get_words_to_find(input_file)


def get_yearhits_string(year, input_dict):

    output = year + "\n"

    for key in input_dict:
        output = (output +
                  key +
                  ": " + str(input_dict[key]) + "\n")

    return output


print "hits: "

for y_i, year in enumerate(years):
    yearhits = year_hits_for_words(year, tokens)
    yearhits_string = get_yearhits_string(year, yearhits)
    print yearhits_string

    out_f = open(output_file, 'w')
    out_f.write(yearhits_string)
    out_f.close()

# output = (str(year) +
#           "\n" + str(word) + "\t" +
#           " words: " + str(yearly_articles[y_i])[:-2] + "\n")
# output_file.write(output)
