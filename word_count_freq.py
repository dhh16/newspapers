#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os
import numpy as np
#from matplotlib import pyplot as plt

# count articles / adcles", articles_sumt that have some particular word

basepath = "/srv/data/newspapers/newspapers/fin/"
#basepath = "testdata/fin/"
output_file =open("output","a")

file1 = sys.argv[1]
#fileptr = open(file1,"r")

#tokens1="stre"

f= open(file1, 'r')
text2 = f.read()
text1 = text2.lower()
tokens1 = text1.split()
print(tokens1)


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

    return cnt


start_year = 1880
end_year = 1885
print "range", start_year, end_year
all_years = os.listdir(basepath)
years = [y for y in all_years if int(y) >= start_year and int(y) <= end_year]
years = np.sort(years)
yearly_articles = np.zeros(years.shape)
articles_sum = 0
yearly_ads = np.zeros(years.shape)
ads_sum = 0


def year_hits(year, tokens1):
   for word in tokens1:
        articles = glob.glob(basepath + str(year) + '/*/*/extracted/*article*.txt')
        yearly_articles[y_i] = count_items_with_word(articles, word)
        articles_sum+=yearly_articles[y_i]
        print "articles", yearly_articles[y_i]
        output = (str(year) +
                 "\n" +  str(word) +"\t" +
                 " words: " + str(yearly_articles[y_i])[:-2] + "\n")
        output_file.write(output)
	        print "articles", articles_sum


#if __name__ == "__main__":
    # ...
"""
start_year = 1880
end_year = 1885
print "range", start_year, end_year
all_years = os.listdir(basepath)
years = [y for y in all_years if int(y) >= start_year and int(y) <= end_year]
years = np.sort(years)
yearly_articles = np.zeros(years.shape)
articles_sum = 0
yearly_ads = np.zeros(years.shape)
ads_sum = 0
"""
for y_i, year in enumerate(years):
    print year
    year_hits(year, tokens1)
"""for word in tokens1:
        articles = glob.glob(basepath + str(year) + '/*/*/extracted/*article*.txt')
        yearly_articles[y_i] = count_items_with_word(articles, word)
        articles_sum+=yearly_articles[y_i]
        print "articles", yearly_articles[y_i]
        output = (str(year) +  
                 "\n" +  str(word) +"\t" + 
                 " words: " + str(yearly_articles[y_i])[:-2] + "\n")
        output_file.write(output)
 
        print "articles", articles_sum
"""


