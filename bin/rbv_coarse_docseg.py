#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: predict.py <model> <nblock> <img> [-d] [-s <outdir>]

Options:
   -h --help
   -d --display
   -s --save
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
    display = args['--display']
    save = args['<outdir>']
    return imfile, nblock, model, display, save


if __name__ == '__main__':
    from docopt import docopt
    from os.path import basename as pbase
    from os.path import join as pjoin
    from mscr.util import load_gray, AddSuffix
    from mscr.bovw import BoVW
    from mscr.blocks import RandBlockIter
    from mscr.blockVote import Vote, BlockVote, Votes2Img

    imfile, nblock, model, display, save = parse_args()
    print '#----------------------------'
    print imfile

    img = load_gray(imfile)
    bbb = BoVW()
    bbb.load(model)

    rbv = BlockVote(
        Vote(bbb), RandBlockIter(nblock, pdiv, sdiv, md, Md))
    asd = rbv.run(img)

    if display:
        rbv.show()

    vimg = Votes2Img(img.shape[:2])
    vimg.run(asd)
    vimg.get_bounding_box()

    if save:
        base = pbase(imfile)
        outfile = pjoin(save, AddSuffix('out', 'pck').run(base))
        vimg.save_bb(outfile)
