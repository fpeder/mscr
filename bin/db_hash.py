#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: db_hash.py <src>

Options:
    -h, --help  Show this screen
"""

import os
import hashlib

from mscr.util import ImgFileIter


class DbHash():

    def __init__(self, src, cls=['txt', 'ms'], hfunc=hashlib.sha1()):
        self._src = src
        self._cls = cls
        self._hfunc = hfunc

    def run(self):
        for cls in self._cls:
            path = os.path.join(self._src, cls)
            out = open(path + '.txt', 'w')
            for img in ImgFileIter(path, cls).run():
                self._hfunc.update(img)
                out.write(self._hfunc.hexdigest() + '\n')
            out.close()

if __name__ == '__main__':
    db = DbHash('db/newnew')
    db.run()
