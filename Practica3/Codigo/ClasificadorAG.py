from Clasificador import Clasificador
import random
import numpy as np

class ClasificadorAlgoritmoGenetico(Clasificador):

  def __init__(self, numGeneraciones, numIndividuos, maxReglas = 6):

    self.numGeneraciones = numGeneraciones
    self.numIndividuos = numIndividuos
    self.maxReglas = maxReglas
    super().__init__()

  def generar_poblacion(self, dataset):

    # Diccionario que va a almacenar todos los individuos que van a componer la poblacion
    self.individuos = {}

    # Calculamos la longitud de la regla que se va a generar y los intervalos dentro la regla que hacen referencia a cada atributo.
    self.listaDictsIntervalos = np.array([])

    longitud_regla = 0
    for i in range(len(dataset.listaDicts)):
      dict ={}
      dict['inicio'] = longitud_regla
      dict['final'] = longitud_regla + len(dataset.listaDicts[i]) -1
      self.listaDictsIntervalos = np.append(self.listaDictsIntervalos,dict)

      longitud_regla += len(dataset.listaDicts[i])

    self.generar_regla(longitud_regla)

    # Falta generar las reglas!!!

  def generar_regla(self, longitud_regla):

    # Generamos una regla de longitud calculada anteriormente
    regla = np.zeros(longitud_regla)

    for i in range(len(self.listaDictsIntervalos)):
      aleat = np.random.randint(low = self.listaDictsIntervalos[i]['inicio'], high = self.listaDictsIntervalos[i]['final'] + 1)
      regla[aleat] = 1

    return regla




























