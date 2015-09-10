#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: db_dumpfeat.py -i <dbroot> -d <dataout> -l <labelout>

Options:
    -h --help  show this message
"""


def parse_args():
    args = docopt(__doc__)
    dbroot = args['<dbroot>']
    dataout = args['<dataout>']
    labelout = args['<labelout>']
    return dbroot, dataout, labelout

if __name__ == '__main__':
    from numpy import save as npsave
    from mscr.data import Data
    from mscr.features import Features
    from docopt import docopt
    from cv2.xfeatures2d import SURF_create as SURF

    dbroot, dataout, labelout = parse_args()
    data = Data(Features(SURF()))
    X, y = data.load(dbroot, {'txt': 0, 'ms': 1})
    npsave(dataout, X)
    npsave(labelout, y)
