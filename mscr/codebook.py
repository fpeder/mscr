#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class CodeBook():

    def __init__(self, K):
        self._K = K
        self._criteria = (cv2.TERM_CRITERIA_EPS +
                          cv2.TERM_CRITERIA_MAX_ITER,
                          10, 1.0)

    def run(self, X):
        Xt = np.vstack(X)
        _, _, self._words = cv2.kmeans(Xt, self._K, None, self._criteria,
                                       10, cv2.KMEANS_RANDOM_CENTERS)
        return self._words


if __name__ == '__main__':
    pass
