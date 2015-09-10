#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: res_prstats.py <msfile> <txtfile>

Options:
  -h --help   show this message
"""


def parse_args():
    args = docopt(__doc__)
    msfile = args['<msfile>']
    txtfile = args['<txtfile>']
    return msfile, txtfile


def get_stats(infile):
    res = np.loadtxt(infile)
    p, r = res[:, 1], res[:, 2]
    f = 2*p*r/(p+r)
    f[np.isnan(f)] = 0
    return p*100, r*100, f*100


def printa(lab, p, r, f):
    print '%s & $%.1f\pm %.1f$ & $%.1f\pm %.1f$ & $%.1f\pm %.1f$\\\\' % \
        (lab, p.mean(), p.std(), r.mean(), r.std(), f.mean(), f.std())


def avg(x, y):
    return np.array([x, y]).mean()


if __name__ == '__main__':
    import numpy as np
    from docopt import docopt

    msfile, txtfile = parse_args()
    p1, r1, f1 = get_stats(msfile)
    printa('music', p1, r1, f1)
    p2, r2, f2 = get_stats(txtfile)
    printa('text', p2, r2, f2)
    print 'avg & $%.1f\pm %.1f$ & $%.1f\pm %.1f$ & $%.1f\pm %.1f$\\\\' %\
        (avg(p1.mean(), p2.mean()), avg(p1.std(), p2.std()),
         avg(r1.mean(), r2.mean()), avg(r1.std(), r2.std()),
         avg(f1.mean(), f2.mean()), avg(f1.std(), f2.std()))
