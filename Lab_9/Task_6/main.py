import threading
import random
import time

buffer = []
buffer_size = 5

lock = threading.Lock()
empty_slots = threading.Semaphore(buffer_size)
filled_slots = threading.Semaphore(0)

stop_event = threading.Event()

timeout_delay = 0.6
thread_sleep_time = 0.2

def consumer():
    while not stop_event.is_set():
        time.sleep(thread_sleep_time)
        acquired = filled_slots.acquire(timeout=timeout_delay)

        if not acquired:
            if stop_event.is_set():
                empty_slots.release()
                break
            else:
                continue

        if stop_event.is_set():
            empty_slots.release()
            break

        with lock:
            item = buffer.pop()
            print("Consumer Thread: consumed: ", item)
        empty_slots.release()

def producer():
    while not stop_event.is_set():
        time.sleep(thread_sleep_time)

        acquired = empty_slots.acquire(timeout=timeout_delay)

        if not acquired:
            if stop_event.is_set():
                empty_slots.release()
                break
            else:
                continue

        if stop_event.is_set():
            filled_slots.release()
            break

        with lock:
            random_number = random.randint(1, 100)
            print(f"Thread [{threading.get_ident()}]: produced: {random_number}, [{len(buffer)}]")
            buffer.append(random_number)
        filled_slots.release()


if __name__ == '__main__':
    consumer_thread = threading.Thread(target=consumer)
    producer_threads = []

    for i in range(3):
        producer_threads.append(threading.Thread(target=producer))
        producer_threads[i].start()

    consumer_thread.start()

    time.sleep(1)
    stop_event.set()

    consumer_thread.join()
    for element in producer_threads:
        element.join()