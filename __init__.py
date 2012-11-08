from __future__ import division

__author__ = "Marek Rudnicki"


import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument(
    '--log',
    dest='loglevel'
)
parser.add_argument(
    '--backend',
    dest='backend'
)
parser.add_argument(
    '--machines',
    dest='machines',
    nargs='+',
    default=[]
)
parser.add_argument(
    '--cache',
    dest='cache'
)
parser.add_argument(
    '--plot',
    dest='plot'
)


args = parser.parse_args()



if args.loglevel is None:
    logging.basicConfig(level=logging.INFO)
else:
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level)


logging.debug(args)



import thorns
import waves

from dumpdb import (
    dumpdb,
    loaddb
)
from maps import map
from plot import plot
