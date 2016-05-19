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

def lemmatize_tmpfile_las(tempfilepath):
    """
    Shared lemmatization routines by _file and _str with las
    """
    pr = os.popen("/srv/bin/las lemmatize --locale fi --max-edit-distance 2 " + tempfilepath)
    pr.close()

    with codecs.open(tempfilepath+".lemmatized", 'r', encoding="utf-8") as f:
        contents = f.read()

    os.remove(tempfilepath)

    return contents

def lemmatized_contents_file_las(filepath):
    """
    Lemmatizes filepath with las and returns lemmatized contents as a string.
    """
    workdir_check()
    year, iss, date, number, date_number, item = get_info_for_item(filepath)
    tempfilepath = workdir+item+".txt"
    shutil.copy(filepath, tempfilepath)
    return lemmatize_tmpfile_las(tempfilepath)


def lemmatized_contents_str_las(string):
    workdir_check()
    tempfilepath = workdir + "tmp_lemma_las_str"
    with codecs.open(tempfilepath, 'w') as f:
        f.write(string)

    return lemmatize_tmpfile_las(tempfilepath)

def hfst_words(wordlist):
    """
    runs hfsts on wordlist

    returns list of unicode str
    """
    workdir_check()
    tempfilepath = workdir + "tmp_lemma_hfst_str"
    with codecs.open(tempfilepath, 'w') as f:
        for s in wordlist:
            f.write(s + '\n')
    pr = os.popen("cat " + tempfilepath + "| hfst-optimized-lookup /srv/bin/omorfi-omor.analyse.hfst")
    out = []
    found_words = set()
    for l in pr:
        lsplit = l.split()
        if not lsplit:
            continue
        w_o = lsplit[0]
        if w_o not in found_words:
            found_words.add(w_o)
            rest = lsplit[1]
            if rest:
                rsplit = rest.split(']')
                if rsplit[0] and rsplit[0][1:].startswith("WORD_ID"):
                    out.append(rsplit[0][9:].decode('utf8'))
    pr.close()
    return out
