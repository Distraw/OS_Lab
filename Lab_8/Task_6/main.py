import threading

left_border = int(input("Введіть ліву границю: "))
right_border = int(input("Введіть праву границю: "))

precision_parts = 1000

increment = (right_border - left_border) / precision_parts
result = 0.0
result_lock = threading.Lock()

def f(x: float):
    return (x ** 2 + 34) / (x - 1)

def calculate_rectangle_at(x: float):
    global result
    rectangle_area = f(x) * increment
    with result_lock:
        result += rectangle_area

if __name__ == '__main__':
    t = []
    for i in range(precision_parts):
        new_thread = threading.Thread(target=calculate_rectangle_at, args=[left_border + (i * increment),])
        t.append(new_thread)
        t[i].start()

    for element in t:
        element.join()

    print(result)