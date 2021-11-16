import sys
import argparse
import cv2 as cv
from model.pcb_flow import PCBFlow
from util.img_util import takepic, loadImage
from view.flow import executar_flow

def main(argv):
    ##  Recebimento dos argumentos
    parser = argparse.ArgumentParser(description = 'Detecção de solda')
    parser.add_argument('--arquivo', action = 'store', dest = 'src', default = 'foto', required = False, help = 'Nome do arquivo de imagem ou "foto" para utilizar a camera')
    parser.add_argument('-filtro', type = int, action = 'store', dest = 'filtro', default = 1, required = False, help = 'Tipo se filtro a ser aplicado: 1- Sem Filtro; 2 - Median Blur; 3 - Gaussian Blur ')
    parser.add_argument('-borda', type = int, action = 'store', dest = 'borda', default = 1, required = False, help = 'Tipo de detecção de borda a ser aplicado: 1- Corner Harris; 2 - Hough Lines')
    
    arguments = parser.parse_args()

    ##  Verifica se carrega o arquivo ou tira uma foto
    if (arguments.src == 'foto'):
        #srcGrey, srcRGB = takepic() #   Chama função da camera
        srcRGB = takepic() #   Chama função da camera
        outFile = "seg_saida.png"
    else:
        #srcGrey, srcRGB = loadImage(arguments.src) # Carrega Imagem
        srcRGB = loadImage(arguments.src) # Carrega Imagem
        # outFile = "seg_" + arguments.src
        outFile = "seg_test.png"
    
    # Instanciando objeto do PCB
    pcb_flow : PCBFlow = PCBFlow(srcRGB, arguments.borda, arguments.filtro)
    
    # Executando flow de processamento
    img = executar_flow(pcb_flow)

    # Salvando imagem resultante
    cv.imwrite(outFile, img)
    return 0

if __name__ == "__main__":
    main(sys.argv[1:])