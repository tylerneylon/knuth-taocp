#!/usr/bin/env python
""" commafree.py

    This is an implementation of Donald Knuth's commafree-code-finding Algorithm
    C from section 7.2.2 of The Art of Computer Programming. I'll explain the
    key idea, but I recommend reading that section to understand this in depth.

    The output of this program is a list of codewords of length 4 with the
    alphabet 1-m, for some variable integer m in the range [2, 7].
    The output list of codewords has the special property that, if we know the
    codebook (the codeword list), and we see any sequence of characters from a
    longer, delimiter-free (concatenated) list of codewords, then we can always
    immediately know where the word boundaries are despite not having any
    delimiters. For example, the sequence

        ...mathisle...

    could be from a sequence of words like

        ... math, isle, ...

    or just as well from a sequence of words like

        ... puma, this, lead, ...  (same letters as ...pu math isle ad..).

    So we see that the three words "math", "isle", and "this" should not be in a
    commafree codebook because, given "mathisle", we can't tell if it starts
    with "math" or if "ma" is the end of some other word, and we would start
    with "this" after "ma". Note that we want to be nice to the decoder, so the
    three-word vocab "math", "isle", "this" is invalid even if there is no other
    word ending in "ma" (this omission, to a clever human, might still let them
    find the word boundaries in "mathisle").

    Usage:

        ./commafree.py <m> [g]

    m = The base we're working in; aka the alphabet size.

    g = The goal number of codewords.

    If g is not provided, this looks for the maximum possible codebook, which
    has size L = (m^4 - m^2) / 4.
"""


# ______________________________________________________________________
# Imports

import math
import sys

import numpy as np


# ______________________________________________________________________
# Globals

alf   = None
M     = None
stamp = None
sigma = None


# ______________________________________________________________________
# Functions

def find_commafree_code(m, g):

    # Step C1: Initialize.
    init(m, g)

def init(m, g):

    global alf, M, stamp, sigma

    alf = [0] * (16 ** 3 * m)
    for a in range(m):
        for b in range(m):
            for c in range(m):
                for d in range(m):
                    # alf[(abcd)_16] = (abcd)_m
                    abcd_m = ((a * m + b) * m + c) * m + d
                    alf[4096 * a + 256 * b + 16 * c + d] = abcd_m

    M = math.floor(23.5 * m ** 4)
    stamp = [0] * M
    sigma = 0


# ______________________________________________________________________
# Main

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    m = int(sys.argv[1])
    assert 1 < m <= 7

    if len(sys.argv) > 2:
        g = sys.argv[2]
    else:
        g = (m ** 4 - m ** 2) / 4
    g = int(g)

    print('_' * 70)
    print(f'Working with alphabet size m={m}, goal codebook size g={g}.')

    find_commafree_code(m, g)
