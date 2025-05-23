import threading
import random
import time

buffer = []
buffer_size = 5
stop_event = threading.Event()

lock = threading.Lock()
is_buffer_filled = False

def producer():
    global is_buffer_filled

    while not stop_event.is_set():
        time.sleep(0.1)
        with lock:
            if is_buffer_filled:
                continue

            if len(buffer) >= buffer_size:
                is_buffer_filled = True
                continue

            random_number = random.randint(1, 100)
            print(f'[{threading.get_ident()}] Згенеровано: {random_number}')
            buffer.append(random_number)

def consumer():
    global is_buffer_filled, buffer

    while not stop_event.is_set():
        time.sleep(0.2)

        with lock:
            if not is_buffer_filled:
                continue

            print('Отримано: ', buffer)
            buffer.clear()
            is_buffer_filled = False

if __name__ == '__main__':
    consumer_thread = threading.Thread(target=consumer)
    consumer_thread.start()

    producer_threads = []
    for i in range(0, buffer_size):
        producer_threads.append(threading.Thread(target=producer))
        producer_threads[i].start()

    time.sleep(1)
    stop_event.set()

    consumer_thread.join()
    for i in range(0, buffer_size):
        producer_threads[i].join()