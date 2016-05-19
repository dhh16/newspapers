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

def hfst_words(wordlist, filter=None):
    """
    runs hfsts on wordlist and filters

    filter = list or tuple of (VERB, NOUN, etc)
    inclusive: returns only words of type listed in filter

    returns list of unicode str
    """
    workdir_check()
    tempfilepath = workdir + "tmp_lemma_hfst_str"
    with codecs.open(tempfilepath, 'w') as f:
        for s in wordlist:
            f.write(unicode(s + '\n').encode('utf8'))
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
                    lemma = rsplit[0][9:].decode('utf8')
                    if filter and rsplit[1] and rsplit[1][1:].startswith("UPO"):
                        if rsplit[1][6:] in filter:
                            out.append(lemma)
                    else:
                        out.append(lemma)
    pr.close()
    return out
