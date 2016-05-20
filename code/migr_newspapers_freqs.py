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

def amount_newspapers_yearly(migr_paths, years, element, papers=None):
    newspapers_yearly_migr_elems = {}
    print "amount_yearly"
    for path in migr_paths:
        year, iss, date, number, date_number, item = get_info_for_item(path)
        year = int(year)
        print iss, year
        if year not in years:
            continue
        if papers and iss not in papers:
            continue
        if iss not in newspapers_yearly_migr_elems:
            newspapers_yearly_migr_elems[iss] = np.zeros(years.shape)
        newspapers_yearly_migr_elems[iss][year-start_year] += 1
    return newspapers_yearly_migr_elems

def frequencies_newspapers_whole(migr_paths, years, element, papers=None):
    """
    Relative frequencies against whole data set.
    element: e.g. "article"
    papers: select only these papers (iterable)
    """
    n_mig =amount_newspapers_yearly(migr_paths, years, element, papers)
    newspapers_yearly_migr_elems = n_mig
    newspapers_yearly_all_elems = {}
    newspapers_yearly_migr_freq = {}

    for iss in newspapers_yearly_migr_elems:
        n_years = n_elements_by_newspaper(years, iss, element)
        newspapers_yearly_all_elems[iss] = n_years
        newspapers_yearly_migr_freq[iss] = newspapers_yearly_migr_elems[iss]/n_years
    return newspapers_yearly_all_elems, newspapers_yearly_migr_elems, newspapers_yearly_migr_freq


def frequencies_newspapers_sample(migr_paths, sample_paths, years, element, papers=None):
    """
    Relative frequencies against sample data set.
    element: e.g. "article"
    papers: select only these papers (iterable)
    """
    print "n migr", len(migr_paths)
    print "n sample", len(sample_paths)
    n_mig =amount_newspapers_yearly(migr_paths, years, element, papers)
    newspapers_yearly_migr_elems = n_mig
    newspapers_yearly_all_elems = {}
    newspapers_yearly_migr_freq = {}

    for iss in newspapers_yearly_migr_elems:
        n_all = amount_newspapers_yearly(sample_paths, years, element, papers)
        newspapers_yearly_all_elems[iss] = n_all
        newspapers_yearly_migr_freq[iss] = newspapers_yearly_migr_elems[iss]/n_all[iss]
    return newspapers_yearly_all_elems, newspapers_yearly_migr_elems, newspapers_yearly_migr_freq

if __name__ == "__main__":
    migration_element_paths_file = sys.argv[1]
    sample_paths_file = sys.argv[2]

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

    with open(sample_paths_file, 'r') as f:
        sample_paths = [l.strip() for l in f]

    #info_all_data_papers = frequencies_newspapers_whole(migr_paths, years, element)
    #freqs = info_all_data_papers[2]
    #freqs_certain_paper = frequencies_newspapers_whole(migr_paths, years, element, nuor)
    #freqs = freqs_certain_paper[2]
    nuor = ['0355-2047','1458-2619','1458-8595','0356-1356']
    vanha = ['1457-4721','0355-6913','1458-090X','1458-0535','1458-0543']

    freq_all = frequencies_newspapers_sample(migr_paths, sample_paths, years, element)
    freqs = freq_all[2]

    total_migr = np.zeros(years.shape)
    total_all  = np.zeros(years.shape)
    for iss in freqs:
        print iss, len(freqs[iss])
        for i in xrange(len(freqs[iss])):
            print years[i], freqs[iss][i]
            total_all[i] += freq_all[0][iss][i]
            total_migr[i] += freq_all[1][iss][i]

        data = np.column_stack([years, freqs[iss]])
        np.savetxt("migr" + iss + ".csv", data, delimiter=",")
    final_freqs = total_migr/total_all
    np.savetxt("migr_total_freqs.csv",final_freqs,delimiter=",")
    np.savetxt("migr_total_all.csv",total_all,delimiter=",")
    np.savetxt("migr_total_migr.csv",total_migr,delimiter=",")










