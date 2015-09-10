#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: peval.py <imgdir> <gtdir> <outdir> <ext>

Options:
   -h --help  Show this message
"""

import os
import numpy as np
import cPickle as pickle

from glob import glob
from cv2 import imread
from mscr.util import AddSuffix


class PevalAll():

    def __init__(self, imgdir, gtdir, outdir, ext='jpg'):
        self._imgdir = imgdir
        self._ext = ext
        self._gtdir = gtdir
        self._outdir = outdir

    def run(self):
        res = []
        count = 1
        for imgf in sorted(
                glob(os.path.join(self._imgdir, '*.' + self._ext))):
            print '#--------------------------'
            print imgf

            bn = os.path.basename(imgf)
            gt = os.path.join(
                self._gtdir, AddSuffix('gt', 'pck').run(bn))
            out = os.path.join(
                self._outdir, AddSuffix('out', 'pck').run(bn))

            tmp = Peval(imread(imgf), gt, out).run()
            res += tmp
            for x in tmp:
                print count, x[0], x[1], x[2]

            count += 1

        #for lab in ['txt', 'ms']:
        #    tmp = np.array([x[1:] for x in res if x[0] == lab]).mean(axis=0)
        #    pre, rec = tmp
        #    fsc = 2*pre*rec/(pre + rec) if pre != 0 and rec != 0 else 0
        #    print '# %s %f %f %f' % lab, pre, rec, fsc


class Peval():

    def __init__(self, img, gt, out):
        self._gt = pickle.load(open(gt, 'r'))
        self._out = pickle.load(open(out, 'r'))
        self._img = img
        self._size = img.shape[:2]

    def run(self):
        res = []
        cls = list(set([x[0] for x in self._gt]))

        for lab in cls:
            gt = self.__bb2img(self._gt, lab)
            out = self.__bb2img(self._out, lab)
            inter = np.logical_and(gt, out)
            if out.sum() == 0:
                pre = 0
                rec = 0
            else:
                pre = float(inter.sum())/out.sum()
                rec = float(inter.sum())/gt.sum()
            tmp = [lab, pre, rec]
            res.append(tmp)
        return res

    def __bb2img(self, bb, lab):
        img = np.zeros(self._size, np.uint8)
        tmp = [x for x in bb if x[0] == lab]
        for x in tmp:
            xs, ys = x[1][0]
            xe, ye = x[1][1]
            img[ys:ye, xs:xe] = 1
        return img


if __name__ == '__main__':
    from docopt import docopt

    args = docopt(__doc__)
    imgdir = args['<imgdir>']
    outdir = args['<outdir>']
    gtdir = args['<gtdir>']
    ext = args['<ext>']

    res = PevalAll(imgdir, gtdir, outdir, ext).run()
