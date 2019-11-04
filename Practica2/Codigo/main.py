
from Datos import Datos
from EstrategiaParticionado import EstrategiaParticionado, ValidacionSimple, ValidacionCruzada
from Clasificador import Clasificador, ClasificadorNaiveBayes
from matplotlib import pyplot as plt
import numpy as np
from sklearnNB import validacion_cruzada_sklearn,validacion_simple_sklearn,nb_sklearn, error, nb_sklearn_validacion_cruzada,matriz_confusion_sklearn,curvaROC_sklearn


def main():

    dataset = Datos('example1.data')
    datosNormalizar = dataset.extraeDatos([0,1,2])
    print(datosNormalizar)
    #esta = dataset.calcularMediasDesv(datosNormalizar)
    dataNorm, esta = dataset.normalizarDatos(datosNormalizar)
    print(dataNorm)
    #print(esta)
    #print(dataNorm)


if __name__ == "__main__":
    main()