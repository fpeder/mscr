#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: db_ext_split.py <src> <dst> <prob>

Options:
    -h --help
"""

import os
import cv2

from glob import glob
from docopt import docopt

from mscr.split import Split, RandomSplitPredicate
from mscr.util import Crop
from mscr.data import MyProgressBar

PAD = 8

if __name__ == '__main__':
    args = docopt(__doc__)
    src = args['<src>']
    dst = args['<dst>']
    prob = float(args['<prob>'])
    split = Split(RandomSplitPredicate(p=prob))
    crop = Crop()

    count = 0
    if os.path.exists(src) and os.path.exists(dst):
        filz = glob(os.path.join(src, '*.jpg'))
        pbar = MyProgressBar(len(filz), 'extending db:')
        for im in filz:
            img = cv2.imread(im)
            img = crop.run(img)
            for bl in split.run(img):
                out = os.path.join(dst, str(count).zfill(PAD) + '.jpg')
                cv2.imwrite(out, bl.img)
                count += 1
            pbar.update()
        pbar.finish()

    else:
        print 'err: dimstat.py: path doesn\'t exists'
