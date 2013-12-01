#!/usr/bin/python

import argparse
import sys
import copy
import blm

parser = argparse.ArgumentParser(description="Check a text document against Benford's law.")

args = parser.parse_args()

bl = blm.benfords_law(sys.stdin.read(), 0.01)
print bl.get_result()
