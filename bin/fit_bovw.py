#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: fit_bovw.py -i <prep_data> -o <out>

Options:
    -h --help
"""


def parse_args():
    args = docopt(__doc__)
    infile = args['<prep_data>']
    outfile = args['<out>']
    return infile, outfile

if __name__ == '__main__':
    from os.path import exists as pex
    from docopt import docopt
    from mscr.bovw import BoVW

    infile, outfile = parse_args()
    assert pex(infile), "file %s dosen't exist" % infile

    bbb = BoVW()
    bbb.fit_from_prep(infile)
    bbb.save(outfile)
