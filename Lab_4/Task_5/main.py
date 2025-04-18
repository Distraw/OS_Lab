import os
import signal
import sys
import argparse
import time
import platform
import shutil

def alarm_handler(signum, frame):
    if platform.system() == 'Linux' and (shutil.which('notify-send') is not None and ('DISPLAY' in os.environ or 'WAYLAND_DISPLAY' in os.environ)):
        os.system(f'notify-send "{message}"')
    else:
        print(message)

    sys.exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--seconds', type=int, required=True, help='Time in seconds')
    parser.add_argument('-m', '--message', type=str, required=True, help='Message after timer run out')
    args = parser.parse_args()

    seconds = args.seconds
    message = args.message

    pid = os.fork()
    if pid == 0:
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(seconds)
        signal.pause()
    else:
        time.sleep(seconds + 1)
        sys.exit(0)