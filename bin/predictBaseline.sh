#!/bin/bash

bdir=test

for n in $(seq 100 140)
do
    if [ ! -e $bdir/test.$n.tif ]
    then
	convert test/test.$n.jpg $bdir/test.$n.tif
    fi
    python -m bin/predictBaseline $bdir/test.$n.tif -s
done
