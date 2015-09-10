#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: draw_blocks.py -i <in> -o <out>

Options:
   -h --help
"""

SIZE = (1056, 816, 3)
COLOR = {'txt': 32, 'ms': 255-32}

if __name__ == '__main__':
    import numpy as np
    import cPickle as pickle

    from docopt import docopt
    from cv2 import imwrite

    args = docopt(__doc__)

    infile = args['<in>']
    outfile = args['<out>']
    blocks = pickle.load(open(infile, 'r'))
    img = 128 * np.ones(SIZE, np.uint8)

    for block in blocks:
        cls, bb = block
        x1, y1 = bb[0]
        x2, y2 = bb[1]
        img[y1:y2, x1:x2, :] = COLOR[cls]

    imwrite(outfile, img)
