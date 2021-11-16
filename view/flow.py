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
    start = time.time()
    
    # Detecção de bordas
    pcb_flow.img_bordas = deteccaoBordasService.tratar(pcb_flow)

    end = time.time()
    print("Corner")
    pcb_flow.tempos.append(end - start)
    print(end - start)

    # Normalização de cor
    pcb_flow.img_norm = normalizacaoService.tratar(pcb_flow)

    end = time.time()
    print("Normal")
    pcb_flow.tempos.append(end - start)
    print(end - start)

    # Thresholding
    pcb_flow.thrGray = thresholdService.tratar(pcb_flow)

    end = time.time()
    print("Thresold")
    pcb_flow.tempos.append(end - start)
    print(end - start)

    # Segmentação
    img, segList = segmentacaoService.tratar(pcb_flow)
    
    end = time.time()
    print("Segmentação")
    pcb_flow.tempos.append(end - start)
    print(end - start)

    return img
