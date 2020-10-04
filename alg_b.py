from collections import defaultdict

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

    for d in D[ell]:
        x[ell] = d
        ell += 1
        if is_good(x, ell):
            if ell == len(x):
                yield x
            else:
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

# The n-queens problem.

def n_queens_is_good(x, ell):
    # Ensure each queen is in a unique column.
    if len(set(x[0:ell])) < ell:
        return False
    # Ensure the new queen is not attacked along diagonals.
    for k in range(ell - 1):
        if ell - 1 - k == abs(x[ell - 1] - x[k]):
            return False
    return True

def print_board(x):
    n = len(x)
    for col in x:
        print(f'{"L_ " * col} * {"L_ " * (n - col - 1)}')

def n_queens(n):

    x = [0] * n
    D = [list(range(n)) for _ in range(n)]

    for i, q in enumerate(algorithm_b(x, D, n_queens_is_good)):
        print()
        print(f'Solution {i + 1}:')
        print_board(x)

def problem_8():
    """ The problem is to search for two different 8-queens solutions which are
        identical in the first six rows. """

    n = 8
    x = [0] * n
    D = [list(range(n)) for _ in range(n)]

    # `solns` will map (x1,x2,..,x6) to a list of full solutions.
    solns = defaultdict(list)
    for i, q in enumerate(algorithm_b(x, D, n_queens_is_good)):
        key = tuple(q[:6])
        solns[key].append((i + 1, q))
        if len(solns[key]) == 2:
            soln1, soln2 = solns[key]
            print()
            print('_' * 70)
            print(f'Solutions {soln1[0]} and {soln2[0]} are a pair:')
            print()
            print_board(soln1[1])
            print()
            print_board(soln2[1])

# permutations(4)
# combinations(5, 3)
# n_queens(8)

if __name__ == '__main__':
    problem_8()
