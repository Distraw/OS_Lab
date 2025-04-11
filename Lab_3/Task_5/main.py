import os

def my_system(cmd):
    pid = os.fork()  # створюємо дочірній процес

    if pid == 0:
        os.execve('/bin/sh', ['/bin/sh', '-c', cmd], os.environ)
        os._exit(1)
    else:
        pid, status = os.wait()

my_system(input('>>'))