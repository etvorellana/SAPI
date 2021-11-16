import time

class Temporizador():
    def __init__(self, method) -> None:
        self.method = method
        self.start = 0
        self.end = 0

    def start_timer(self, method_str):
        self.method = method_str
        self.start = time.perf_count()

    def stop_timer(self, method_str):
        self.end = time.perf_count()
        duracao = self.end - self.start
        return duracao