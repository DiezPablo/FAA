from Clasificador import Clasificador
import numpy as np
from matplotlib import pyplot as plt
import random

class ClasificadorAlgoritmoGenetico(Clasificador):

    def __init__(self, numGeneraciones, numIndividuos, numReglas = 8, probabilidadMutacion = 0.1, elitismo = 0.05, probabilidadCruce = 0.85, numAtributosCompare = 1):

        self.numGeneraciones = numGeneraciones
        self.numIndividuos = numIndividuos
        self.numReglas = numReglas
        self.probabilidadMutacion = probabilidadMutacion
        self.elitismo = elitismo
        self.probabilidadCruce = probabilidadCruce
        self.listaFitnessMedios = []
        self.listaFitnessChampion = []
        self.numAtributosCompare = numAtributosCompare

        super().__init__()


    def entrenamiento(self, dataset, datosTrain):

        """Algoritmo de entrenamiento del Algoritmo genetico. Recibe por parametro los datosTrain y el dataset sobre el que se ejecuta."""
        # Guardamos el numero de atributos del dato
        self.numAtributos = len(dataset.listaDicts) - 1

        # Generamos la poblacion inicial
        self.generar_poblacion(dataset)

        for numGen in range(self.numGeneraciones):

            # Inicializamos todos los fitness a 0.
            for individuo in self.poblacion:
                individuo['fitness'] = 0
            
            # Calculo del fitness de la poblacion
            self.fitness(datosTrain)

            # Guardamos los fitness medios de cada poblacion
            suma_fitness = 0
            for individuo in self.poblacion:
                suma_fitness += individuo['fitness']

            fitness_medio_generacion = suma_fitness/len(self.poblacion)
            self.listaFitnessMedios.append(fitness_medio_generacion)

            # Guardamos el fitness del mejor individuo de cada poblacion
            self.listaFitnessChampion.append(self.champion()['fitness'])

            # Elites que pasan directamente a a la siguiente poblacion
            elites, n_elites = self.seleccion_elitismo()

            # Operador cruce
            poblacion_cruzada = self.operador_cruce()

            #  Operador mutacion sobre la nueva poblacion
            individuos_mutados = self.operador_mutacion()     
                
            self.poblacion = []
            for i in range(len(poblacion_cruzada)):
                self.poblacion.append(poblacion_cruzada[i])
            
            for i in range(len(individuos_mutados)):
                self.poblacion.append(individuos_mutados[i])

            for i in range(len(elites)):
                self.poblacion.append(elites[i])

        #Calculamos el mejor individuo final
        self.fitness(datosTrain)
        champion = self.champion()
        self.listaFitnessChampion.append(champion['fitness'])

        suma_fitness = 0
        for individuo in self.poblacion:
            suma_fitness += individuo['fitness']

        fitness_medio_generacion = suma_fitness / len(self.poblacion)
        self.listaFitnessMedios.append(fitness_medio_generacion)

        print("Mejor individuo final: ", champion)


        return champion

    def clasifica(self, datosTest, champion):
        """Utilizando el mejor individuo tras terminar el numero de generaciones del algoritmo, clasifica los datos Test."""
        
        datTest = self.datos_transformados[datosTest]
        aciertos = 0

        # Recorremos los datos de test
        for dato in datTest:
            # Array que guardara las clases que se predicen para cada dato para posteriormente votar
            clases_predichas = []

            # Recorremos todas las reglas del mejor individuo
            for regla in champion['reglas']:
                pred = -1
        
                # Vemos si coinciden los atributos
                res = np.bitwise_and(dato.astype(int), regla.astype(int))
                num_unos = (res[:-1] == 1).sum()
                
                # En caso de que todos los atributos coincidan, guardamos la clase que predice esa regla.
                if num_unos >= self.numAtributosCompare:
                    clases_predichas.append(regla[-1])

            # En el caso en el que se haya predicho algo, vemos cual es la clase mayoritaria y la devolvemos
            if len(clases_predichas) != 0:
                if clases_predichas.count(1) > clases_predichas.count(0):
                    pred = 1
                elif clases_predichas.count(1) < clases_predichas.count(0):
                    pred = 0
                else:
                    pred = np.random.randint(0,2)

            # Si la clase mayoritaria acierta, se suma uno
            if pred == dato[-1]:
                aciertos += 1

        # Calculamos el error y lo devolvemos
        error = (len(datTest) - aciertos) / len(datosTest)

        return error, 1 - error


    def transforma_dataset(self, dataset):
        """ Transforma el dataset a la misma notacion que van a utilizar las reglas del algoritmo genético"""

        # Creamos un array donde van a insertarse los datos transformados
        self.datos_transformados = np.array([])

        # Convertimos los elementos al mismo tipo que las reglas
        for dato in dataset.datos:
            array_convertido = np.zeros(self.longitud_regla - 1)
            for i in range(len(dato)-1):
                posicion_bit_uno = self.listaDictsIntervalos[i]['final'] - int(dato[i])
                array_convertido[posicion_bit_uno] = 1

            array_convertido = np.append(array_convertido, dato[i+1])

            self.datos_transformados = np.append(self.datos_transformados, array_convertido)

        self.datos_transformados = self.datos_transformados.reshape(dataset.numDatos, self.longitud_regla)

    def calculo_intervalos(self, dataset):

        # Calculamos la longitud de la regla que se va a generar y los intervalos dentro la regla que hacen referencia a cada atributo.
        self.listaDictsIntervalos = np.array([])

        # Hacemos un random del numero de reglas, pero todos los individuos tendran el mismo
        self.longitud_regla = 0
        for i in range(len(dataset.listaDicts) - 1):
            dict ={}
            dict['inicio'] = self.longitud_regla
            dict['final'] = self.longitud_regla + len(dataset.listaDicts[i]) -1
            self.listaDictsIntervalos = np.append(self.listaDictsIntervalos,dict)

            self.longitud_regla += len(dataset.listaDicts[i])

        self.longitud_regla += 1

        return self.longitud_regla

    def generar_poblacion(self, dataset):

        # Lista de diccionarios que va a almacenar los individuos
        self.poblacion = np.array([])

        self.calculo_intervalos(dataset)

        # Generamos los individuos que formaran la poblacion inicial
        for num_generacion in range(self.numIndividuos):

            # Diccionario que forma el individuo, con su num_reglas, la lista de reglas que lo componen y el fitness
            individuo = {}
            individuo['fitness'] = 0
            individuo['num_reglas'] = self.numReglas
            individuo['reglas'] = []
            for regla in range(self.numReglas):
                individuo['reglas'].append(self.generar_regla())

            self.poblacion = np.append(self.poblacion, individuo)

    def generar_regla(self):

        # Generamos una regla de longitud calculada anteriormente
        regla = np.zeros(self.longitud_regla -1)

        # Caso atributos(n bits)
        for i in range(len(self.listaDictsIntervalos)):
            aleat = np.random.randint(self.listaDictsIntervalos[i]['inicio'], self.listaDictsIntervalos[i]['final']+1)
            regla[aleat] = 1

            # Caso clase(1 bit)
        aleat = np.random.randint(0, 2)
        regla = np.append(regla, aleat)

        return regla

    def operador_mutacion(self):
        """ Solo se mutara una regla, de manera aleatoria, en caso de que la probabilidad que obtenemos sea menor del umbral."""

        n_mutaciones = round((self.probabilidadMutacion * self.numIndividuos))

        individuos_mutacion = random.sample(list(self.poblacion), n_mutaciones)
        
        for individuo in individuos_mutacion:
            # Si hay que mutar, generamos un numero aleat. para ver que regla mutamos.
            regla_mutacion = np.random.randint(0,individuo['num_reglas'])
            
            # Generamos una regla aleatoria nueva y la cambiamos por la anterior
            individuo['reglas'][regla_mutacion] = self.generar_regla()

        return individuos_mutacion

    def operador_cruce(self):
        """ Funcion que genera el cruce de dos individuos en caso deque supere la probabilidad definida."""

        # Seleccionamos los progenitores
        progenitores = self.seleccion_progenitores()

        n_cruces = round((self.probabilidadCruce * self.numIndividuos))
        
        # Creamos la poblacion nueva
        poblacion_nueva = []
        
        for i in range(0, len(progenitores), 2):

            # Inicializamos los individuos nuevos que vamos a crear
            individuo_1 = {}
            individuo_2 = {}
            individuo_1['fitness'] = 0
            individuo_1['num_reglas'] = self.numReglas
            individuo_2['fitness'] = 0
            individuo_2['num_reglas'] = self.numReglas            
            
            # Calculamos un punto aleatorio entre las reglas del primer y el segundo progenitor
            punto_cruce = np.random.randint(0, self.numReglas)
            
            individuo_1['reglas'] = progenitores[i]['reglas'][:punto_cruce]
            individuo_1['reglas'] = individuo_1['reglas'] + progenitores[i+1]['reglas'][punto_cruce:]
            individuo_2['reglas'] = progenitores[i+1]['reglas'][:punto_cruce]
            individuo_2['reglas'] = individuo_2['reglas'] + progenitores[i]['reglas'][punto_cruce:]
            
        # En caso contrario los padres son los nuevos individuos
            
            poblacion_nueva.append(individuo_1)
            poblacion_nueva.append(individuo_2)
            
        return poblacion_nueva[:n_cruces]

    def seleccion_elitismo(self):
        """Se selecciona el porcentaje marcada entre los mejores fitness de todos los individuos que formaran
        parte de la siguiente generacion de forma directa."""

        # Ordenamos la poblacion y calculamos el numero de elites en funcion de la probabilidad de elitismo.
        self.poblacion = sorted(self.poblacion, key=lambda k: k['fitness'], reverse=True)
        num_elites = round((self.elitismo * self.numIndividuos))

        # Nos guardamos los 5 mejores de la poblacion y los añadimos a la poblacion nueva
        individuos = self.poblacion[:num_elites]

        # Guardamos en una nueva lista que devolvemos los mejores
        elites = []
        for i in range(num_elites):
            elites.append(individuos[i])

        return elites, num_elites

    def champion(self):
        """ Devuelve el mejor individiuo de la poblacion"""

        # Ordenamos la poblacion en funcion del fitness
        self.poblacion = sorted(self.poblacion, key=lambda k: k['fitness'], reverse=True)

        champion = self.poblacion[0]
        return champion

    def seleccion_progenitores(self):
        """ Esta funcion genera una lista con los progenitores que se van a utilizar para el cruce."""

        # Lista de progenitores
        progenitores = []

        # Creamos un array con las probabilidades de cada individuo.
        lista_fitness_ponderados = []

        suma_fitness = 0
        # Media del fitness de la poblacion
        for individuo in range(len(self.poblacion)):
            suma_fitness += self.poblacion[individuo]['fitness']

        # Probabilidad de ser elegido de cada individuo
        for individuo in range(len(self.poblacion)):
            if suma_fitness == 0:
                lista_fitness_ponderados.append(0)
            else:
                fitness_ponderado = self.poblacion[individuo]['fitness']/suma_fitness
                lista_fitness_ponderados.append(fitness_ponderado)

        # Generamos la lista de progenitores con la funcion de numpy random_choice
        indices_progenitores = np.random.choice(len(self.poblacion),len(self.poblacion), lista_fitness_ponderados)

        # Generamos un array con los diccionarios que representan cada individuo
        for i in indices_progenitores:
            progenitores.append(self.poblacion[i])

        return progenitores


    def fitness(self, datosTrain):
        """ Funcion que calcula el fitness de un individuo de la poblacion"""

        datTrain = self.datos_transformados[datosTrain]
    
        # Para cada individuo recorremos todos los datos
        for individuo in self.poblacion:
            
            # Contador que cuenta el numero de aciertos del individuo respecto a todos los datos, que es el fitness
            aciertos = 0
            for dato in datTrain:
                clases_predichas = []
                pred = -1

                for regla in individuo['reglas']:
                    # And logico de los atributos
                    res = np.bitwise_and(dato.astype(int), regla.astype(int))
                    num_unos = (res[:-1] == 1).sum()

                    # Si coinciden todos guardamos la clase de las reglas que se activan
                    if num_unos >= self.numAtributosCompare:
                        clases_predichas.append(regla[-1])

                # Predecimos la clase mayoritaria
                if len(clases_predichas) != 0:
                    if clases_predichas.count(1) > clases_predichas.count(0):
                        pred = 1
                    elif clases_predichas.count(1) < clases_predichas.count(0):
                        pred = 0
                    else:

                        # Este caso se desestima, por incongruencias de las reglas
                        pred = -1

                    # Si la prediccion coincide con la clase del dato, acertamos
                if pred == dato [-1]:
                    aciertos += 1

            # Calculo del fitness para cada individuo.
            individuo['fitness'] = aciertos / len(datTrain)

    def graficas_fitness(self):
        """ Funcion que genera las graficas del fitness medio de la poblacion y la evolucion del fitness del mejor individuo."""

        plt.plot(self.listaFitnessChampion, c='red', label = 'fitness champion')
        plt.plot(self.listaFitnessMedios, c='blue', label = 'fitness medio poblacion')
        plt.xlabel("Num. generaciones")
        plt.ylabel("Fitness")
        plt.legend(loc='best')
        plt.show()
