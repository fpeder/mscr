#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: db_ext_rb.py <src> <dst>

Options:
    -h --help
"""

import cv2
import os

from docopt import docopt

from mscr.util import ImgFileIter, Crop
from mscr.blocks import RandBlockIter


if __name__ == '__main__':
    args = docopt(__doc__)
    src = args['<src>']
    dst = args['<dst>']

    for folder in ['ms', 'txt']:
        fileiter = ImgFileIter(os.path.join(src, folder), crop=Crop())
        blockiter = RandBlockIter(15)
        count = 0
        for x in fileiter.run():
            for b, _ in blockiter.run(x):
                outfile = os.path.join(dst, folder, str(count).zfill(8)
                                       + '.jpg')
                cv2.imwrite(outfile, b)
                count += 1
