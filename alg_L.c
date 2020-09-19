// alg_L.c
//
// This program explores Langford pairs by implementing algorithm L from section
// 7.2.2 from Donald Knuth's The Art of Computer Programming.
//
// The main function is alg_L(), which is based directly on the Knuth text. The
// biggest difference is that I've let the stack implicitly hold some variables
// for us, such as the undo buffer, called y in the text.
//
// This version is faster than the Python version in alg_L.py. For example, this
// code can compute the number of Langford pairs for n=15 in about 7 min, 5 sec.
// The Python version requires

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char *usage =
    "Usage:  alg_L [options] <n>                                            \n"
    "                                                                       \n"
    "    Searches for Langford pairs for the given value of n.              \n"
    "                                                                       \n"
    "    options:                                                           \n"
    "                                                                       \n"
    "        --alpha  Prints out alphabetic letters to represent the        \n"
    "                 Langford pair rather than integers.                   \n"
    "                                                                       \n"
    "        --checkpoints  Prints out regular progress reports.            \n"
    "                                                                       \n"
    "        --count  Prints out only the number of pairs found, not the    \n"
    "                 pairs themselves.                                     \n"
    "                                                                       \n"
    "        --realtime  Prints out progress rapidly, on a single line.     \n"
    "                    Discovered results (eg full pairs) still get their \n"
    "                    Own line.                                          \n";

int n;
int *x;
int *p;

long count = -1;

long num_entries_since_last_update = 0;
long update_interval = -1;
char *update_suffix = "\n";

void (*print_x)(int, char *) = NULL;

void print_alpha(int zero_char, char *ending) {
    for (int i = 0; i < 2 *n; ++i) {
        int xi = x[i] < 0 ? -x[i] : x[i];
        int c = xi == 0 ? zero_char : xi - 1 + 'a';
        printf("%c", c);
    }
    printf("%s", ending);
}

void print_ints(int zero_char, char *ending) {
    for (int i = 0; i < 2 * n; ++i) {
        if (i) printf(" ");
        if (x[i]) {
            printf("%3d", x[i]);
        } else {
            printf("  %c", zero_char);
        }
    }
    printf("%s", ending);
}

// This returns the next index i > ell such that x[i] == 0.
int next_zero_index(ell) {
    for (int i = ell + 1;; ++i) {
        if (x[i] == 0) return i;
    }
}

void show_update_if_appropriate() {
    if (update_interval > 0) {
        num_entries_since_last_update++;
        if (num_entries_since_last_update > update_interval) {
            printf(" Checkpoint: ");
            print_x('.', "");
            printf("%s", update_suffix);
            fflush(stdout);
            num_entries_since_last_update = 0;
        }
    }
}

void alg_L(ell) {

    show_update_if_appropriate();

    if (ell == 2 * n) {
        if (count >= 0) {
            count++;
        } else {
            printf("Solution: ");
            print_x('0', "      \n");
        }
    }

    for (int j = 0, k = p[j]; k > 0; j = k, k = p[k]) {

        // Check bailout / skip conditions.
        if (ell + k + 1 >= 2 * n) return;
        if (x[ell + k + 1] != 0) continue;

        // Try x[ell] = k.
        x[ell] = k;
        x[ell + k + 1] = -k;
        p[j] = p[k];

        // Recursively look for more complete solutions.
        alg_L(next_zero_index(ell));

        // Prepare to try the next value.
        p[j] = k;
        x[ell + k + 1] = 0;
        x[ell] = 0;
    }
}

int main(int argc, char **argv) {

    if (argc < 2) {
        printf("\n%s\n", usage);
        return 0;
    }

    // Parse the command-line arguments.
    n = 4;
    print_x = print_ints;
    for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], "--realtime") == 0) {
            update_interval = 2e6;
            update_suffix = "\r";
        } else if (strcmp(argv[i], "--alpha") == 0) {
            print_x = print_alpha;
        } else if (strcmp(argv[i], "--checkpoints") == 0) {
            update_interval = 5e7;
            update_suffix = "\n";
        } else if (strcmp(argv[i], "--count") == 0) {
            count = 0;
        } else {
            n = atoi(argv[i]);
        }
    }
    if (n < 1) {
        printf("Bailing due to bad n value: %d.\n", n);
        return 1;
    }

    // Initialization.
    x = calloc(2 * n + 1, sizeof(int));
    p = calloc(n + 1, sizeof(int));
    for (int i = 0; i < n; ++i) p[i] = i + 1;

    // Run the algorithm!
    alg_L(0);

    if (count >= 0) {
        printf("Full count: %ld\n", count);
        printf("Half count: %ld\n", count / 2);
    }

    return 0;
}
