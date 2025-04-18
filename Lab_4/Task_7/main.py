import time
import signal
import os
import sys

def read_config():
    with open('config.txt', 'r') as f:
        symb = f.readline().strip()
        rep = int(f.readline())

    return symb, rep

is_read_config = False
def sighup_handler(signum, frame):
    global is_read_config
    is_read_config = True

if __name__ == '__main__':
    pid = os.fork()

    if pid != 0:
        sys.exit(0)

    time.sleep(1)
    print('Child process ID: ', os.getpid())

    config_symbol, config_repeat = read_config()
    signal.signal(signal.SIGHUP, sighup_handler)
    while True:
        time.sleep(3)
        print('Symbol=', config_symbol, '\tRepeat=', config_repeat)
        if is_read_config:
            is_read_config = False
            config_symbol, config_repeat = read_config()