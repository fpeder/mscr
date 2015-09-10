#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='mscr',
    version='0.1',
    author='Fabrizio Pedersoli',
    author_email='fpeder@uvic.ca',
    packages=['mscr'],
    scripts=['bin/train.py', 'bin/predict.py', 'bin/fitModel.py'],
    license='LICENSE.txt',
    description='Music Score Detection in Images',
    long_descriotion=open('README.md').read(),
    install_requires=["sklearn", "cv2", "numpy"],
)
