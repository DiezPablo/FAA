from ClasificadorAG import ClasificadorAlgoritmoGenetico
from Datos import Datos
from EstrategiaParticionado import ValidacionSimple, ValidacionCruzada

def main():
    dataset = Datos("../Datasets/ejemplo2.data")
    clf = ClasificadorAlgoritmoGenetico(100, 100, numReglas=4)

    vs = ValidacionSimple(0.7)
    vs.creaParticiones(dataset)

    clf.calculo_intervalos(dataset)
    clf.transforma_dataset(dataset)

    champion = clf.entrenamiento(dataset, vs.particiones[0].indicesTrain)
    error,acierto = clf.clasifica(vs.particiones[0].indicesTest,champion)
    print(error)
    clf.graficas_fitness()


if __name__ == "__main__":
    main()