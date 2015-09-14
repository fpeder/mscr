#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='mscr',
    version='0.1',
    author='Fabrizio Pedersoli',
    author_email='f.peder@gmail.com',
    packages=['mscr'],
    scripts=['bin/*.py'],
    license='LICENSE.txt',
    url='http://github.com/fpeder/mscr',
    description='Document segmentation into music score and text',
    long_descriotion=open('README.md').read(),
    install_requires=["sklearn", "cv2", "numpy"],
)
