from time import perf_counter

class Temporizador():
    def __init__(self, method : str) -> None:
        self.method = method
        self.start = 0
        self.end = 0
        self.duracao = 0

    def start_timer(self):
        self.start = perf_counter()

    def stop_timer(self):
        self.end = perf_counter()
        self.duracao = self.end - self.start
        