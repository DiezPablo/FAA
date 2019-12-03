from Clasificador import Clasificador
import random
import numpy as np
import collections
import operator

class ClasificadorAlgoritmoGenetico(Clasificador):

    def __init__(self, numGeneraciones, numIndividuos, numReglas = 6, probabilidadMutacion = 0.1, elitismo = 0.05, probabilidadCruce = 0.85):

        self.numGeneraciones = numGeneraciones
        self.numIndividuos = numIndividuos
        self.numReglas = numReglas
        self.probabilidadMutacion = probabilidadMutacion
        self.elitismo = elitismo
        self.probabilidadCruce = probabilidadCruce
        super().__init__()

    def generar_poblacion(self, dataset):

        # Lista de diccionarios que va a almacenar los individuos
        self.poblacion = np.array(self.numIndividuos)

        # Calculamos la longitud de la regla que se va a generar y los intervalos dentro la regla que hacen referencia a cada atributo.
        self.listaDictsIntervalos = np.array([])

        # Hacemos un random del numero de reglas, pero todos los individuos tendran el mismo
        longitud_regla = 0
        for i in range(len(dataset.listaDicts)):
            dict ={}
            dict['inicio'] = longitud_regla
            dict['final'] = longitud_regla + len(dataset.listaDicts[i]) -1
            self.listaDictsIntervalos = np.append(self.listaDictsIntervalos,dict)

            longitud_regla += len(dataset.listaDicts[i])

        # Generamos los individuos que formaran la poblacion inicial
        for num_generacion in range(self.numIndividuos):

            # Diccionario que forma el individuo, con su num_reglas, la lista de reglas que lo componen y el fitness
            individuo = {}
            individuo['fitness'] = - 1
            individuo['num_reglas'] = self.num_reglas
            individuo['reglas'] = []
            for regla in range(self.num_reglas):
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

    def operador_cruce(self):
        """ Funcion que genera el cruce de dos individuos en caso deque supere la probabilidad definida."""
        # Seleccionamos los progenitores
        progenitores = self.seleccion_progenitores()

        # Creamos la poblacion nueva
        poblacion_nueva = []

        # Individuos que se generan del cruce
        individuo_1 = {}
        individuo_2 = {}


        for i in range(0, len(progenitores), 2):

            # Inicializamos los individuos nuevos que vamos a crear
            individuo_1 = {}
            individuo_2 = {}
            individuo_1['fitness'] = - 1
            individuo_1['num_reglas'] = self.num_reglas
            individuo_2['fitness'] = - 1
            individuo_2['num_reglas'] = self.num_reglas

            # En caso de que sea menor se produce el cruce
            if np.random.uniform(0, 1) < self.probabilidadCruce:

                # Calculamos un punto aleatorio entre las reglas del primer y el segundo progenitor
                punto_cruce = np.random.randint(0, self.numReglas)
                individuo_1['reglas'] = progenitores[i]['reglas'][:punto_cruce]
                individuo_1['reglas'] = individuo_1['reglas'] + progenitores[i+1]['reglas'][punto_cruce:]
                individuo_2['reglas'] = progenitores[i+1]['reglas'][:punto_cruce]
                individuo_2['reglas'] = individuo_2['reglas'] + progenitores[i]['reglas'][punto_cruce:]

            # En caso contrario los padres son los nuevos individuos
            else:
                individuo_1 = progenitores[i]
                individuo_2 = progenitores[i+1]

            poblacion_nueva.append(individuo_1)
            poblacion_nueva.append(individuo_2)


        return poblacion_nueva

    def seleccion_elitismo(self, poblacion_nueva):
        """Se selecciona el porcentaje marcada entre los mejores fitness de todos los individuos que formaran
        parte de la siguiente generacion de forma directa."""

        self.poblacion.sort(key=operator.itemgetter('fitness'), reverse = True)
        num_elites = round((self.elitismo * self.numIndividuos))

        # Los seleccionamos de la poblacion actual ordenada
        individuos_elitistas = self.poblacion[:num_elites]

        # Eliminamos de la poblacion_nueva el numero de individuos que son elitistas para hacer hueco a los nuevos
        poblacion_nueva = poblacion_nueva[:-individuos_elitistas]
        poblacion_nueva.append(individuos_elitistas)

        return poblacion_nueva

    def seleccion_progenitores(self):
        """ Esta funcion genera una lista con los progenitores que se van a utilizar para el cruce."""

        # Lista de progenitores
        progenitores = []

        # Creamos un array con las probabilidades de cada individuo.
        lista_fitness_ponderados = []

        # Media del fitness de la poblacion
        for individuo in range(self.poblacion):
            suma_fitness = self.poblacion[individuo]['fitness']

        # Probabilidad de ser elegido de cada individuo
        for individuo in range(self.poblacion):
            fitness_ponderado = self.poblacion[individuo]['fitness']/suma_fitness
            self.poblacion[individuo]['probabilidad_seleccion'] = fitness_ponderado
            lista_fitness_ponderados.append(fitness_ponderado)

        # Generamos la lista de progenitores con la funcion de numpy random_choice
        indices_progenitores = np.random.choice(len(self.poblacion),len(self.poblacion), lista_fitness_ponderados)

        # Generamos un array con los diccionarios que representan cada individuo
        for i in range(indices_progenitores):
            progenitores.append(self.poblacion[i])

        return progenitores

    def evaluar_regla(self):
        return




























