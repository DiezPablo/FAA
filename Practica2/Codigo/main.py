
from Datos import Datos
from EstrategiaParticionado import EstrategiaParticionado, ValidacionSimple, ValidacionCruzada
from Clasificador import Clasificador, ClasificadorNaiveBayes, ClasificadorVecinosProximos, ClasificadorRegresionLogistica
from matplotlib import pyplot as plt
import numpy as np
from sklearn_RegLog_Knn import validacion_simple_sklearn, knn_val_simple, knn_val_cruzada, validacion_simple_sklearn, regresionLog_val_cruzada,regresionLog_val_simple, error
from plotModel import plotModel

def main():

    dataset = Datos('example1.data')
    estrategia = ValidacionSimple(0.7)
    estrategia.creaParticiones(dataset)

    #knn = ClasificadorVecinosProximos(3)
    #knn.entrenamiento(dataset, estrategia.particiones[0].indicesTrain)
    #pred = knn.clasifica(dataset.datos,estrategia.particiones[0].indicesTest)
    #print(pred)
    #error = knn.error(dataset.extraeDatos(estrategia.particiones[0].indicesTest), pred)
    #print(error)

    #x = dataset.datos[estrategia.particiones[0].indicesTrain, 0]
    #y = dataset.datos[estrategia.particiones[0].indicesTrain, 1]
    #clase = dataset.datos[estrategia.particiones[0].indicesTrain, -1] != 0
    #plotModel(x, y, clase, knn, "title")

    logistic_reg = ClasificadorRegresionLogistica(0.5,250)
    logistic_reg.entrenamiento(dataset,estrategia.particiones[0].indicesTrain)
    pred = logistic_reg.clasifica(dataset.datos,estrategia.particiones[0].indicesTest)
    print(pred)
    error = logistic_reg.error(dataset.extraeDatos(estrategia.particiones[0].indicesTest),pred)
    print(error)
    matriz = logistic_reg.matrizConfusion(dataset,estrategia.particiones[0].indicesTest,pred)
    print(matriz)
    logistic_reg.curvaROC()

    #X_train, X_test, y_train, y_test = validacion_simple_sklearn(dataset, 0.7)
    #pred = knn_val_simple(X_train, y_train, X_test, 3)
    #print(error(pred, y_test))

    #X = dataset.datos[:, :-1]
    #y = dataset.datos[:, -1]

    #acierto, _ = knn_val_cruzada(X, y, 5, 3)

    #error = 0
    #for porc in acierto:
    #    error += (1 - porc)

    #print(error/len(acierto))

    #X_train, X_test, y_train, y_test = validacion_simple_sklearn(dataset, 0.7)
    #pred = regresionLog_val_simple(X_train, y_train, X_test)
    #print(error(pred, y_test))

    #X = dataset.datos[:, :-1]
    #y = dataset.datos[:, -1]

    #acierto, _ = regresionLog_val_cruzada(X, y, 3)

    #error = 0
    #for porc in acierto:
    #    error += (1 - porc)

    #print(error/len(acierto))




if __name__ == "__main__":
    main()
    print(error)
