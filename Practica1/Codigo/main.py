
from Datos import Datos
from EstrategiaParticionado import EstrategiaParticionado, ValidacionSimple, ValidacionCruzada
from Clasificador import Clasificador, ClasificadorNaiveBayes
from matplotlib import pyplot as plt
import numpy as np
from sklearnNB import validacion_cruzada_sklearn,validacion_simple_sklearn,nb_sklearn, error, nb_sklearn_validacion_cruzada


def main():

    dataset = Datos('../Datasets/tic-tac-toe.data')
    #estrategia = ValidacionSimple(0.7)
    #estrategia.creaParticiones(dataset)
    #estrategia = ValidacionCruzada(4)
        #nb = ClasificadorNaiveBayes(True)
        #nb.entrenamiento(dataset, estrategia.particiones[0].indicesTrain)
        #pred = nb.clasifica(dataset,estrategia.particiones[0].indicesTest)

    #err = nb.error(dataset.extraeDatos(estrategia.particiones[0].indicesTest), pred)
    #print("Error", err)

    #matriz = nb.matrizConfusion(dataset, estrategia.particiones[0].indicesTest,pred)
    #nb.curva_roc(matriz)

    #particiones = validacion_cruzada_sklearn(dataset,4)
    #for particion in particiones:
    #    print(particion)


    # Prueba SKLearn validacion simple
    #X_train, X_test, y_train, y_test = validacion_simple_sklearn(dataset, 0.75)
    #pred =  nb_sklearn(X_train, y_train, X_test, tipo = 'Multinomial', laplace=True)
    #print(error(pred,y_test))

    # NB SK Cross Val
    #predict = nb_sklearn_validacion_cruzada(X_train, y_train, 4)
    #print(1-np.mean(predict))
    

    estrategia = ValidacionCruzada(4)
    nb = ClasificadorNaiveBayes(True)
    estrategia.creaParticiones(dataset)
    for particion in estrategia.particiones:
        nb.entrenamiento(dataset, particion.indicesTrain)
        pred = nb.clasifica(dataset,particion.indicesTest)
        matriz = nb.matrizConfusion(dataset, particion.indicesTest,pred)

    #nb.curvaROC()



if __name__ == "__main__":
    main()