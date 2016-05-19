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
        lines = lines[:30]
    data_words = []
    data_freqs = []
    for l in lines:
        word, freq = l.split(',')
        data_words.append(word)
        data_freqs.append(float(freq))
    inds = np.arange(0, len(data_words), 1)
    print len(data_words)
    print len(inds)
    width = 0.4
    fig, ax = plt.subplots()
    ax.bar(inds, data_freqs, width, color='g')
    ax.set_xticks(inds + 0.5*width)
    ax.set_title("Overrepresented words in 1. train data")
    ax.set_ylabel("q", rotation="horizontal")
    ax.set_xticklabels(data_words, rotation=-80)
    plt.subplots_adjust(bottom=0.30)
    #plt.show()
    fig.savefig("frequencies.pdf")
    fig.savefig("frequencies.png", dpi=300)
    fig.savefig("frequencies.svg")

