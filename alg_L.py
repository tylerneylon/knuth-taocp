# alg_L.py
#
# Usage: python alg_L.py <n>
#

import sys

# Iterate over a linked list (stored as a Python list).
def linked_list(p):
    j = 0
    k = p[j]
    while k > 0:
        yield j, k
        j = k
        k = p[j]

# Iterate over all Langford pairs for the given value of n.
def algorithm_L(n, x=None, p=None, ell=0):

    # Initialize as in L1.
    if x is None:
        x = [0] * (2 * n + 1)
        p = list(range(1, n + 2))
        p[-1] = 0
        y = [0] * (2 * n)

    # Check the visit condition as in L2.
    if ell == 2 * n:
        yield x[:-1]
        return

    for j, k in linked_list(p):

        # See if x[ell] = k can work as in L3.
        if ell + k + 1 >= 2 * n:
            return
        if x[ell +k + 1] != 0:
            continue
        x[ell] = k
        x[ell + k + 1] = -k
        p[j] = p[k]

        # Recursively solve the rest. Analogous to "return to L2."
        yield from algorithm_L(n, x, p, x.index(0, ell))

        # This is analogous to L5.
        p[j] = k
        x[ell + k + 1] = 0
        x[ell] = 0

# This clause prints the first solution alphabetically.
if False:
    for x in algorithm_L(int(sys.argv[1])):
        print(x)
        print(''.join(chr(abs(xi) + ord('a') - 1) for xi in x))
        break

# This clause prints half the number of distinct solutions.
if True:
    count = 0
    for x in algorithm_L(int(sys.argv[1])):
        count += 1
    print(count // 2)
