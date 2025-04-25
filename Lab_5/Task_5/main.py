import os
import time
import sys

child_processes_number = 5

if __name__ == "__main__":
    read_pipe, write_pipe = os.pipe()
    children_pids = []

    for i in range(child_processes_number):
        pid = os.fork()
        if pid == 0:
            os.close(read_pipe)
            print(f"Дочірній процес {i} почав роботу")

            # Робота дочірнього процесу

            os.write(write_pipe, b'1')
            print(f"Дочірній процес {i} завершив роботу")

            sys.exit(0)
        else:
            children_pids.append(pid)

    os.close(write_pipe)
    print("\nБатьківський процес очікує сигналу\n")

    for _ in range(child_processes_number):
        os.read(read_pipe, 1)

    print("Усі дочірні процеси завершили роботу")
    print("Батьківський процес продовжує роботу")

    for pid in children_pids:
        os.waitpid(pid, 0)