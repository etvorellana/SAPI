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
    
    def print_timers(self):
        for tempo in self.tempos:
            print("Método: ", tempo.method)
            print("Start: ", tempo.start)
            print("End: ", tempo.end)
            print("Duração: ", tempo.duracao)
            print()

