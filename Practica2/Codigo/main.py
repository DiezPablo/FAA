
from Datos import Datos
from EstrategiaParticionado import EstrategiaParticionado, ValidacionSimple, ValidacionCruzada
from Clasificador import Clasificador, ClasificadorNaiveBayes, ClasificadorVecinosProximos
from matplotlib import pyplot as plt
import numpy as np
from sklearnNB import validacion_cruzada_sklearn,validacion_simple_sklearn,nb_sklearn, error, nb_sklearn_validacion_cruzada,matriz_confusion_sklearn,curvaROC_sklearn


def main():

    dataset = Datos('example1.data')

    knn = ClasificadorVecinosProximos(3)
    estrategia = ValidacionSimple(0.7)
    estrategia.creaParticiones(dataset)

    knn.entrenamiento(dataset, estrategia.particiones[0].indicesTrain)

    #print(esta)
    #print(dataNorm)


if __name__ == "__main__":
    main()