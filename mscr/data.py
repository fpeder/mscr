#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import glob
import numpy as np
import sys
import cPickle as pickle

from util import MyProgressBar, Crop


class Data(object):

    def __init__(self, feat=None):
        self.data = {'X': [], 'y': [], 'H': [], 'w': []}
        self._feat = feat

    def load(self, dbroot, classes):
        X, y = DataHandler(dbroot, classes, feat=self._feat).run()
        self.data['X'] = X
        self.data['y'] = y
        return X, y

    def dump(self, outfile, keys):
        if self.check(keys):
            tmp = {k: self.data[k] for k in keys}
            pickle.dump(tmp, open(outfile, 'wb'))

    def load_from_file(self, infile):
        tmp = pickle.load(open(infile, 'rb'))
        for k in tmp.keys():
            self.data[k] = tmp[k]
        return self.data['H'], self.data['y'], self.data['w']

    def check(self, keys):
        for k in keys:
            if len(self.data[k]) == 0:
                return False
        return True

    @property
    def H(self):
        return self.data['H']

    @H.setter
    def H(self, val):
        self.data['H'] = val

    @property
    def w(self):
        return self.data['w']

    @w.setter
    def w(self, val):
        self.data['w'] = val

    @property
    def y(self):
        return self.data['y']

    @y.setter
    def y(self, val):
        self.data['y'] = val


class DataHandler(object):

    def __init__(self, dbroot, classes, fext='.jpg', feat=None, crop=False):
        self._dbroot = dbroot
        self._classes = classes
        self._crop = crop
        self._fext = fext
        self._feat = feat

    def run(self):
        X, y = [], []
        for cls, lab in self._classes.iteritems():
            path = os.path.join(self._dbroot, cls)
            if not os.path.exists(path):
                sys.exit('err: datahandler: path doesn\'t exists')

            imfile = glob.glob(os.path.join(path, '*' + self._fext))
            if len(imfile) == 0:
                sys.exit('err: datahadler: %s is empty' % path)

            pbar = MyProgressBar(len(imfile), cls)

            for fimg in imfile:
                x = cv2.imread(fimg, 0)
                x = Crop().run(x) if self._crop else x
                x, _ = self._feat.run(x, int(lab)) if self._feat else x
                if isinstance(x, np.ndarray):
                    X.append(x)
                    y.append(int(lab))
                    pbar.update()
            pbar.finish()

        return X, np.array(y)


if __name__ == '__main__':
    pass
