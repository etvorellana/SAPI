import time
from model.pcb_flow import PCBFlow
from model.temporizador import Temporizador
from service.deteccao_bordas_service import DeteccaoBordasService
from service.normalizacao_service import NormalizacaoService
from service.threshold_service import ThresholdService
from service.segmentacao_service import SegmentacaoService

deteccaoBordasService : DeteccaoBordasService = DeteccaoBordasService()
normalizacaoService : NormalizacaoService = NormalizacaoService()
thresholdService : ThresholdService = ThresholdService()
segmentacaoService : SegmentacaoService = SegmentacaoService()

def executar_flow(pcb_flow : PCBFlow):
    # Detecção de bordas
    temporizador : Temporizador = Temporizador("Corner")
    temporizador.start_timer()

    pcb_flow.img_bordas = deteccaoBordasService.tratar(pcb_flow)

    temporizador.stop_timer()
    pcb_flow.tempos.append(temporizador)


    # Normalização de cor
    temporizador : Temporizador = Temporizador("Normalização")
    temporizador.start_timer()

    pcb_flow.img_norm = normalizacaoService.tratar(pcb_flow)

    temporizador.stop_timer()
    pcb_flow.tempos.append(temporizador)


    # Thresholding
    temporizador : Temporizador = Temporizador("Thresold")
    temporizador.start_timer()

    pcb_flow.thrGray = thresholdService.tratar(pcb_flow)

    temporizador.stop_timer()
    pcb_flow.tempos.append(temporizador)


    # Segmentação
    temporizador : Temporizador = Temporizador("Segmentação")
    temporizador.start_timer()

    img, segList = segmentacaoService.tratar(pcb_flow)

    temporizador.stop_timer()
    pcb_flow.tempos.append(temporizador)
    
    
    pcb_flow.print_timers()
    return img
