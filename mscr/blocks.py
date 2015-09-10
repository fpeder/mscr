#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import ctypes as ct
import numpy.ctypeslib as npct

from util import get_dim


class RandBlockIter(object):

    def __init__(self, num, pdiv=(16, 16), sdiv=(8, 8), md=(7, 7), Md=(3, 3)):
        self._num = num
        self._md = md
        self._Md = Md
        self._pdiv = pdiv
        self._sdiv = sdiv

    def run(self, img):
        H, W = get_dim(img)
        count = 0
        while count < self._num:
            (y, x, h, w) = self.__get_rand_block(H, W)
            tmp = img[y:y+h, x:x+w]
            count += 1
            yield tmp, (y, x, h, w)

    def __get_rand_block(self, H, W):
        w = self.__myrand(W/self._Md[1], W/self._md[1], self._sdiv[1])
        h = self.__myrand(H/self._Md[0], H/self._md[0], self._sdiv[0])
        x = self.__myrand(0, W, self._pdiv[1])
        y = self.__myrand(0, H, self._pdiv[0])
        x = x if x < W - w else W - w
        y = y if y < H - h else H - h
        return (y, x, h, w)

    def __myrand(self, low, high, step):
        delta = float((high - low))/step
        x = np.floor(np.random.uniform(0, high-low)/delta)*delta + low
        return x.astype(int)


class TrivialBlockIter():

    def __init__(self, w, h):
        self._w = w
        self._h = h

    def run(self, img):
        H, W = img.shape[:2]
        for i in range(0, H - self._h, self._h):
            for j in range(0, W - self._w, self._w):
                tmp = img[i:i+self._h, j:j+self._w]
                yield tmp, (i, j, self._h, self._w)


class SlidingBlockIter():

    def __init__(self, w, s):
        self._iter = Blocketize(w, s)

    def run(self, img):
        for box, block in self._iter.run(img):
            yield box, block


class Blocketize():
    LIB = 'blocketize'

    def __init__(self, dim, skip):
        self._w, self._h = dim
        self._sx, self._sy = skip
        self._blpr = npct.load_library(self.LIB, 'mscr/clib')

    def run(self, img):
        self._img = img
        H, W = img.shape[:2]
        M, N, L = self.__blocks_num(H, W)
        boxes = [(y, x, self._w, self._w)
                 for y in np.arange(0, H - self._h, self._sy)
                 for x in np.arange(0, W - self._w, self._sx)]
        blocks = self.__run(img, H, W, M*N, L)
        return zip(blocks, boxes)

    def __run(self, img, H, W, T, L):
        out = np.zeros((T, L), np.uint8)
        myptr = ct.POINTER(ct.c_uint8)
        self._blpr.blocketize.argtypes = [myptr, ct.c_int, ct.c_int,
                                          myptr, ct.c_int, ct.c_int,
                                          ct.c_int, ct.c_int]
        self._blpr.blocketize.restype = ct.c_int
        self._blpr.blocketize(self._img.ctypes.data_as(myptr), H, W,
                              out.ctypes.data_as(myptr), T, L,
                              self._w, self._h, self._sx, self._sy)
        out = [x.reshape((self._w, self._w)) for x in out]
        return out

    def __blocks_num(self, H, W):
        M, N, L = (np.int32(np.ceil(float(H - self._h + 1)/self._sy)),
                   np.int32(np.ceil(float(W - self._w + 1)/self._sx)),
                   self._w * self._w)
        return M, N, L


if __name__ == '__main__':
    from util import load_gray

    img = load_gray('test/test4.jpg')
    for bl in RandBlockIter(5).run(img):
        print 'a'
