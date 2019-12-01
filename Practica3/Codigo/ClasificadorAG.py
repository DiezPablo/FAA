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
    self.listaDictsIntervalos = {}

    for i in range(len(dataset.listaDicts)):




  def generar_regla(self, longitud_regla):

    i = 0
    print(i)
























