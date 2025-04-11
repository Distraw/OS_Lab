import os
import random
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('a', type=str)
    parser.add_argument('b', type=str)
    args = parser.parse_args()

    a = float(args.a)
    b = float(args.b)
    NUM = int(os.environ['NUM'])
    occurences = 0
    for i in range(NUM):
        if a < random.random() < b:
            occurences += 1

    print(occurences, end='')
    sys.exit(1)