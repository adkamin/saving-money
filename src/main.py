from algorithm import find_min_cost
import sys
import time
import operator as op
from functools import reduce

def main():
    c = 0
    while True:
        c += 1
        start = time.process_time()
        if(find_min_cost() == -10):
            print(c)
            break
        end = time.process_time()
        print(f'Time elapsed: {end - start} seconds', file=sys.stderr)

def a(products, dividers):
    total = 0
    for d in range(dividers+1):
        total += ncr(products-1, d)
    return total

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2

if __name__ == '__main__':
    main()
