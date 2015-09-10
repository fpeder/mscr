#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from sklearn.neighbors import NearestNeighbors
from util import MyProgressBar


class VQ():

    def __init__(self, cb, nneigh=1, algo='ball_tree', hist=False,
                 verbose=False):
        #self._verb = verbose
        self.cb = cb
        self._hist = hist
        self._nbrs = NearestNeighbors(n_neighbors=nneigh,
                                      algorithm=algo)

    def run(self, X):
        self._nbrs.fit(self.cb)
        H = np.array([])
        #if self._verb:
        #    pbar = MyProgressBar(len(X), 'vq')

        if isinstance(X, list):
            for x in X:
                _, tmp = self._nbrs.kneighbors(x)
                if self._hist:
                    tmp, _ = np.histogram(tmp, self._hist)
                    tmp = tmp.astype(np.float32)/tmp.sum()
                    H = np.vstack((H, tmp)) if len(H) > 0 else tmp
                #if self._verb:
                #    pbar.update()
            #if self._verb:
            #    pbar.finish()
        else:
            print 'err: vq: needs a list'

        return H


if __name__ == '__main__':
    pass
