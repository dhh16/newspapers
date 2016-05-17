#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    # ...
    if len(sys.argv) == 2:
        input_line_file = sys.argv[1]
        with open(input_words_file, 'r') as f:
            lines = [line for line in f]
    else:
        print "error, unknown number of command line args"
        sys.exit(1)
    start_year = 1880
    end_year = 1905
    print "range", start_year, end_year
    all_years = os.listdir(basepath)
    years = [y for y in all_years if int(y) >= start_year and int(y) <= end_year]
    years = np.sort(years)
    for line in lines:
        for y_i, year in enumerate(years):
            print year
            elements = glob.glob(basepath + str(year) + '/*/*/extracted/*.txt')
            for text_element_path in elements:
                with open(text_element_path, 'r') as f:
                    text = f.read()
                    if line in text:
                        print text_element_path


