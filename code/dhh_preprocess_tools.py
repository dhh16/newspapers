# -*- coding: utf-8 -*-

# python package: preprocess input files

import os
import codecs
import shutil
from get_training_data_paths import get_info_for_item

workdir = "./lemma_work/"

def workdir_check():
    if not os.path.isdir(workdir):
        os.mkdir(workdir)

def lemmatize_tmpfile(tempfilepath):
    """
    Shared lemmatization routines by _file and _str
    """
    pr = os.popen("/srv/bin/las lemmatize --locale fi --max-edit-distance 2 " + tempfilepath)
    pr.close()

    with codecs.open(tempfilepath+".lemmatized", 'r', encoding="utf-8") as f:
        contents = f.read()

    os.remove(tempfilepath)

    return contents

def lemmatized_contents_file(filepath):
    """
    Lemmatizes filepath with las and returns lemmatized contents as a string.
    """
    workdir_check()
    year, iss, date, number, date_number, item = get_info_for_item(filepath)
    tempfilepath = workdir+item+".txt"
    shutil.copy(filepath, tempfilepath)
    return lemmatize_tmpfile(tempfilepath)


def lemmatized_contents_str(string):
    workdir_check()
    tempfilepath = workdir + "tmp_lemma_str"
    with codecs.open(tempfilepath, 'w') as f:
        f.write(string)

    return lemmatize_tmpfile(tempfilepath)

def hfst_filter_words(wordlist, type):
    """
    type = VERB|AUX|etc
    """
    with codecs.oepn(workdir + "hfsttmp.txt") as f:
        for word in wordlist:
            f.write(word + '\n')
    pr = os.popen("")
    pr.close()
