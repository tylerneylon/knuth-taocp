all: alg_L

alg_L: alg_L.c
	cc -O3 alg_L.c -o alg_L
