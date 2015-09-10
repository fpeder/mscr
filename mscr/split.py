#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np

from util import load_gray
from util import imshow


class Elem(object):

    def __init__(self, img, box, spcount, cls=-1):
        self._img = img
        self._box = box
        self._cls = cls
        self._prob = None
        self._sc = spcount

    @property
    def img(self):
        return self._img

    @property
    def box(self):
        return self._box

    @property
    def sc(self):
        return self._sc

    @property
    def cls(self):
        return self._cls

    @cls.setter
    def cls(self, val):
        self._cls = val

    @property
    def prob(self):
        return self._prob

    @prob.setter
    def prob(self, val):
        if val is not None:
            self._prob = val


class RandomSplitPredicate():

    def __init__(self, p=.6):
        self._p = p

    def run(self, elem):
        p = self._p / (elem.sc + 1)**0.5
        return np.random.randn() >= (1-p)


class SplitPredicate():

    def __init__(self, pred, thmax=0.85, thmin=0.5, alpha=2):
        self._pred = pred
        self._thmax = thmax
        self._thmin = thmin
        self._alpha = alpha

    def run(self, elem):
        pred, prob = self._pred.predict(elem.img)
        need_split = False
        if pred == -1:
            elem.cls = pred
            elem.prob = 1
        else:
            prob = prob[0][pred]
            elem.prob = prob
            if prob >= self.__comp_thresh(elem.sc):
                elem.cls = pred
                elem.prob = prob
            else:
                need_split = True
        return need_split

    def __comp_thresh(self, sc):
        D = self._thmax - self._thmin
        y = D * np.exp(-1 * self._alpha * sc) + self._thmin
        return y


class DoSplit(object):

    def __init__(self):
        self._count = 0

    def run(self, elem):
        img, offset, sc = elem.img, elem.box[0], elem.sc
        M, N = img.shape[:2]
        blocks, i = [], 0
        for c1 in range(2):
            j = 0
            for c2 in range(2):
                timg = img[i:i+M/2, j:j+N/2]
                box = ((offset[0] + i, offset[1] + j),
                       (offset[0] + i + M/2, offset[1] + j + N/2))
                blocks.append(Elem(timg, box, sc+1))
                j += N/2
            i += M/2
        self._count += 1
        return blocks

    @property
    def count(self):
        return self._count


class Split(object):

    def __init__(self, predicate, msizeratio=4):
        self._splitter = DoSplit()
        self._splitpred = predicate
        self._msr = msizeratio
        self._img = []
        self._blocks = []
        self._min_size = []

    def run(self, img):
        self._img = img
        self._min_size = (img.shape[0]/self._msr, img.shape[1]/self._msr)
        elem = Elem(img, ((0, 0), img.shape[:2]), 0)
        processlist = [elem]
        regionlist = []
        while processlist:
            elem = processlist.pop()
            if not self._splitpred.run(elem):
                regionlist.append(elem)
            elif self.__min_size(elem):
                regionlist.append(elem)
            else:
                processlist += self._splitter.run(elem)
        self._blocks = regionlist
        return self._blocks

    def __min_size(self, x):
        M, N = x.img.shape[:2]
        return M <= self._min_size[0] and N <= self._min_size[1]

    def show(self, lw=4, off=16):
        colors = ((0, 255, 0), (255, 0, 0), (0, 0, 0), ())
        tmp = cv2.cvtColor(self._img, cv2.COLOR_GRAY2RGB)
        for bl in self._blocks:
            pred, prob = bl.cls, bl.prob
            p1, p2 = bl.box[0], (bl.box[1][0] - lw, bl.box[1][1] - lw)
            cv2.putText(tmp, str(prob), (p1[1] + off, p1[0] + int(2.5*off)),
                        cv2.FONT_HERSHEY_PLAIN, 2, colors[pred], 2)
            cv2.rectangle(tmp, p1[::-1], p2[::-1], colors[pred], lw)
        imshow(tmp)


if __name__ == '__main__':
    from util import Crop

    img = load_gray('test/test4.jpg')
    crop = Crop()
    img = crop.run(img)
    split = Split(RandomSplitPredicate())
    split.run(img)
    split.show()
