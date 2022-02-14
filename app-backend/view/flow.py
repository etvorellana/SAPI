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
    pcb_flow.start_timer("Corner")

    pcb_flow.img_bordas = deteccaoBordasService.tratar(pcb_flow)

    pcb_flow.stop_timer("Corner")


    # Normalização de cor
    pcb_flow.start_timer("Normalização")

    pcb_flow.img_norm = normalizacaoService.tratar(pcb_flow)

    pcb_flow.stop_timer("Normalização")


    # Thresholding
    pcb_flow.start_timer("Thresold")

    pcb_flow.thrGray = thresholdService.tratar(pcb_flow)

    pcb_flow.stop_timer("Thresold")


    # Segmentação
    pcb_flow.start_timer("Segmentação")

    img, segList = segmentacaoService.tratar(pcb_flow)

    pcb_flow.stop_timer("Segmentação")
    
    
    pcb_flow.print_timers()
    return img
