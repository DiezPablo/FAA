from Clasificador import Clasificador
import random

class ClasificadorAlgoritmoGenetico(Clasificador):

  def __init__(self, numGeneraciones, numIndividuos, maxReglas = 6):

    self.numGeneraciones = numGeneraciones
    self.numIndividuos = numIndividuos
    self.maxReglas = maxReglas
    super().__init__()

  def generar_poblacion(self, dataset):

    # Diccionario que va a almacenar todos los individuos que van a componer la poblacion
    self.individuos = {}

    # Calculamos la longitud de la regla que se va a generar.
    longitud_regla = 0
    for dict in dataset.listaDicts:
      longitud_regla += len(dict)



    # Creacion de reglas aleatorias para cada individuo, van a estar inicializados con un max de 6 y un minimo de 2
    for individuo in range(self.numIndividuos):
      num_reglas = random.randint(2, self.maxReglas)

      #for regla in range(num_reglas):

  def generar_regla(self, longitud_regla):
    return


