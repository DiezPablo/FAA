from Clasificador import Clasificador
import random
import numpy as np
import collections
import operator

class ClasificadorAlgoritmoGenetico(Clasificador):

    def __init__(self, numGeneraciones, numIndividuos, maxReglas = 6, probabilidadMutacion = 0.1, elitismo = 0.05, probabilidadCruce = 0.85):

        self.numGeneraciones = numGeneraciones
        self.numIndividuos = numIndividuos
        self.maxReglas = maxReglas
        self.probabilidadMutacion = probabilidadMutacion
        self.elitismo = elitismo
        self.probabilidadCruce = probabilidadCruce
        super().__init__()

    def generar_poblacion(self, dataset):

        # Lista de diccionarios que va a almacenar los individuos
        self.poblacion = np.array(self.numIndividuos)

        # Calculamos la longitud de la regla que se va a generar y los intervalos dentro la regla que hacen referencia a cada atributo.
        self.listaDictsIntervalos = np.array([])

        longitud_regla = 0
        for i in range(len(dataset.listaDicts) - 1):
            dict ={}
            dict['inicio'] = longitud_regla
            dict['final'] = longitud_regla + len(dataset.listaDicts[i]) -1
            self.listaDictsIntervalos = np.append(self.listaDictsIntervalos,dict)

            longitud_regla += len(dataset.listaDicts[i])

        # Generamos los individuos que formaran la poblacion inicial
        for num_generacion in range(self.numIndividuos):

            # Diccionario que forma el individuo, con su num_reglas, la lista de reglas que lo componen y el fitness
            individuo = {}
            num_reglas = np.random.randint(2, self.maxReglas)
            individuo['fitness'] = - 1
            individuo['num_reglas'] = num_reglas
            individuo['reglas'] = []
            for regla in range(num_reglas):
                individuo['reglas'].append(self.generar_regla(longitud_regla))

            self.poblacion = np.append(self.poblacion, individuo)

    def generar_regla(self, longitud_regla):

        # Generamos una regla de longitud calculada anteriormente
        regla = np.zeros(longitud_regla)

        for i in range(len(self.listaDictsIntervalos)):
            aleat = np.random.randint(self.listaDictsIntervalos[i]['inicio'], self.listaDictsIntervalos[i]['final'])
            regla[aleat] = 1

        return regla


    def operador_mutacion(self):
        """ Solo se mutara una regla, de manera aleatoria, en caso de que la probabilidad que obtenemos sea menor del umbral."""

        for individuo in self.poblacion:

            # Calculamos la probabilidad de mutar en base al umbral.
            if np.random.uniform(0, 1) < self.probabilidadMutacion:

                # Si hay que mutar, generamos un numero aleat. para ver que regla mutamos.
                regla_mutacion = np.random.randint(0,individuo['num_reglas'])

                random_atributo = np.random.randint(0,len(self.listaDictsIntervalos))
                atributo_mutacion = self.listaDictsIntervalos[random_atributo]

                bit_flip = np.random.randint(low = atributo_mutacion['inicio'], high = atributo_mutacion['final'])

                # Ponemos a 0 todos los bits del atributo que se va a mutar
                for i in range(atributo_mutacion['inicio'], atributo_mutacion['final']):
                    individuo['reglas'][regla_mutacion][i] = 0

                individuo['reglas'][regla_mutacion][bit_flip] = 1

        return self.poblacion

    def operador_cruce(self, progenitores):
        individuo1 = {}
        individuo2 = {}



    def seleccion_elitismo(self):
        """Se selecciona el porcentaje marcada entre los mejores fitness de todos los individuos que formaran
        parte de la siguiente generacion de forma directa."""
        self.poblacion.sort(key=operator.itemgetter('fitness'))

        return self.poblacion[:(self.elitismo * self.numIndividuos)]

    def seleccion_progenitores(self):





























