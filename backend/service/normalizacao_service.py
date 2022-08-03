from service.filtros.dct_service import DctService
from model.pcb_flow import PCBFlow

class NormalizacaoService():
    
    def normIllumination(self, pcb_flow : PCBFlow, DCTdistance = 10, dataType = "float64", base = 2):
        dctService = DctService()

        filtered_img = dctService.dctFilter(pcb_flow.img_bordas, DCTdistance, dataType, base)

        return filtered_img