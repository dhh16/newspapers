#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import codecs
from matplotlib import pyplot as plt

if __name__ == "__main__":
    file = sys.argv[1]
    with codecs.open(file, 'r', encoding='utf-8') as f:
        lines = [l for l in f]
        lines = lines[:10]
    data_words = []
    data_freqs = []
    for l in lines:
        word, freq = l.split(',')
        data_words.append(word)
        data_freqs.append(float(freq))
    inds = np.arange(len(data_words))
    width = 0.6
    fig, ax = plt.subplots()
    ax.bar(inds, data_freqs, width, color='g')
    ax.set_xticks(inds + 0.5*width)
    ax.set_ylabel("freq")
    ax.set_xticklabels(data_words, rotation=-75)
    plt.subplots_adjust(bottom=0.30)
    #plt.show()
    fig.savefig("frequencies.pdf")
    fig.savefig("frequencies.png")

