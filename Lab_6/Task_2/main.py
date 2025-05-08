import os
import mmap
import pickle
import string
import sys
import random
import fcntl
import time
import signal

from PIL.PngImagePlugin import MAX_TEXT_CHUNK

FILE_PATH = './mmap_file.txt'
RANDOM_STRING_LENGTH = 16
NUM_CHILDREN = 3
MAX_ITERATIONS = 4
BLOCK_SIZE = len(pickle.dumps(' ' * RANDOM_STRING_LENGTH))
MAP_SIZE = BLOCK_SIZE * NUM_CHILDREN

children = []

def parent_process():
    file = open(FILE_PATH, 'r+b')
    shared_mem = mmap.mmap(file.fileno(), MAP_SIZE)

    for j in range(MAX_ITERATIONS):
        time.sleep(1)

        print('Ітерація', j)
        pos = 0
        while pos < MAP_SIZE:
            fcntl.lockf(file, fcntl.LOCK_EX, BLOCK_SIZE, pos)

            unpickled = pickle.loads(shared_mem[pos: pos + BLOCK_SIZE])
            print(unpickled)

            fcntl.lockf(file, fcntl.LOCK_UN, BLOCK_SIZE, pos)
            pos += BLOCK_SIZE

    file.close()
    for child in children:
        os.kill(child, signal.SIGTERM)
        os.waitpid(child, 0)
    sys.exit(0)

def child_process(iterator: int):
    with open(FILE_PATH, 'r+b') as file:
        shared_mem = mmap.mmap(file.fileno(), MAP_SIZE)
        while True:
            time.sleep(0.1)

            random_string = ''.join(random.choices(string.ascii_letters, k=RANDOM_STRING_LENGTH))
            pickled = pickle.dumps(random_string)
            fcntl.lockf(file, fcntl.LOCK_EX, BLOCK_SIZE, iterator * BLOCK_SIZE)

            shared_mem[iterator * BLOCK_SIZE: iterator * BLOCK_SIZE + BLOCK_SIZE] = pickled

            fcntl.lockf(file, fcntl.LOCK_UN, BLOCK_SIZE, iterator * BLOCK_SIZE)



if __name__ == '__main__':
    with open(FILE_PATH, 'wb') as f:
        f.truncate(MAP_SIZE)

    for i in range(NUM_CHILDREN):
        pid = os.fork()
        if pid == 0:
            child_process(i)
            sys.exit(0)
        else:
            children.append(pid)

    parent_process()