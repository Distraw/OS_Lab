import os
import sys
import struct
import signal

if __name__ == "__main__":
    child_read, parent_write = os.pipe()
    parent_read, child_write = os.pipe()

    pid = os.fork()
    if pid == 0:
        os.close(parent_write)
        os.close(parent_read)

        while True:
            # Спочатку отримуємо розмір рядку
            parent_string_length = struct.unpack('i', os.read(child_read, 4))[0]

            # Тепер отримуємо сам рядок
            parent_string = os.read(child_read, parent_string_length).decode('utf-8')

            parent_string = parent_string.upper()

            os.write(child_write, parent_string.encode('utf-8'))
    else:
        os.close(child_write)
        os.close(child_read)

        while True:
            user_string = input('>')

            if user_string == 'stop':
                os.kill(pid, signal.SIGTERM)
                sys.exit(0)

            # Спочатку треба передати розмір рядку
            os.write(parent_write, struct.pack('i', len(user_string.encode('utf-8'))))

            # Тепер передаємо сам рядок
            os.write(parent_write, user_string.encode('utf-8'))

            child_output = os.read(parent_read, len(user_string.encode('utf-8'))).decode('utf-8')
            print(f"Child output :: {child_output}")