from ClasificadorAG import ClasificadorAlgoritmoGenetico
from Datos import Datos
from EstrategiaParticionado import ValidacionSimple, ValidacionCruzada
import random

def main():
    dataset = Datos("ejemplo1.data")
    clf = ClasificadorAlgoritmoGenetico(10, 10)

    clf.generar_poblacion(dataset)



if __name__ == "__main__":
    main()