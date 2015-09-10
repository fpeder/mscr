#!/usr/bin/env python
# -*- coding: utf-8 -*

import cPickle as pickle

from os.path import exists as pex
from sklearn import cross_validation
from cv2.xfeatures2d import SURF_create as SURF
from sklearn.ensemble import RandomForestClassifier as RF

from data import Data
from features import Features
from codebook import CodeBook
from vq import VQ


class PrepData(object):

    def __init__(self, ndim):
        self._ndim = ndim

    def run(self, X, y):
        w = CodeBook(self._ndim).run(X)
        H = VQ(w, hist=self._ndim).run(
            X if isinstance(X, list) else list(X))
        return H, w


class FitBoVW(object):

    def __init__(self, cls=RF(n_estimators=40), nfold=3, verbose=True):
        self._cls = cls
        self._verbose = verbose
        self._nfold = nfold

    def run(self, X, y, ndim):
        H, w = PrepData(ndim).run(X, y)
        self._cls.fit(H, y)
        if self._verbose:
            print cross_validation.cross_val_score(
                self._cls, H, y, cv=self._nfold)

        return self._cls, H, w

    @property
    def cls(self):
        return self._cls


class BoVW(object):
    NFEAT_THR = 40

    def __init__(self, feat=SURF(), cls=RF(n_estimators=40), verbose=True):
        self._ft = Features(feat)
        self._da = Data(self._ft)
        self._fm = FitBoVW(cls)
        self._verbose = verbose
        self._cl = cls
        self._vq = None

    def predict(self, img):
        x = self._ft.run(img)[0]
        if x is not None and len(x) > self.NFEAT_THR:
            x = self._vq.run([x])
            p, prob = self._cl.predict(x), self._cl.predict_proba(x)
        else:
            p, prob = -1, 1.0
        return p, prob

    def fit(self, X, y, ndim):
        self._cl, H, w = self._fm.run(X, y, ndim)
        self._da.H = H.copy()
        self._da.w = w.copy()
        self._da.y = y.copy()

    def fit_from_db(self, dbroot, classes, ndim):
        X, y = self._da.load(dbroot, classes)
        self.fit(X, y, ndim)

    def fit_from_prep(self, infile):
        H, y, w = self._da.load_from_file(infile)
        self._vq = VQ(w, hist=w.shape[0])
        self._cl.fit(H, y)
        if self._verbose:
            print cross_validation.cross_val_score(
                self._cl, H, y, cv=3).mean()

    def save(self, outfile):
        if self._vq and self._cl:
            pickle.dump((self._vq, self._cl), open(outfile, 'wb'))

    def save_prep(self, outfile):
        self._da.dump(outfile, ['H', 'w', 'y'])

    def load(self, infile):
        assert pex(infile), 'bovw.py: %s dosen\'t exist' % infile
        self._vq, self._cl = pickle.load(open(infile, 'rb'))

    # #def predict_from_prep(self, X, y):
    # #    pass

    # def fit(self, X, y, Ndim):
    #     w = CodeBook(Ndim).run(X)
    #     vq = VQ(w, hist=Ndim)
    #     H = self._vq.run(X)
    #     self._cls.fit(H, y)
    #     self._w = w
    #     self._vq = vq
    #     self._H = H

    # def fit_from_db(self, dbroot, classes, Ndim):
    #     X, y = self._d.load(dbroot, classes)
    #     w = self._d.data['w'] = CodeBook(Ndim).run(X)
    #     self._vq = VQ(w, hist=Ndim)
    #     H = self._d.data['H'] = self._vq.run(X)
    #     self._cls.fit(H, y)

    # def fit_from_preprocessed(self, infile):
    #     self._d.load_from_file(infile)
    #     w = self._d.data['w']
    #     H = self._d.data['H']
    #     y = self._d.data['y']
    #     self._vq = VQ(w, hist=len(w))
    #     self._cls.fit(H, y)

    # def cross_validation(self, nfold=3):
    #     scores = cross_validation.cross_val_score(
    #         self._cls, self._d.data['H'], self._d.data['y'], cv=nfold)
    #     return scores

 

    # @property
    # def data(self):
    #     return self._d


if __name__ == '__main__':
    bbb = BoVW()
    bbb.fit_from_preprocessed('data/new.prep.32.pck')
    test = pickle.load(open('data/ext.prep.pck', 'rb'))
    bbb.predict_from_prep(test['H'], test['y'])
