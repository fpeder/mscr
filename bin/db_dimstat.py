#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: db_dimstat.py <src>

Options:
    -h --help
"""

import numpy as np

from docopt import docopt
from mscr.util import ImgFileIter


if __name__ == '__main__':
    args = docopt(__doc__)
    src = args['<src>']

    dim = []
    fileIter = ImgFileIter(src)
    for x in fileIter.run():
        tmp = x.shape[:2]
        dim = np.vstack((dim, tmp)) if len(dim) > 0 else tmp

    print dim.mean(axis=0), dim.std(axis=0)
