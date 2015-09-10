#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: db_printdim.py <src>

Options:
    -h --help
"""

import os
import sys
import cv2

from glob import glob
from docopt import docopt


if __name__ == '__main__':
    args = docopt(__doc__)
    src = args['<src>']

    if not os.path.exists(src):
        sys.exit('error: %s doesn\'t exists' % src)

    for fil in glob(os.path.join(src, '*.jpg')):
        img = cv2.imread(fil)
        H, W = img.shape[:2]
        print '%s\t%d %d' % (fil, H, W)
