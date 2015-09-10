#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cv2
import os
import pylab as plt
import numpy as np

from glob import glob

from progressbar import ProgressBar, Percentage, Bar
from sklearn.neighbors import KNeighborsClassifier


def rgb2gray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def gray2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)


def gray2bgr(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


def rgb2bgr(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


def load_gray(infile):
    if not os.path.exists(infile):
        sys.exit('err: img file %s doesn\'t exists', infile)
    img = cv2.imread(infile, 0)
    return img


def get_dim(img):
    return img.shape[:2]


def imshow(img):
    plt.imshow(img)
    plt.show()


class MyCC():

    def __init__(self, labels, min_elem=10000, remove_small=True):
        self._labs = labels
        self._me = min_elem
        self._rs = remove_small
        self._cc = []

    def run(self, img):
        H, W = img.shape[:2]
        out = []
        for lab in self._labs:
            tmp = np.zeros((H, W), np.int32)
            tmp[img == lab] = -1
            ccount = 1
            while True:
                pt = self.__find_seed(tmp)
                if not pt:
                    break
                cv2.floodFill(tmp, None, pt, ccount)
                ccount += 1
            if self._rs:
                tmp = self.__remove_small(tmp)
            out.append(tmp.copy())
        self._cc = out
        return out

    def get_bounding_box(self):
        allbb = []
        for comp in self._cc:
            bb = []
            for lab in np.unique(comp)[1:]:
                x, y = np.where(comp == lab)
                tmp = [(y.min(), x.min()), (y.max(), x.max())]
                bb.append(tmp)
            allbb.append(bb)
        return allbb

    def __remove_small(self, img):
        for lab in np.unique(img)[1:]:
            cc = img == lab
            if cc.sum() < self._me:
                img[cc] = 0
        return img

    def __find_seed(self, img, l=-1):
        pt = ()
        tmp = np.where(img == l)
        if len(tmp[0]) > 0 and len(tmp[1]) > 0:
            pt = (tmp[1][0], tmp[0][0])
        return pt


class MyKNN():

    def __init__(self, cls, nn=25, skip=4):
        self._cls = cls
        self._skip = skip
        self._clf = KNeighborsClassifier(n_neighbors=nn)

    def fit(self, img):
        X, y = self.__get_data(img)
        self._clf.fit(X, y)

    def predict(self, X):
        p = self._clf.predict(X)
        return p

    def __get_data(self, img):
        X, y = [], []
        for k, v in self._cls.iteritems():
            tmp = np.where(img == v)
            tx = np.vstack((tmp[0], tmp[1])).T
            tx = tx[::self._skip, :]
            ty = v * np.ones(tx.shape[0], np.uint8)
            X = np.vstack((X, tx)) if len(X) > 0 else tx
            y = np.hstack((y, ty)) if len(y) > 0 else ty
        return X, y

    @property
    def labels(self):
        return self._cls.values()


class MyMorph():

    def __init__(self, size, niter, elem=cv2.MORPH_RECT):
        self._size = size
        self._niter = niter
        self._elem = elem

    def run(self, img):
        strel = cv2.getStructuringElement(cv2.MORPH_RECT, self._size)
        img = cv2.morphologyEx(img.astype(np.float32), cv2.MORPH_CLOSE,
                               strel, None, None, self._niter)
        return img


class AddSuffix():

    def __init__(self, sub, ext, sep='.'):
        self._sub = sub
        self._ext = ext
        self._sep = sep

    def run(self, path):
        folder, name = os.path.split(path)
        tmp = self._sep.join(name.split(self._sep)[:-1])
        name = tmp + self._sep + self._sub + self._sep + self._ext
        out = os.path.join(folder, name) if folder else name
        return out


class ImgFileIter(object):

    def __init__(self, src, msg='', ext='.jpg', crop=False):
        self._src = src
        self._msg = msg
        self._ext = ext
        self._crop = crop

    def run(self):
        self.__chek_path([self._src])
        filz = glob(os.path.join(self._src, '*' + self._ext))
        pbar = MyProgressBar(len(filz), self._msg)
        for x in filz:
            img = cv2.imread(x)
            if self._crop:
                img = self._crop.run(img)
            pbar.update()
            yield img
        pbar.finish()

    def __chek_path(self, path):
        for x in path:
            if not os.path.exists(x):
                sys.exit('err: %s doesn\'t exists' % x)


class MyProgressBar(object):

    def __init__(self, num, msg=''):
        self._count = 0
        self._pb = ProgressBar(
            widgets=[msg, ':', Percentage(), ' ', Bar()],
            maxval=num).start()

    def update(self):
        self._pb.update(self._count)
        self._count += 1

    def finish(self):
        self._pb.finish()


class Crop(object):

    def __init__(self, ksize=5,
                 crit=cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU):
        self._ksize = ksize
        self._box = []
        self._thr = MyThreshold(ksize=ksize, crit=crit)

    def run(self, img):
        tmp = rgb2gray(img) if len(img.shape) == 3 else img
        tmp = self._thr.run(tmp)
        y, x = np.where(tmp == 255)
        box = ((y.min(), x.min()), (y.max(), x.max()))
        img = img[box[0][0]:box[1][0], box[0][1]:box[1][1]]
        self._box = box
        return img

    @property
    def box(self):
        return self._box


class MyThreshold():

    def __init__(self, val=255, ksize=5,
                 crit=cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU):
        self._val = val
        self._ksize = ksize
        self._crit = crit

    def run(self, img):
        _, tmp = cv2.threshold(img, 0, self._val, self._crit)
        if self._ksize:
            tmp = cv2.medianBlur(tmp, self._ksize)
        return tmp


class StdResize(object):

    def __init__(self, h, method=cv2.INTER_LINEAR):
        self._h = h
        self._method = method

    def run(self, img):
        r = float(img.shape[1])/img.shape[0]
        img = cv2.resize(img, (int(r * self._h), self._h),
                         interpolation=self._method)
        return img


if __name__ == '__main__':
    img = load_gray('test/test4.jpg')
    c = Crop()
    asd = c.run(img)
    imshow(asd)
