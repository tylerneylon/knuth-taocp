# alg_P.py
#
# This implements Knuth's Algorithm P from section 7.2.1.2 of TAoCP.
#
# This algorithm takes any given list and returns, as a Python generator,
# all permutations of that list. It does so efficiently in the sense that
# each iteration only uses a single pair swap.
#
# To be honest, I only have partial understanding of why this code works,
# so I can't yet include great comments to clarify the thinking behind
# this. Note that Knuth uses 1-based indexes whereas I've adjusted things
# a bit to use 0-based indexes.
#

def algorithm_P(items):

    c    = [0] * len(items)
    sign = [1] * len(items)  # This is Knuth's variable `o`.

    while True:

        yield items

        j = len(items) - 1
        s = 0

        # Update j and s to choose the pair to swap.
        while True:
            q = c[j] + sign[j]
            if q > j:
                if j == 1:
                    return
                s += 1
            if 0 <= q <= j:
                break
            sign[j] *= -1
            j -= 1

        m, n = j - c[j] + s, j - q + s  # We'll swap these two indexes.
        items[m], items[n] = items[n], items[m]
        c[j] = q

if __name__ == '__main__':
    # An example usage:
    for items in algorithm_P([5, 1, 3, 4, 2]):
        print(' '.join(map(str, items)))
