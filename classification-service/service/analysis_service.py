from model.pcb_flow import PCBFlow
from view.flow import executar_flow
from util.img_util import from_np_array_to_base64

def orchestrate_analysis(image, filtro):
    # orchestrate analysis
    print(f"Starting image analysis...")
    pcb_flow = PCBFlow(image, filtro)
    result_image, classification = executar_flow(pcb_flow)
    return from_np_array_to_base64(result_image), classification
