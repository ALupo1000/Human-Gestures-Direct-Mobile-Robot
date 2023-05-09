
from collections import deque
import time

DEFAULT_LOCK = 20
queue = deque(maxlen=DEFAULT_LOCK * 5)
currently_executing = 0


def consecutive_on_queue(queue, element, amount):
    count = 1
    for queue_element in queue:
        if queue_element == element:
            count += 1
            if count == amount:
                return True
        else:
            return False 

def put_on_queue_to_execute(put_on_queue, stored_function, to_execute):
    global queue
    global currently_executing
    if consecutive_on_queue(queue, stored_function, DEFAULT_LOCK):
        to_execute()
    if put_on_queue():
        queue.append(stored_function)