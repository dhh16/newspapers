#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import glob
import os
import numpy as np
from matplotlib import pyplot as plt

from get_training_data_paths import get_info_for_item

basepath = "/srv/data/newspapers/newspapers/fin/"

if __name__ == "__main__":
    machinereadable_file = sys.argv[1]

    with open(machinereadable_file, 'r') as f:
        tuples = [l.strip().split(',') for l in f if l.strip()]
    weights = np.array([float(t[1]) for t in tuples])
    plt.plot(weights, linewidth=2)
    plt.title("Test set: emigration coefficient of some articles")
    plt.ylabel("w", rotation="horizontal")
    plt.xlabel("random sample of 3000 random articles")
    plt.savefig("weights.pdf")










