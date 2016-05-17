#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy as np
import glob
import os
import re
import codecs
import pickle

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
        with codecs.open(input_line_file, 'r', encoding="utf-8") as f:
            rawlines = [l for l in f]
            lines = []
            dates = []
            for r in rawlines:
                if r and ''.join(r.split()):
                    print "input: ", r
                    dates.append(r[:10])
                    no_ws = ''.join(r[11:].split())
                    lines.append(no_ws)
    else:
        print "error, unknown number of command line args"
        sys.exit(1)
    start_year = 1870
    end_year = 1910
    print "range", start_year, end_year
    all_years = os.listdir(basepath)
    years = [y for y in all_years if int(y) >= start_year and int(y) <= end_year]
    years = np.sort(years)
    found_paths = dict()
    print len(lines)
    found_path_names = []
    for y_i, year in enumerate(years):
        print year
        elements = glob.glob(basepath + str(year) + '/*/*/extracted/*.txt')
        for text_element_path in elements:
            #print text_element_path
            pyear, iss, pdate, pnumber, pdate_number, pitem = get_info_for_item(text_element_path)
            for i, (date, line) in enumerate(zip(dates,lines)):
                if date == pdate:
                    with codecs.open(text_element_path, 'r', encoding="utf-8") as f:
                        text = f.read()
                        text = ''.join(text.split())
                        if line in text:
                            print i, date, pitem, text_element_path
                            if i not in found_paths:
                                found_paths[i] = dict()
                            found_paths[i][pitem] = text_element_path
                            found_path_names.append(text_element_path)
    with open("training_data_all_elements.txt", 'w') as tr_out:
        for l in found_path_names:
            tr_out.write(l+'\n')
    dobj = open("training_data_all_dict.p", "wb")
    pickle.dump(found_paths, dobj)
    dobj.close()




