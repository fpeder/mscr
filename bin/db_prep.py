#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: db_prep.py -d <data> -l <label> -n <ndim> -o <outfile>

Options:
   -h --help   show this message
"""


def parse_args():
    args = docopt(__doc__)
    data = args['<data>']
    label = args['<label>']
    ndim = int(args['<ndim>'])
    outfile = args['<outfile>']
    return data, label, ndim, outfile

if __name__ == '__main__':
    from docopt import docopt
    from numpy import load
    from mscr.bovw import BoVW

    data, label, ndim, outfile = parse_args()
    X, y = load(data), load(label)
    bbb = BoVW()
    bbb.fit(X, y, ndim)
    bbb.save_prep(outfile)
