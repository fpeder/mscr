#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import cPickle as pickle

from util import MyThreshold, get_dim, gray2rgb, imshow, MyMorph
from util import MyCC, MyKNN


class GridClassifier():

    def __init__(self, cls, grid):
        self._cls = cls
        self._grd = grid
        self._pred = []
        self._bb = []

    def run(self, img, vimg):
        self._img = img.copy()
        self._cls.fit(vimg)
        pts = self._grd.run(img)
        tmp = self._cls.predict(pts)
        prd = self._grd.toImage(tmp)
        self._pred = prd
        return prd

    def finalize(self):
        if len(self._pred) > 0:
            pred = MyMorph((self._grd.w, self._grd.h), 2).run(self._pred)
            cc = MyCC(self._cls.labels)
            cc.run(pred)
            self._bb = cc.get_bounding_box()

    def save(self, outfile):
        out = []
        for bbs, desc in zip(self._bb, ['txt', 'ms']):
            for bb in bbs:
                out.append([desc, bb])
        pickle.dump(out, open(outfile, 'w'))

    def show(self, lw=4):
        tmp = gray2rgb(self._img)
        colors = [(255, 0, 0), (0, 0, 255)]
        descr = ['text', 'music']
        for bbs, color, desc in zip(self._bb, colors, descr):
            for bb in bbs:
                cv2.rectangle(tmp, bb[0], bb[1], color, lw)
                pt = (bb[0][0]+32, bb[0][1]+48)
                cv2.putText(tmp, desc, pt, cv2.FONT_HERSHEY_PLAIN, 3, color, 8)
        return tmp


class Grid():
    COLORS = ((0, 0, 255), (255, 0, 0), (0, 0, 0), ())
    R = 4

    def __init__(self, dim, mep=10, r=4):
        self._w, self._h = dim
        self._mep = mep
        self._pts = []
        self._img = []

    def run(self, img):
        self._img = img.copy()
        M, N = get_dim(img)
        tmp = MyThreshold(val=1, ksize=0).run(img)

        def enough_elem(x):
            return x.sum()/(self._w * self._h)*100 > self._mep

        pts = [(y, x)
               for y in np.arange(0, M - self._w, self._w)
               for x in np.arange(0, N - self._h, self._h)
               if enough_elem(tmp[y:y+self._h, x:x+self._w])]
        self._pts = pts
        return pts

    def toImage(self, pred):
        out = -1 * np.ones(self._img.shape[:2], np.int32)
        for pt, p in zip(self._pts, pred):
            y, x = pt
            out[y:y+self._w, x:x+self._h] = p
        return out

    def show(self, pred=[]):
        tmp = gray2rgb(self._img)
        if len(pred) > 0:
            for pt, p in zip(self._pts, pred):
                color = self.COLORS[p]
                cv2.circle(tmp, (pt[1], pt[0]), self.R, color, -1)
        else:
            for pt in self._pts:
                cv2.circle(tmp, (pt[1], pt[0]), self.R, self.COLORS[1], -1)
        imshow(tmp)

    @property
    def w(self):
        return self._w

    @property
    def h(self):
        return self._h


if __name__ == '__main__':
    from util import load_gray, Crop
    from blockVote import Votes2Img

    img = load_gray('test/test4.jpg')
    img = Crop().run(img)

    votes = pickle.load(open('votes.pck', 'rb'))
    vimg = Votes2Img(img.shape[:2]).run(votes)

    knn = MyKNN({'ms': 1, 'txt': 0}, nn=50)
    grid = Grid((16, 16))

    gcls = GridClassifier(knn, grid)
    gcls.run(img, vimg)
    gcls.finalize()
    gcls.show()
