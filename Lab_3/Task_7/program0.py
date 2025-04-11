import os
import subprocess
import random
import argparse

if __name__ == '__main__':
    print(os.getcwd())
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', type=int, required=True)
    parser.add_argument('-num', type=int, required=True)
    args = parser.parse_args()

    os.environ['NUM'] = str(args.num)

    step = (1 / args.n)
    result = []
    for i in range(args.n):
        result.append(subprocess.Popen(['python3', 'program1.py', str(step * i), str(step * i + step)],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ.copy()))

    for i, proc in enumerate(result):
        stdout, stderr = proc.communicate()
        print(f"[Процес {i}] Статус: {proc.returncode}")
        print(f"[Процес {i}] STDOUT: {stdout.decode()}")
        print(f"[Процес {i}] STDERR:\n{stderr.decode()}")

    for i in range(len(result)):
        result[i].stdout.close()
        result[i].stderr.close()