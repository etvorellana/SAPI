from model.pcb_flow import PCBFlow
from service.deteccao_bordas_service import DeteccaoBordasService
from service.normalizacao_service import NormalizacaoService
from service.threshold_service import ThresholdService
from service.segmentacao_service import SegmentacaoService
from service.classificacao_service import ClassificacaoService

deteccaoBordasService : DeteccaoBordasService = DeteccaoBordasService()
normalizacaoService : NormalizacaoService = NormalizacaoService()
thresholdService : ThresholdService = ThresholdService()
segmentacaoService : SegmentacaoService = SegmentacaoService()
classificacaoService : ClassificacaoService = ClassificacaoService()

def executar_flow(pcb_flow : PCBFlow):
    # Detecção de bordas
    pcb_flow.start_timer("Corner")

    pcb_flow.img_bordas = deteccaoBordasService.tratar(pcb_flow)

    pcb_flow.stop_timer("Corner")


    # Normalização de cor
    pcb_flow.start_timer("Normalização")

    pcb_flow.img_norm = normalizacaoService.normIllumination(pcb_flow)

    pcb_flow.stop_timer("Normalização")


    # Thresholding
    pcb_flow.start_timer("Thresold")

    pcb_flow.thrGray = thresholdService.tratar(pcb_flow)

    pcb_flow.stop_timer("Thresold")


    # Segmentação
    pcb_flow.start_timer("Segmentação")

    img, classificacao, qtd_soldas = segmentacaoService.tratar(pcb_flow)

    pcb_flow.stop_timer("Segmentação")

    classificacao = {"qtd_soldas": qtd_soldas, "classificacao": classificacao}
    pcb_flow.print_timers()
    return img, classificacao
