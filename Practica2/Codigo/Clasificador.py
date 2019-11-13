from abc import ABCMeta,abstractmethod
import numpy as np
import math
from collections import Counter
from sortedcontainers import SortedDict
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
from numpy import linalg as LA
from statistics import mode

class Clasificador:
  # Clase abstracta
  __metaclass__ = ABCMeta

  # Metodos abstractos que se implementan en casa clasificador concreto
  @abstractmethod
  # TODO: esta funcion debe ser implementada en cada clasificador concreto
  # datosTrain: matriz numpy con los datos de entrenamiento
  # atributosDiscretos: array bool con la indicatriz de los atributos nominales
  # diccionario: array de diccionarios de la estructura Datos utilizados para la codificacion de variables discretas
  def entrenamiento(self, datos, datosTrain, atributosDiscretos, diccionario):
    pass

  @abstractmethod
  # TODO: esta funcion debe ser implementada en cada clasificador concreto
  # devuelve un numpy array con las predicciones
  def clasifica(self, datosTest, atributosDiscretos, diccionario):
    pass

  # Obtiene el numero de aciertos y errores para calcular la tasa de fallo
  # TODO: implementar
  def error(self, datos, pred):
    # Aqui se compara la prediccion (pred) con las clases reales y se calcula el error
    i = 0
    real = datos[:, -1]
    error = 0
    for i in range(len(real)):
      if real[i] != pred[i]:
        error += 1
    err = (error) / (len(real) + 0.0)
    return err

  # Realiza una clasificacion utilizando una estrategia de particionado determinada
  # particionado : estrategia de validacion que queremos utilizar
  # dataset : clase de tipo Datos que utilizamos para entrenar y clasificar el modelo
  # clasificador: instancia del clasificador que se va a usar
  # TODO: implementar esta funcion
  def validacion(self, particionado, dataset, clasificador, seed: object = None):

    # Creamos las particiones siguiendo la estrategia llamando a particionado.creaParticiones
    # - Para validacion cruzada: en el bucle hasta nv entrenamos el clasificador con la particion de train i
    # y obtenemos el error en la particion de test i
    # - Para validacion simple (hold-out): entrenamos el clasificador con la particion de train
    # y obtenemos el error en la particion test. Otra opci�n es repetir la validaci�n simple un n�mero especificado de veces, obteniendo en cada una un error. Finalmente se calcular�a la media.
    errores = 0
    # particionado.creaParticiones(dataset, seed)
    # Comprobamos si es por validación cruzada o simple, por la longitud de la lista de particiones
    particionado.particiones = []
    particionado.creaParticiones(dataset)

    # Validación Simple
    if len(particionado.particiones) == 1:
      clasificador.entrenamiento(dataset, particionado.particiones[0].indicesTrain)
      pred = clasificador.clasifica(dataset, particionado.particiones[0].indicesTest)
      ret = self.error(dataset.extraeDatos(particionado.particiones[0].indicesTest), pred)
      if ret > 0:
        return ret
      else:
        return 0

    # Validación Cruzada
    else:
      lista_error = []
      for particion in particionado.particiones:
        clasificador.entrenamiento(dataset, particion.indicesTrain)
        pred = clasificador.clasifica(dataset, particion.indicesTest)
        ret = self.error(dataset.extraeDatos(particion.indicesTest), pred)
        lista_error.append(ret)
      return np.mean(lista_error), np.std(lista_error)

  def matrizConfusion(self, dataset, datosTest, prediccion):

    # Calculamos la matriz de confusion utlizando sk-learn. Solo se calcula en el caso de que la clasificacion sea binaria.
    testData = dataset.extraeDatos(datosTest)
    clase_real = testData[:, -1]

    matriz = confusion_matrix(prediccion, clase_real)

    # La funcion ravel() devuelve todas las estadisticas relacionadas con la matriz de confusion
    tn, fp, fn, tp = matriz.ravel()

    # Calculamos las tasas extraídas de la matriz de confusión
    tpr = tp / (tp + fn)
    fpr = fp / (fp + fn)

    self.lista_tpr.append(tpr)
    self.lista_fpr.append(fpr)

    return matriz

  def curvaROC(self):

    x = np.linspace(0, 1, 100)
    plt.plot(x, x, c='blue')
    for i in range(len(self.lista_fpr)):
      plt.plot(self.lista_fpr[i], self.lista_tpr[i], 'ro')
    plt.show()

class ClasificadorNaiveBayes(Clasificador):

  def __init__(self, laplace):
    self.laplace = laplace
    self.lista_fpr = []
    self.lista_tpr = []

  def entrenamiento(self, dataset, datosTrain):

    # Cargamos todos los datos de la clase del dataset desde la matriz de datos
    clasesTrain = dataset.extraeDatos(datosTrain)
    self.numClases = clasesTrain[:, -1]

    # Contamos las apariciones de cada uno para luego calcular la probabilidad a priori de cada clase
    counter = Counter(self.numClases)

    # Calculamos la probabilidad de la clase y lo metemos en un diccionario ordenado segun el numero
    # correspondiente a cada clase asignado en el diccionario
    self.dictPrioris = {}
    for k in counter:
      k = int(k)
      counter[k] = counter[k] / len(self.numClases)
      self.dictPrioris[k] = counter[k]

    # Aqui ordenamos el diccionario para que esten en el mismo orden de como extraemos los datos del dataset
    self.dictPrioris = SortedDict(self.dictPrioris)

    # Calcular tablas de probabilidades del entrenamiento. Tenemos que calcular por cada atributo una cuenta
    # de las apariciones en cada clase
    # Creamos una lista de matrices, donde vamos almacenar todos los datos que hemos obtenido en los datos de Test
    self.posteriori = np.zeros(len(dataset.nombreAtributos) - 1, dtype=object)

    # Recorremos todos los datos de la matriz sin llegar a la clase
    for i in range(len(dataset.nombreAtributos) - 1):

      # Si el dato que obtenemos es Nominal haremos el recuento de todas las veces que sale la P(D|H)
      if dataset.nominalAtributos[i] == True:

        # Creamos una matriz de tamaño X: Número de Atributos menos la clase Y: Número de clases
        post = np.zeros((len(dataset.listaDicts[i]), len(dataset.listaDicts[-1])))

        # Aqui contamos todos las datos que queremos del datos Train para construir la matriz de entrenamiento
        for c in range(len(dataset.listaDicts[-1])):
          datosEnt = dataset.extraeDatos(datosTrain)
          dat = datosEnt[:, i]
          repes = Counter(dat[datosEnt[:, -1] == c])
          for r in repes:
            post[int(r), c] = repes[r]
          if self.laplace == True:
            self.posteriori[i] = post + 1
          else:
            self.posteriori[i] = post

      # Si el dato es Continuo obtendremos la media y la desviación tipica de la clase
      else:

        # Creamos una matriz de X: Los datos de Media y Desivación típica Y: Número de clases
        post = np.zeros((2, len(dataset.listaDicts[-1])))

        # Aqui obtenemos la media y desviación tipica de cada clase, despues de tener los datos de entrenamiento
        for c in range(len(dataset.listaDicts[-1])):
          datosEnt = dataset.extraeDatos(datosTrain)
          dat = datosEnt[:, i]
          datos = dat[datosEnt[:, -1] == c]
          post[0][c] = np.mean(datos)
          post[1][c] = np.std(datos)
        self.posteriori[i] = post


    # Calculamos los valores de los posteriori de todos las tablas anteriores
    for i in range(len(dataset.listaDicts) - 1):
      if dataset.nominalAtributos[i] == True:
        self.posteriori[i] /= sum(self.posteriori[i])

  def clasifica(self, dataset, datosTest):
    acum_probs = 1
    self.prediccion = []
    datTest = dataset.extraeDatos(datosTest)

    # Ahora vamos a estudiar la probabilidad de la clase con los datos obtenidos en el entrenamiento
    # Recorremos todos las datos de la matriz de los datos Test
    for dato in datTest:
      mapa = []
      # Aqui obtenemos los prioris de cada clase para poder obtener la probabilidad de cada una
      for clase in range(len(self.dictPrioris)):
        listaVerosimilitudes = []
        # Aqui obtenemos cada valor posteriori de nuestro entrenamiento de los datos, es decir, P(D|H)
        for atributo in range(len(self.posteriori)):
          if dataset.nominalAtributos[atributo] == True:
            prob = self.posteriori[atributo][int(dato[atributo])][clase]
            listaVerosimilitudes.append(prob)

          # Aqui obtenemos la probabilidad de los atibutos continuos
          else:
            # Hacemos la formula de la distribucion normal
            exp1 = 1 / (self.posteriori[atributo][1][clase] * math.sqrt(2 * math.pi))
            exp2 = np.power((dato[atributo] - self.posteriori[atributo][0][clase]), 2)
            exp3 = np.power(self.posteriori[atributo][1][clase], 2)
            exp4 = exp2 / exp3
            exp4 = math.exp((-1 / 2) * exp4)
            prob = exp1 * exp4
            listaVerosimilitudes.append(prob)

        for verosimilitud in listaVerosimilitudes:
          acum_probs *= verosimilitud
        acum_probs *= self.dictPrioris.get(clase)
        mapa.append(acum_probs)
        acum_probs = 1

      # Aqui obtenemos la predicción de mayor probabilidad y la guardamos en nuestra lista de predicciones
      self.prediccion.append(np.argmax(mapa))


    # Devolvemos la lista con la predicción de nuestro clasifica
    return self.prediccion

class ClasificadorVecinosProximos(Clasificador):

  def __init__(self, k, normaliza = True):

    # k define el numero de vecinos y normaliza si queremos normalizar los datos o no.
    self.k = k
    self.normaliza = normaliza

    super().__init__()

  def entrenamiento(self, dataset, datosTrain):

    # Normalizar los datos en caso de que la variable sea True
    if self.normaliza == True:
      self.datosClasifica, _ = dataset.normalizarDatos(dataset.datos)
    else:
      self.datosClasifica = dataset.datos

    # Datos de train
    self.datTrain = self.datosClasifica[datosTrain]

    return self.datTrain

  def clasifica(self, dataset, datosTest = None):

    if datosTest is None:
      datTest = dataset[range(len(dataset))]
    else:
      datTest = self.datosClasifica[datosTest]



    prediccion = []

    # Cogemos cada ejemplo en datosTest para calcular la distancia a cada uno de los ejemplos de Train
    for datoTest in datTest[:, :-1]:
      distancias = []
      for datoTrain in self.datTrain[:, :-1]:
        sumatorio_dist_euclideas = 0
        for i in range(len(datoTest)):
          sumatorio_dist_euclideas += LA.linalg.norm(datoTest[i] - datoTrain[i])
        distancias.append(sumatorio_dist_euclideas)

      k_datos = self.datTrain[np.argsort(distancias)[:self.k]]
      prediccion.append(mode(k_datos[:,-1]))

    return prediccion

# Clase que define un clasificador utilizando el metodo de Regresion Logistica
class ClasificadorRegresionLogistica(Clasificador):

  def __init__(self, constante_aprendizaje, epocas):
    # Se utiliza para inicializar la constante de aprendizaje y el numero de epocas necesarias para el train
    self.constante_aprendizaje = constante_aprendizaje
    self.epocas = epocas

    super().__init__()

  # Funcion que realiza el calculo de la sigmoidal de el numero que recibe por parámetro
  def sigmoidal(self, a):

    if a >= 100:
      return 1
    elif a < 100:
      return 0
    else:
      return 1.0 / (1.0 + math.exp(-a))

  def entrenamiento(self, dataset, datosTrain):

    # Datos de entrenamiento
    self.datTrain = dataset.extraeDatos(datosTrain)

    # Inicializamos el vector w
    self.vector_w = np.random.uniform(low=-0.5, high=0.5, size=len(dataset.tipoAtributos))

    i = 0

    # Algoritmo del entrenamiento de regresion lineal
    while i < self.epocas:
      for dato in self.datTrain:

        # Calculamos vector x
        x = np.append([1],dato[:-1])

        # Calculamos w.x
        wx = np.dot(self.vector_w,x)

        # Sigmoidal de w.x
        sigmoidal = self.sigmoidal(wx)

        # Actualizamos el vector w
        self.vector_w = self.vector_w - (np.dot(self.constante_aprendizaje * (sigmoidal - dato[-1]),x))

      i += 1

    return self.vector_w

  def clasifica(self, dataset, datosTest = None):

    if datosTest is None:
      datosTest = range(len(dataset))

    datTest = dataset[datosTest]
    prediccion = []

    for dato in datTest:

      # Vector x
      x = np.append([1], dato[:-1])

      # Calculo de la sigmoidal que nos da la probabilidad de que el dato sea de clase 1
      wx = np.dot(self.vector_w, x)
      sigmoidal = self.sigmoidal(wx)

      # Prediccion del clasificador
      if(sigmoidal >= 0.5):
        prediccion.append(1)
      else:
        prediccion.append(0)

    return prediccion




