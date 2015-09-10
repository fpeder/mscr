#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: ubv_docseg.py <model> <w> <h> <nneigh> <img> [-d] [-s <dir>]

Options:
  -h --help      show this message
  -d --display   display intermidiate seg
  -s --save      dir output save
"""

labels = {'ms': 1, 'txt': 0}
microsize = (16, 16)


def parse_args():
    args = docopt(__doc__)
    imgf = args['<img>']
    model = args['<model>']
    w = int(args['<w>'])
    h = int(args['<h>'])
    nn = int(args['<nneigh>'])
    display = args['--display']
    save = args['<dir>']
    return imgf, model, w, h, nn, display, save


if __name__ == '__main__':
    from cv2 import imwrite
    from docopt import docopt
    from os.path import join as pjoin
    from os.path import basename as pbase
    from mscr.util import load_gray, MyKNN, imshow, AddSuffix
    from mscr.bovw import BoVW
    from mscr.blocks import TrivialBlockIter
    from mscr.blockVote import Vote, BlockVote, Votes2Img
    from mscr.grid import Grid, GridClassifier

    imgf, model, w, h, nn, display, save = parse_args()
    img = load_gray(imgf)

    print '#-----------------------'
    print imgf

    bvw = BoVW()
    bvw.load(model)

    ubv = BlockVote(Vote(bvw), TrivialBlockIter(w, h))
    votes = ubv.run(img)

    coarse = Votes2Img(img.shape[:2]).run(votes)

    grid = GridClassifier(MyKNN(labels, nn=nn), Grid(microsize))
    grid.run(img, coarse)
    grid.finalize()
    res = grid.show()

    if display:
        imshow(res)

    if save:
        base = pbase(imgf)
        outfile = pjoin(save, AddSuffix('out', 'jpg').run(base))
        imwrite(outfile, res)
        outfile = pjoin(save, AddSuffix('out', 'pck').run(base))
        grid.save(outfile)
