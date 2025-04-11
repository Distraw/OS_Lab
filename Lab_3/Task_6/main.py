import os
import argparse
import random
import sys
import time
import signal

def child_task() -> None:
    if random.random() >= 0.5:
        print(f'{os.getpid()} достроково завершив роботу')
        return
    else:
        # Нескінченний цикл
        while True:
            time.sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--number', type=int, help="Number of child processes")
    args = parser.parse_args()

    child_process_count = 10
    if args.number and args.number > 0:
        child_process_count = args.number

    child_id = []
    for i in range(child_process_count):
        pid = os.fork()

        if pid == 0:
            child_task()
            sys.exit(1)
        else:
            child_id.append(pid)

    time.sleep(3)
    print('')
    for i in range(len(child_id)):
        if os.waitpid(child_id[i], os.WNOHANG)[0] != 0:
            print(f'[Процес {child_id[i]}] очищений')
            child_id[i] = -1

    time.sleep(5)
    print('')
    for child in child_id:
        if child != -1:
            if os.waitpid(child, os.WNOHANG)[0] == 0:
                print(f'[Процес {child}] остаточно завершений')
                os.kill(child, signal.SIGTERM)