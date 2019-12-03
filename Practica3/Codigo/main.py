from ClasificadorAG import ClasificadorAlgoritmoGenetico
from Datos import Datos
from EstrategiaParticionado import ValidacionSimple, ValidacionCruzada
import random
import numpy as np
def main():
    #dataset = Datos("ejemplo1.data")
    #clf = ClasificadorAlgoritmoGenetico(10, 100)

    #clf.generar_poblacion(dataset)
    individuo1 = {}
    individuo2 = {}

    prueba1 = {}
    prueba1['reglas'] = [[1],[2],[3],[4]]
    prueba2 = {}
    prueba2['reglas'] = [[5],[6],[7],[8]]

    aleat = np.random.randint(0, len(prueba1['reglas']))
    print(aleat)

    individuo1['reglas'] = prueba1['reglas'][:aleat]
    individuo1['reglas']= individuo1['reglas'] + prueba2['reglas'][aleat:]
    individuo2['reglas'] = prueba2['reglas'][:aleat]
    individuo2['reglas'] = individuo2['reglas'] + prueba1['reglas'][aleat:]

    print(individuo1)
    print(individuo2)

if __name__ == "__main__":
    main()