import os
import time
import signal
import sys

sigrtmin_occurence = 0
sigusr1_occurence = 0

def sigrtmin_handler(signum, frame):
    global sigrtmin_occurence
    sigrtmin_occurence += 1

def sigusr1_handler(signum, frame):
    global sigusr1_occurence
    sigusr1_occurence += 1

def parent_process(signum, frame):
    print("Parent: sending signals...")
    for _ in range(10):
        os.kill(pid, signal.SIGRTMIN)
    for _ in range(10):
        os.kill(pid, signal.SIGUSR1)

    print("Parent: signals were sent")
    time.sleep(3)

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        signal.signal(signal.SIGRTMIN, sigrtmin_handler)
        signal.signal(signal.SIGUSR1, sigusr1_handler)

        signal.pthread_sigmask(signal.SIG_SETMASK, {signal.SIGRTMIN, signal.SIGUSR1})

        print("Child: ready to receive signals")
        os.kill(os.getppid(), signal.SIGUSR2)

        time.sleep(2)

        signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGRTMIN, signal.SIGUSR1})
        print("Child: signals received")

        print("SIGRTMIN: ", sigrtmin_occurence)
        print("SIGUSR1: ", sigusr1_occurence)
        sys.exit(0)
    else:
        signal.signal(signal.SIGUSR2, parent_process)
        signal.pause()