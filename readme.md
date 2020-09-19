# knuth-taocp

This is a collection of algorithms and related coding problems from Donald
Knuth's The Art of Computer Programming.

Recently I've been reading through section 7.2.2 about backtracking algorithms,
and the current code is based on that.

Files:
* `alg_b.py` - This contains the generic backtracking method, Algorithm 7.2.2B.
* `alg_L.py` - This contains the Python version of a way to find all Langford
  pairs, Algorithm 7.2.2L.
* `alg_L.c` - This is the C version of alg_L.py, also Algorithm 7.2.2L.

Based on one timing test, it looks like alg_L.C is about 64x faster than
alg_L.py.
