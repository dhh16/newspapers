#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy as np
import glob
import os
import re

basepath = "/srv/data/newspapers/newspapers/fin/"

rep = re.compile(r".*\/([0-9]*)\/(.*)\/.*_([0-9]*-[0-9]*-[0-9]*)_(.*)\/extracted\/(.*).txt")

def get_info_for_item(filename):
    """
    returns tuple (iss, year, date, number, date_number, item)
    """
    m = rep.match(filename)
    if m:
        year, iss, date, number, item = m.groups()
        date_number = date + "_" + number
        return year, iss, date, number, date_number, item
    else:
        return None

if __name__ == "__main__":
    # ...
    if len(sys.argv) == 2:
        input_line_file = sys.argv[1]
        with open(input_line_file, 'r') as f:
            rawlines = [rawline for line in f]
            lines = []
            dates = []
            for r in rawline:
                dates.append(r[:10])
                lines.append(r[11:])
    else:
        print "error, unknown number of command line args"
        sys.exit(1)
    start_year = 1880
    end_year = 1905
    print "range", start_year, end_year
    all_years = os.listdir(basepath)
    years = [y for y in all_years if int(y) >= start_year and int(y) <= end_year]
    years = np.sort(years)
    for y_i, year in enumerate(years):
        print year
        elements = glob.glob(basepath + str(year) + '/*/*/extracted/*.txt')
        for text_element_path in elements:
            print text_element_path
            with open(text_element_path, 'r') as f:
                text = f.read()
                pyear, piss, pdate, pnumber, pdate_number, pitem = get_info_for_item(text_element_path)
                for date, line in zip(dates,lines):
                    if date == pdate and line in text:
                        print "hit", date, text_element_path


