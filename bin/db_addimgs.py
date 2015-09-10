#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: db_addimgs.py <src> <dst> <cls>

Options:
   -h, --help  Show this screen
"""

import os
import hashlib

from glob import glob
from cv2 import imwrite
from mscr.util import ImgFileIter


class Add():

    def __init__(self, src, dst, cls, hfunc=hashlib.sha1):
        self._src = src
        self._dst = dst
        self._cls = cls
        self._filez = os.path.join(self._dst, self._cls + '.txt')
        self._hfunc = hfunc

    def run(self):
        H = self.__read()
        num = self.__get_last_num()
        for img in ImgFileIter(self._src).run():
            h = self._hfunc(img).hexdigest()
            if h not in H:
                self.__append(h)
                out = os.path.join(self._dst, self._cls, self._cls +
                                   '.' + str(num).zfill(5) + '.jpg')
                print out
                imwrite(out, img)
                num += 1

    def __get_last_num(self):
        tmp = glob(os.path.join(self._dst, self._cls, '*.jpg'))
        tmp.sort()
        num = int(tmp[-1].split('.')[1])
        return num+1

    def __read(self):
        with open(self._filez, 'r') as fil:
            H = [x.strip('\n') for x in fil.readlines()]
        fil.close()
        return H

    def __append(self, h):
        with open(self._filez, 'a') as fil:
            fil.write(h + '\n')
        fil.close()

    def is_new(self):
        pass


if __name__ == '__main__':
    from docopt import docopt

    args = docopt(__doc__)
    add = Add(args['<src>'], args['<dst>'], args['<cls>'])
    add.run()
