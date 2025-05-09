import threading
import math

def catalan_number(n: int) -> int:
    return math.comb(2*n, n) // (n + 1)

def is_prime(value_to_check: int) -> bool:
    if value_to_check <= 1:
        return False
    if value_to_check <= 3:
        return True
    if value_to_check % 2 == 0 or value_to_check % 3 == 0:
        return False

    i = 5
    while i * 2 <= value_to_check:
        if value_to_check % i == 0:
            return False
        i += 2

    return True

catalan_result = []
prime_result = []

def catalan_thread(n: int):
    for i in range(n):
        catalan_result.append(catalan_number(i))

def prime_thread(n: int):
    num = 0
    i = 0
    while i < n:
        if is_prime(num):
            prime_result.append(num)
            i += 1
        num += 1


if __name__ == '__main__':
    catalan_t = threading.Thread(target=catalan_thread, args=(15, ))
    prime_t = threading.Thread(target=prime_thread, args=(15, ))

    catalan_t.start()
    prime_t.start()

    catalan_t.join()
    prime_t.join()

    print(catalan_result)
    print(prime_result)