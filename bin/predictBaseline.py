#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: predict_baseline.py <img> [-s]

Options:
    -h --help    Show This message
    -s           dump stuff

"""

import cv2
import numpy as np
import cPickle as pickle
import pylab as plt

from mscr.util import gray2rgb, AddSuffix
from gamera.core import *
from gamera.toolkits.musicstaves import musicstaves_rl_simple


class MusicStaff():
    X_THR = 0.05
    LAB = 'ms'
    SUBFIX = '.out'

    def __init__(self, imgf):
        init_gamera()
        self._infile = imgf
        self._img = load_image(imgf)
        self._y = []
        self._bb = []

    def run(self):

        print "-----------------------"
        print self._infile
        
        self.__get_lines()
        ym = self.__ymargin()
        xm = self.__xmargin()
        self.__boxes(ym, xm)

    def __boxes(self, ym, xm):
        bb = [[self.LAB, [(xm[0], y[0]), (xm[1], y[1])]] for y in ym]
        self._bb = bb
        return bb

    def __get_lines(self):
        img = self._img.to_onebit()
        ms = musicstaves_rl_simple.MusicStaves_rl_simple(img)
        ms.remove_staves()
        staves = ms.get_staffpos()
        for staff in staves:
            self._y += staff.yposlist
        self._y = np.array(self._y)
        return self._y

    def __ymargin(self):
        y = self._y
        diff = (y[1:] - y[:-1]).astype(np.float)
        norm = (diff - diff.min())/(diff.max() - diff.min())
        qwe = norm > norm.mean() + norm.std()
        qwe = np.hstack((qwe, True))
        bb = []
        start = 0
        i = 1
        while i < len(qwe):
            if qwe[i]:
                if qwe[i-1]:
                    box = [y[start], y[start]]
                else:
                    box = [y[start], y[i]]
                    bb.append(box)
                start = i+1
            i += 1
        return bb

    def __xmargin(self):
        tmp = self._img.to_onebit().to_numpy()
        x = tmp.sum(axis=0)/float(tmp.shape[0]) > self.X_THR
        qwe = np.where(x)[0]
        xm = [qwe.min(), qwe.max()]
        return xm

    def save(self):
        assert self._bb, "no bounding boxes"
        outfile = AddSuffix('out', 'pck').run(self._infile)
        pickle.dump(self._bb, open(outfile, 'wb'))

    def show_lines(self):
        tmp = self._img.to_numpy()
        s, e = 0, tmp.shape[1]
        for y in self._y:
            cv2.line(tmp, (s, y), (e, y), (255, 0, 0))

        #plt.subplot(121)
        #plt.imshow(tmp)
        #plt.show()

    def show_box(self):
        tmp = self._img.to_numpy()
        for box in self._bb:
            cv2.rectangle(tmp, box[1][0], box[1][1], (255, 0, 0), 4)
        #plt.subplot(122)
        #plt.imshow(tmp)
        #plt.show()
        return tmp


if __name__ == '__main__':
    from docopt import docopt

    args = docopt(__doc__)
    imgf = args['<img>']

    ms = MusicStaff(imgf)
    ms.run()

    if args['-s']:
        img = ms.show_box()
        cv2.imwrite(imgf + '.out.jpg', img)
        ms.save()
