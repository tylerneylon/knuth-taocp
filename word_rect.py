""" word_rect.py

    Find a word rectangle.

"""

from collections import defaultdict

from alg_b import algorithm_b

def get_word_path(wordsize):
    suffix = 'sgb' if wordsize == 5 else 'OSPD4'
    return f'data/words{wordsize}-from-{suffix}'

def find_word_rect(m, n):
    """ Find a word rectangle of size m x n; ie a word rectangle with m rows and
        n columns, where each row and each column is an English word.
    """

    # Load in the pertinent word lists.
    words = {}
    for wordsize in [m, n]:
        if wordsize not in words:
            with open(get_word_path(wordsize)) as f:
                words[wordsize] = [line.strip() for line in f]

    # Index the word lists so we can more efficiently build the rectangle.
    # row_next_letters[prefix] = <the set of valid next letters; may be empty>
    row_next_letters = defaultdict(set)
    for word in words[n]:
        for i in range(1, n):
            row_next_letters[word[:i]].add(word[i])

    # col_words[(i, let)] = <set of words w with w[i] == let>
    col_words = defaultdict(set)
    for word in words[m]:
        for i in range(m):
            col_words[(i, word[i])].add(word)

    # For easier downdating, we'll keep around an undo stack.
    undo_stack = []

    # We'll work effectively with algorithm W (which, as I've written alg B, is
    # the same since I can update D within the update()/downdate() functions).
    # The list x will hold the candidate words in the first ell columns of the
    # word rectangle.

    # Prepare our list of domains D.
    # We plan to modify these as the algorithm runs.
    D = [words[m] for _ in range(n)]

    def is_good(x, ell):
        # They will be good automatically by virtue of update()/downdate().
        return True

    def update(x, ell):
        ''' This receives a list x[0] .. x[ell - 1], each a word of length m.
            We think of these words as columns. For partial row i, this
            function finds the set of column words such that the augmented row
            has any word completions; this is word_sets[i]. The intersection of
            all word_sets is the set of all compatible next columns, which we
            place into D[ell]. This set may be empty, in which case algorithm b
            will backtrack.
        '''

        # For each row prefix, find the set of possible next letters.
        prefixes = [''.join(col[i] for col in x[:ell]) for i in range(m)]
        next_letters = [row_next_letters[prefix] for prefix in prefixes]

        # Find the set of words that could be the next column word.
        word_sets = [set() for _ in range(m)]
        for i, word_set in enumerate(word_sets):
            for let in next_letters[i]:
                word_set |= col_words[(i, let)]

        # The intersection is heuristically faster with shorter sets first.
        word_sets.sort(key=len)
        undo_stack.append(D[ell])
        D[ell] = set.intersection(*word_sets)

    def downdate(x, ell):
        D[ell] = undo_stack.pop()

    x = [None] * n  # There are n columns.
    for wordrect in algorithm_b(x, D, is_good, update, downdate):
        print()
        for i in range(m):  # Print out each of the m rows.
            print(''.join(col[i] for col in x))

if __name__ == '__main__':
    find_word_rect(5, 8)
