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
                print(f'Loaded {len(words[wordsize])} words of size {wordsize}')

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

        # XXX and below
        y = x

        try:
            # For each row prefix, find the set of possible next letters.
            prefixes = [''.join(col[i] for col in x[:ell]) for i in range(m)]
            next_letters = [row_next_letters[prefix] for prefix in prefixes]
        except:
            print('x:', x)

        # Find the compatible word sets.
        try:
            word_sets = [
                    set.union(*[col_words[(i, let)] for let in next_letters[i]])
                    for i in range(m)
            ]
        except:
            print('x:', x)
            print('ell:', ell)

        # I suspect the intersection will be faster if we sort the word sets.
        # I have not verified this.
        word_sets.sort(key=len)

        undo_stack.append(D[ell])
        D[ell] = set.intersection(*word_sets)

    def downdate(x, ell):
        D[ell] = undo_stack.pop()

    x = [None] * n
    for wordrect in algorithm_b(x, D, is_good, update, downdate):
        print(wordrect)

if __name__ == '__main__':
    find_word_rect(5, 6)
