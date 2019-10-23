
from Datos import Datos
from EstrategiaParticionado import EstrategiaParticionado, ValidacionSimple, ValidacionCruzada
from Clasificador import Clasificador, ClasificadorNaiveBayes

def main():

    dataset = Datos('german.data')
    #estrategia = ValidacionSimple(0.7)
    estrategia = ValidacionCruzada(4)
    nb = ClasificadorNaiveBayes(True)

    errores = nb.validacion(estrategia,dataset,nb)
    print(errores)

if __name__ == "__main__":
    main()