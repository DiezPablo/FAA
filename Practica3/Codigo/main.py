from ClasificadorAG import ClasificadorAlgoritmoGenetico
from Datos import Datos
from EstrategiaParticionado import ValidacionSimple, ValidacionCruzada
import random
import numpy as np
def main():
    dataset = Datos("ejemplo1.data")
    clf = ClasificadorAlgoritmoGenetico(10, 5)

    vs = ValidacionSimple(0.7)
    vs.creaParticiones(dataset)


    clf.generar_poblacion(dataset)
    clf.calculo_intervalos(dataset)
    clf.transforma_dataset(dataset)
    clf.fitness(vs.particiones[0].indicesTrain)

    print(clf.poblacion)

if __name__ == "__main__":
    main()