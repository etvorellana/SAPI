from time import perf_counter
from .temporizador import Temporizador
class PCBFlow():
    def __init__(self, src, borda : int = 1, filtro : int = 1) -> None:
        self.img_src = src
        self.img_cinza = []   # Não usado
        self.img_bordas = []
        self.img_norm = []
        self.thrGray = []
        self.tempos = []
        self.borda = borda
        self.filtro = filtro

    def start_timer(self, method : str):
        for tempo in self.tempos:
            if tempo.method == method:
                tempo.start_timer()
                return
        temporizador : Temporizador = Temporizador(method)
        temporizador.start_timer()
        self.tempos.append(temporizador)
    
    def stop_timer(self, method : str) -> bool:
        for tempo in self.tempos:
            if tempo.method == method:
                tempo.stop_timer()
                return 0
        return -1
    
    def print_timers(self):
        print("------------------------")
        for tempo in self.tempos:
            print("Método: ", tempo.method)
            print("Start: ", tempo.start)
            print("End: ", tempo.end)
            print("Duração: ", tempo.duracao)
            print()

