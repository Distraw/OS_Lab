import os
import mmap
import pickle
import string
import sys
import random
import fcntl
import struct

LOCK_FILE_PATH = './lock_file'
RANDOM_STRING_LENGTH = 5
MAX_MAP_LENGTH = 4096
NUM_CHILDREN = 3

children = []

shared_mem = mmap.mmap(-1, MAX_MAP_LENGTH)

def parent_process():
    for child_pid in children:
        os.waitpid(child_pid, 0)

    print('Виведення результатів:')
    used_space = struct.unpack('I', shared_mem[:4])[0]
    i = 0
    pos = 4
    while pos < 4 + used_space:
        pickled_len = struct.unpack('I', shared_mem[pos:pos+4])[0]
        pos += 4

        unpickled_data = pickle.loads(shared_mem[pos: pos + pickled_len])
        print('N', i, ': ', unpickled_data, '  ', pickled_len)

        pos += pickled_len
        i += 1

    sys.exit(0)




def child_process():
    random_string = ''.join(random.choices(string.ascii_letters, k=RANDOM_STRING_LENGTH))
    current_pid = os.getpid()

    data_to_map = {'PID': current_pid, "Random_string": random_string}
    pickled = pickle.dumps(data_to_map)
    pickled_len = len(pickled)

    with open(LOCK_FILE_PATH, 'r+') as lock_fd:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)

        used_space = struct.unpack('I', shared_mem[:4])[0]

        if used_space + 4 + 4 + pickled_len > MAX_MAP_LENGTH:
            print('ПЕРЕВИЩЕНО РОЗМІР ВИДІЛЕНОЇ ПАМ\'ЯТІ: ', used_space + 4 + 4 + pickled_len)
            print('Максимальний розмір області: ', MAX_MAP_LENGTH)
            sys.exit(0)

        shared_mem[4 + used_space:4 + used_space + 4] = struct.pack('I', pickled_len)
        shared_mem[4 + used_space + 4:4 + used_space + 4 + pickled_len] = pickled

        new_used_space = used_space + 4 + pickled_len
        shared_mem[:4] = struct.pack('I', new_used_space)

        fcntl.flock(lock_fd, fcntl.LOCK_UN)

if __name__ == '__main__':
    open(LOCK_FILE_PATH, 'a').close()

    used = struct.pack('I', 0)
    shared_mem[:4] = used

    for _ in range(NUM_CHILDREN):
        pid = os.fork()
        if pid == 0:
            child_process()
            sys.exit(0)
        else:
            children.append(pid)

    parent_process()