import threading
import os
import time

class MyLock:
    def __init__(self):
        self._read, self._write = os.pipe()

    def lock(self):
        os.read(self._read, 1)

    def release(self):
        os.write(self._write, b'1')

lock = MyLock()

def thread_task(name: str):
    print(f'[{name}] Чекає на розблокування...')
    lock.lock()
    print(f'[{name}] Виконує роботу...')
    time.sleep(1)
    print(f'[{name}] Завершив виконання')



if __name__ == '__main__':
    t = threading.Thread(target=thread_task, args=(f'Child_thread', ))
    t.start()

    time.sleep(2)
    print('[Main] віддає сигнал на розблокування')
    lock.release()

    print('[Main] очікує на завершення \'Child_thread\'')
    t.join()

    print('[Main] завершено')