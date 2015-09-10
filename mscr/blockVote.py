#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import ctypes as ct
import numpy.ctypeslib as npct
import cPickle as pickle

from util import load_gray, imshow
from util import gray2rgb, rgb2gray
from util import MyCC
from bovw import BoVW
from blocks import RandBlockIter


class Vote():

    def __init__(self, predictor, th=0.65):
        self._pr = predictor
        self._th = th

    def run(self, img):
        pred, prob = self._pr.predict(img)
        valid = True
        if pred == -1:
            prob = 1
        else:
            prob = prob[0][pred]
            if prob <= self._th:
                valid = False
        return valid, pred, prob,


class BlockVote():

    def __init__(self, voter, block_iter):
        self._voter = voter
        self._iter = block_iter

    def run(self, img):
        self._img = gray2rgb(img)
        votes = []
        for x, box in self._iter.run(img):
            valid, p, prob = self._voter.run(x)
            if valid:
                votes.append({'pred': p, 'prob': prob, 'box': box})
        self._votes = votes
        return votes

    def show(self):
        drawer = DrawVote(self._img)
        for v in self._votes:
            pred = v['pred']
            prob = v['prob']
            box = v['box']
            drawer.run(box, pred, prob)
        drawer.show()


class Votes2Img():
    LIB = 'findmax'

    def __init__(self, dim):
        self._h, self._w = dim
        self._lib = npct.load_library(self.LIB, 'mscr/clib')
        self._coarse = None
        self._bb = None
        self._ncls = 2

    def run(self, votes):
        #self._ncls = self.__get_nclass(votes)
        counts = np.zeros((self._h, self._w, self._ncls), np.int32)
        for v in votes:
            pred = int(v['pred'])
            y, x, h, w = v['box']
            counts[y:y+h, x:x+w, pred] += int(v['prob'] * 100)
        return self.__merge(counts)

    def get_bounding_box(self):
        cc = MyCC([0, 1])
        cc.run(self._coarse)
        bb = cc.get_bounding_box()
        self._bb = bb
        return bb

    def save_bb(self, outfile):
        out = []
        for bbs, desc in zip(self._bb, ['txt', 'ms']):
            for bb in bbs:
                out.append([desc, bb])
        pickle.dump(out, open(outfile, 'w'))

    def __merge(self, counts):
        tmp = counts.reshape(-1, self._ncls)
        idx = np.zeros((tmp.shape[0]), np.int32)
        myptr = ct.POINTER(ct.c_int)
        self._lib.findmax.argtypes = [myptr, ct.c_int, ct.c_int, myptr]
        self._lib.findmax.restype = ct.c_int
        self._lib.findmax(tmp.ctypes.data_as(myptr),
                          tmp.shape[0], tmp.shape[1],
                          idx.ctypes.data_as(myptr))
        idx = idx.reshape(self._h, self._w)
        self._coarse = idx
        return idx

    def __get_nclass(self, votes):
        return len(np.unique([int(x['pred']) for x in votes]))


class DrawVote():

    def __init__(self, img, colors=((0, 0, 255), (255, 0, 0), (0, 0, 0), ()),
                 r=8, lw=2, off=16):
        self._colors = colors
        self._lw = lw
        self._off = off
        self._r = r
        self._lw = lw
        self._off = off
        self._img = gray2rgb(img) if len(img.shape) == 1 else img
        self._tmp = self._img.copy()

    def run(self, box, pred=None, prob=None):
        y, x, h, w = box
        p1 = (x, y)
        p2 = (x+w, y+h)
        color = self._colors[pred] if pred is not None else (255, 0, 0)
        if prob is not None:
            cv2.putText(self._tmp, str(prob),
                        (p1[0] + self._off, p1[1] + int(2.5 * self._off)),
                        cv2.FONT_HERSHEY_PLAIN, 1, color, 2)
        cv2.circle(self._tmp, p1, self._r, color, -1)
        cv2.rectangle(self._tmp, p1, p2, color, self._lw)

    def show(self):
        imshow(self._tmp)

    def clear(self):
        self._tmp = self._img.copy()


if __name__ == '__main__':
    from util import Crop
    from knn import MyKNN

    img = load_gray('test/test5.jpg')
    img = Crop().run(img)

    bbb = BoVW()
    bbb.load('data/randext.model.64.pck')

    rbv = BlockVote(Vote(bbb), RandBlockIter(50))
    votes = rbv.run(img)

    asd = Votes2Img(img.shape[:2])
    vimg = asd.run(votes)

    knn = MyKNN({'txt': 0, 'ms': 1})
    knn.fit(img, vimg)
