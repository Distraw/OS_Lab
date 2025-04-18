import os
import signal
import time

# Глобальні лічильники для сигналів
usr1_count = 0
rtmin_count = 0


def handle_usr1(signum, frame):
    global usr1_count
    usr1_count += 1


def handle_rtmin(signum, frame):
    global rtmin_count
    rtmin_count += 1


def child_process():
    global usr1_count, rtmin_count

    #signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGUSR1, signal.SIGRTMIN})

    print(f"Дочірній процес (PID: {os.getpid()}) готовий до отримання сигналів.")

    os.kill(os.getppid(), signal.SIGUSR2)

    time.sleep(5)

    #signal.pthread_sigmask(signal.SIG_UNBLOCK, {signal.SIGUSR1, signal.SIGRTMIN})

    print(f"Дочірній процес (PID: {os.getpid()}) обробив сигнали:")
    print(f"SIGUSR1: {usr1_count} сигналів")
    print(f"SIGRTMIN: {rtmin_count} сигналів")


def parent_process(child_pid):
    print(f"Батьківський процес (PID: {os.getpid()}) чекає на готовність дитини.")
    signal.pause()

    for _ in range(10):
        os.kill(child_pid, signal.SIGUSR1)
    for _ in range(10):
        os.kill(child_pid, signal.SIGRTMIN)

    time.sleep(5)
    os.kill(child_pid, signal.SIGTERM)

    print("Батьківський процес завершив свою роботу.")

if __name__ == "__main__":
    pid = os.fork()

    if pid == 0:
        signal.signal(signal.SIGUSR1, handle_usr1)
        signal.signal(signal.SIGRTMIN, handle_rtmin)
        signal.signal(signal.SIGTERM, lambda signum, frame: exit(0))

        child_process()

    else:
        parent_process(pid)