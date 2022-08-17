import threading

global current_filter
current_filter = 1
global lock
lock = threading.Lock()

def change_filter(filter):
    global lock
    with lock:
        global current_filter
        current_filter = filter
        return current_filter