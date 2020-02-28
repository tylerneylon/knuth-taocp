def pass_(*args):
    pass

def algorithm_b(x, D, is_good, update=pass_, downdate=pass_, ell=0):
    """ This is the basic backtrack algorithm from section 7.2.2.

        x is a list whose values will be changed as this iterates; x will be the
        list yielded when valid solutions are found.

        D is a list of lists. D[ell] is the list, in order, of all possible
        valid values for x[ell].

        is_good(x, ell) returns True when x[0], ..., x[ell] is a valid partial
        solution.

        The optional functions update() and downdate() provide callers a
        convenient way to keep track of intermediate helper data structures that
        allow is_good to operate more efficiently.
    """

    # print(f'algorithm_b with ell={ell}.')

    if ell == len(x):
        # print(f'About to yield {x}.')
        yield x
        return

    # print('ell:')
    # print(ell)

    # print('D:')
    # print(D)

    for d in D[ell]:
        x[ell] = d
        ell += 1
        if is_good(x, ell):
            update(x, ell)
            yield from algorithm_b(x, D, is_good, update, downdate, ell)
            downdate(x, ell)
        ell -= 1

def permutations(n):

    def is_good(x, ell):
        return len(set(x[0:ell])) == ell

    x = [0] * n
    D = [list(range(n)) for _ in range(n)]

    for p in algorithm_b(x, D, is_good):
        print(p)

def combinations(n, k):

    def is_good(x, ell):
        return len(set(x[0:ell])) == ell

    x = [0] * k
    D = [list(range(n)) for _ in range(n)]

    for p in algorithm_b(x, D, is_good):
        print(p)

def n_queens(n):

    def is_good(x, ell):
        # Ensure each queen is in a unique column.
        if len(set(x[0:ell])) < ell:
            return False
        # Ensure the new queen is not attacked along diagonals.
        for k in range(ell - 1):
            if ell - 1 - k == abs(x[ell - 1] - x[k]):
                return False
        return True

    x = [0] * n
    D = [list(range(n)) for _ in range(n)]

    for i, q in enumerate(algorithm_b(x, D, is_good)):
        print()
        print(f'Solution {i + 1}:')
        for col in x:
            print(f'{"L_ " * col} * {"L_ " * (n - col - 1)}')

# permutations(4)

# combinations(5, 3)

n_queens(8)
