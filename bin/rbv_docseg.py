#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: rbv_docseg.py <model> <nblock> <nneigh> <img> [-d] [-s <dir>]

Options:
  -h --help      show this message
  -d --display   display intermidiate seg
  -s --save      dir output save
"""

pdiv = (8, 8)
sdiv = (8, 8)
md = (3, 3)
Md = (6, 6)
microsize = (16, 16)
labels = {'ms': 1, 'txt': 0}


def parse_args():
    args = docopt(__doc__)
    imfile = args['<img>']
    nblock = int(args['<nblock>'])
    model = args['<model>']
    nneigh = int(args['<nneigh>'])
    display = args['--display']
    save = args['<dir>']
    return imfile, model, nblock, nneigh, display, save


if __name__ == '__main__':
    from cv2 import imwrite
    from os.path import join as pjoin
    from os.path import basename as pbase
    from docopt import docopt

    from mscr.util import load_gray, imshow, AddSuffix, MyKNN
    from mscr.bovw import BoVW
    from mscr.blocks import RandBlockIter
    from mscr.blockVote import Vote, BlockVote, Votes2Img
    from mscr.grid import Grid, GridClassifier

    imfile, model, nblock, nneigh, display, save = parse_args()
    img = load_gray(imfile)

    print '#------------------'
    print imfile

    # random block voting
    bvw = BoVW()
    bvw.load(model)
    rbv = BlockVote(
        Vote(bvw), RandBlockIter(nblock, pdiv, sdiv, md, Md))
    votes = rbv.run(img)

    if display:
        rbv.show()

    # corase segmentation
    coarse = Votes2Img(img.shape[:2]).run(votes)

    # final segmentation
    grid = GridClassifier(MyKNN(labels, nn=nneigh), Grid(microsize))
    grid.run(img, coarse)
    grid.finalize()
    res = grid.show()

    if display:
        imshow(res)

    if save:
        base = pbase(imfile)
        outfile = pjoin(save, AddSuffix('out', 'jpg').run(base))
        imwrite(outfile, res)
        outfile = pjoin(save, AddSuffix('out', 'pck').run(base))
        grid.save(outfile)
