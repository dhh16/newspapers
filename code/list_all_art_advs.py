#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import numpy as np
import glob
import codecs

if __name__ == "__main__":

    # pipe all filenames to file
    for year in xrange(1870, 1910):
        pr = os.popen("find /srv/data/newspapers/newspapers/fin/" + str(year) +" /* -name '*article*.txt' > random_sample_gigantic_art.txt")
        pr.close()
        pr = os.popen("find /srv/data/newspapers/newspapers/fin/" + str(year) +" /* -name '*adv*.txt' > random_sample_gigantic_adv.txt")
        pr.close()






