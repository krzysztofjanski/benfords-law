#!/usr/bin/python

import argparse
import sys
import copy
import blm

parser = argparse.ArgumentParser(description="Check a text document against Benford's law.")
parser.add_argument('-t', '--treshold', dest='treshold', type=float, default=0,
	help='treshold to match frequencies')
args = parser.parse_args()

bl = blm.benfords_law(sys.stdin.read(), args.treshold)
print bl.get_result()
