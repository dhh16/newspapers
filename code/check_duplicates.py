#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

if __name__ == "__main__":
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    with open(f1, 'r') as file1:
        with open(f2, 'r') as file2:
            same = set(file1).intersection(file2)
    print "duplicate lines", len(same)
