import os
import sys
import struct
import signal

parent_fifo = '/tmp/parent_fifo'
child_fifo = '/tmp/child_fifo'

if __name__ == "__main__":
    if not os.path.exists(parent_fifo):
        os.mkfifo(parent_fifo)

    if not os.path.exists(child_fifo):
        os.mkfifo(child_fifo)

    pid = os.fork()
    if pid == 0:
        while True:
            child_read = open(parent_fifo, 'rb')

            # Спочатку отримуємо розмір рядку
            parent_string_length = struct.unpack('i', child_read.read(4))[0]

            # Тепер отримуємо сам рядок
            parent_string = child_read.read(parent_string_length).decode('utf-8')

            parent_string = parent_string.upper()

            child_write = open(child_fifo, 'wb')
            child_write.write(parent_string.encode('utf-8'))
            child_write.flush()
    else:
        while True:
            user_string = input('>')

            if user_string == 'stop':
                os.kill(pid, signal.SIGTERM)
                sys.exit(0)

            parent_write = open(parent_fifo, 'wb')

            # Спочатку треба передати розмір рядку
            parent_write.write(struct.pack('i', len(user_string.encode('utf-8'))))

            # Тепер передаємо сам рядок
            parent_write.write(user_string.encode('utf-8'))
            parent_write.flush()

            parent_read = open(child_fifo, 'rb')

            child_output = parent_read.read(len(user_string.encode('utf-8'))).decode('utf-8')
            print(f"Child output :: {child_output}")