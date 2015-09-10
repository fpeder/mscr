#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: db_stddim.py <src> <dst> <dim>

Options:
   -h --help
"""

import os
import cv2

from docopt import docopt
from glob import glob

from mscr.data import MyProgressBar

PAD = 8


if __name__ == '__main__':
    args = docopt(__doc__)
    src = args['<src>']
    dst = args['<dst>']
    dim = int(args['<dim>'])

    count = 0
    if os.path.exists(src) and os.path.exists(dst):
        filz = glob(os.path.join(src, '*.jpg'))
        pbar = MyProgressBar(len(filz), 'stdimg')
        for im in filz:
            img = cv2.imread(im)
            ratio = float(img.shape[1])/img.shape[0]
            img = cv2.resize(img, (int(ratio*dim), dim))
            out = os.path.join(dst, str(count).zfill(PAD) + '.jpg')

            pbar.update()
            cv2.imwrite(out, img)
            count += 1

        pbar.finish()

    else:
        print 'err: stddim.py: path doesn\'t exists'
