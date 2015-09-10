#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import pylab as plt


class Features():

    def __init__(self, feat, debug=False):
        self._ft = feat
        self._debug = debug
        self._img = None

    def run(self, X, y=-1):
        self._img = X.copy()
        tX, ty = [], []
        if isinstance(y, int):
            tmpx, num = self.__run(X)
            tmpy = y * np.ones((1, num), np.uint8)
            tX = np.vstack((tX, tmpx)) if len(tX) > 0 else tmpx
            ty = np.hstack((ty, tmpy)) if len(ty) > 0 else tmpy
        else:
            # to do: implement list version
            pass

        return tX, ty

    def __run(self, x):
        kp = self._ft.detect(x)
        de = self._ft.compute(x, kp)
        if self._debug:
            tmp = cv2.cvtColor(self._img, cv2.COLOR_GRAY2BGR)
            tmp = cv2.drawKeypoints(tmp, kp, tmp)
            plt.imshow(tmp)
            plt.show()

        return (de[1], len(kp))


if __name__ == '__main__':
    pass
