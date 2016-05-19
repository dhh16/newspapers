#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os
import numpy as np

from get_training_data_paths import get_info_for_item

basepath = "/srv/data/newspapers/newspapers/fin/"

def n_elements_by_newspaper(years, newspaper, element):
    """TODO: Docstring for number_elements_newspaper.
    """
    nums = np.zeros(years.shape)
    for y_i, year in enumerate(years):
        pr = os.popen('find ' + basepath + str(year) + '/' + newspaper + '/* -name ' + "'*" + element + "*.txt' | wc -l")
        n = long(pr.read().strip())
        pr.close()
        nums[y_i] = n
    return nums

def frequencies_newspapers(migr_paths, years, element, papers=None):
    """
    element: e.g. "article"
    papers: select only these papers (iterable)
    """
    newspapers_yearly_all_elems = {}
    newspapers_yearly_migr_elems = {}
    newspapers_yearly_migr_freq = {}
    for path in migr_paths:
        year, iss, date, number, date_number, item = get_info_for_item(path)
        year = int(year)
        if year not in years:
            continue
        if papers and iss not in papers:
            continue
        if iss not in newspapers_yearly_migr_elems:
            newspapers_yearly_migr_elems[iss] = np.zeros(years.shape)
        newspapers_yearly_migr_elems[iss][year-start_year] += 1

    for iss in newspapers_yearly_migr_elems:
        n_years = n_elements_by_newspaper(years, iss, element)
        newspapers_yearly_all_elems[iss] = n_years
        newspapers_yearly_migr_freq[iss] = newspapers_yearly_migr_elems[iss]/n_years
    return newspapers_yearly_all_elems, newspapers_yearly_migr_elems, newspapers_yearly_migr_freq

if __name__ == "__main__":
    migration_element_paths_file = sys.argv[1]

    start_year = 1870
    end_year = 1910
    print "range", start_year, end_year
    all_years = os.listdir(basepath)
    years = [int(y) for y in all_years if int(y) >= start_year and int(y) <= end_year]
    years = np.sort(years)

    element = 'article'
    #sum_all_articles = n_elements_by_newspaper(year, *, element)
    # similarly for each specific newspaper

    with open(migration_element_paths_file, 'r') as f:
        migr_paths = [l.strip() for l in f]

    #info_all_data_papers = frequencies_newspapers(migr_paths, years, element)
    #freqs = info_all_data_papers[2]
    nuor = ['0355-2047','1458-2619','1458-8595','0356-1356']
    vanha = ['1457-4721','0355-6913','1458-090X','1458-0535','1458-0543']
    freqs_certain_paper = frequencies_newspapers(migr_paths, years, element, nuor)
    freqs = freqs_certain_paper[2]

    for iss in freqs:
        print iss, len(freqs[iss])
        for i in xrange(len(freqs[iss])):
            print years[i], freqs[iss][i]










