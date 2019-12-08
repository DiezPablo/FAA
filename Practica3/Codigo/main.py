from ClasificadorAG import ClasificadorAlgoritmoGenetico
from Datos import Datos
from EstrategiaParticionado import ValidacionSimple, ValidacionCruzada

def main():
    dataset = Datos("tic-tac-toe.data")
    clf = ClasificadorAlgoritmoGenetico(200, 200)

    vs = ValidacionSimple(0.7)
    vs.creaParticiones(dataset)


    clf.calculo_intervalos(dataset)
    clf.transforma_dataset(dataset)

    champion = clf.entrenamiento(dataset, vs.particiones[0].indicesTrain)
    error = clf.clasifica(vs.particiones[0].indicesTest,champion)
    print(error)
    clf.graficas_fitness()


if __name__ == "__main__":
    main()