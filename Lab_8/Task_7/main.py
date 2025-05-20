import threading
import random
import time

class Task:
    def __init__(self):
        self.priority = 0

    def execute(self):
        pass

class FindFactorial(Task):
    def __init__(self, user_input: int):
        super().__init__()
        self._user_input = user_input

    def execute(self):
        return self.calculate()

    def calculate(self):
        if self._user_input <= 0:
            return -1

        result = 1
        for j in range(1, self._user_input + 1):
            result *= j

        return result

    @property
    def user_input(self):
        return self._user_input

thr_amount = 10
create_thr = []
execute_thr = []

task_query_lock = threading.Lock()
task_query = []

task_result_lock = threading.Lock()
task_result = []

def thr_create_task():
    new_task = FindFactorial(random.randint(2, 50))

    with task_query_lock:
        task_query.append(new_task)

def thr_execute_task():
    with task_query_lock:
        current_task = task_query.pop()

    start = time.time()
    calculation_result = current_task.execute()
    end = time.time()

    with task_result_lock:
        task_result.append([threading.get_ident(), end - start, current_task.user_input, calculation_result])

if __name__ == "__main__":
    for i in range(thr_amount):
        t = threading.Thread(target=thr_create_task)
        t.start()
        create_thr.append(t)

    for i in range(thr_amount):
        t = threading.Thread(target=thr_execute_task)
        t.start()
        execute_thr.append(t)

    for i in range(thr_amount):
        create_thr[i].join()
        execute_thr[i].join()

    for thr_id, execution_time, user_input, result in task_result:
        print(f"Потік[{thr_id}], час виконання: {execution_time}c. Факторіал {user_input} = {result}")