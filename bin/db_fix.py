#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: db_fix.py <src> <dst> -p <prefix> [-s <start>]

Options:
    -h --help     Show this screen
    -p --prefix   prefix
    -s --start    start counter
"""

import os
import cv2

from glob import glob
from mscr.util import MyProgressBar


class FixDb():

    def __init__(self, src, dst,  prefix, start=0, ext='.jpg', sep='.', pad=5):
        self._src = src
        self._dst = dst
        self._pref = prefix
        self._sep = sep
        self._pad = pad
        self._ext = ext
        self._start = int(start)

    def run(self):
        count = self._start
        filez = glob(self._path + os.sep + '*')
        pbar = MyProgressBar(len(filez))
        for img in filez:
            name = (self._pref + self._sep + str(count).zfill(self._pad) +
                    self._ext)
            img = cv2.imread(img)
            cv2.imwrite(os.path.join(self._dst, name), img)
            pbar.update()
            count += 1
        pbar.finish()


if __name__ == '__main__':
    from docopt import docopt

    args = docopt(__doc__)
    start = args['<start>'] if args['<start>'] else 0
    fix = FixDb(args['<src>'], args['<dst>'], args['<prefix>'], start)
    fix.run()
