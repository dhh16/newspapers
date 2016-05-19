#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os
import numpy as np

from get_training_data_paths import get_info_for_item

def n_elements_by_newspaper(years, newspaper, element):
    """TODO: Docstring for number_elements_newspaper.
    """
    nums = np.zeros(years.shape)
    for y_i, year in enumerate(years):
        print year
        items = glob.glob(basepath + str(year) + '/' + newspaper + '/*/extracted/*' + element + '*.txt')
        nums[y_i] = len(items)
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
        if iss not in newspapers_yearly_migr_elems:
            if not papers or (papers and iss in papers):
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
    years = [y for y in all_years if int(y) >= start_year and int(y) <= end_year]
    years = np.sort(years)

    element = 'article'
    sum_all_articles = n_elements_by_newspaper(year, *, element)
    # similarly for each specific newspaper

    with open(migration_element_paths_file, 'r') as f:
        migr_paths = [l.strip() for l in f]

    info_all_data_papers = frequencies_newspapers(migr_paths, years)
    freqs = info_all_data_papers[2]
    for iss in freqs:
        print iss + "\n"
        for i in np.arange(len(freqs[iss])):
            print years[i], freqs[iss][i]
    #freqs_certain_paper = frequencies_newspapers(migr_paths, years, 'code')











