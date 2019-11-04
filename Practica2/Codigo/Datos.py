import numpy as np

class Datos:
    TiposDeAtributos = ('Continuo', 'Nominal')

    # TODO: procesar el fichero para asignar correctamente las variables tipoAtributos, nombreAtributos, nominalAtributos, datos y diccionarios
    # NOTA: No confundir TiposDeAtributos con tipoAtributos
    def __init__(self, nombreFichero):

        with open(nombreFichero, "r") as f:
            # Guardamos el numero de datos que contiene el DataSet y esta en la primera linea
            self.numDatos = int(f.readline())

            # Guardamos el nombre de los atributos
            self.nombreAtributos = f.readline().strip('\n').split(',')
            # print(self.nombreAtributos)

            # Leemos el tipo de los atributos de las variables y eliminamos el ultimo que es un salto de linea
            self.tipoAtributos = f.readline().strip('\n').split(',')
            # print(self.tipoAtributos)

            # Comprobamos que todos los atributos sean Continuos o Nominales
            if any(atr not in Datos.TiposDeAtributos for atr in self.tipoAtributos):
                raise ValueError("Tipo de atributo erroneo")

            # Segun el atributo, asignamos True o False.
            self.nominalAtributos = []

            # Guardamos en la lista nominalAtributos en la posicion de cada uno si es o no Nominal
            for tipo in self.tipoAtributos:
                if tipo == self.TiposDeAtributos[0]:
                    self.nominalAtributos.append(False)
                else:
                    self.nominalAtributos.append(True)


            # Guardamos los datos del fichero y los formateamos, de tal forma que cada linea es una lista
            datos = f.readlines()
            datosFormat = []
            for lista in datos:
                datosFormat.append(lista.strip('\n').split(','))

            listaDatosAtributos = []
            for i in range(len(self.tipoAtributos)):
                listaDatosAtributos.append([])

            # Hacemos la traspuesta de los datos que guardamos para que cada lista de atributo guarde todos los datos
            # de cada atributo.
            for lista in datosFormat:
                i = 0
                for item in lista:
                    listaDatosAtributos[i].append(item)
                    i += 1

            # Ordenamos y hacemos un set para eliminar repetidos.
            i = 0
            for item in listaDatosAtributos:
                listaDatosAtributos[i] = sorted(set(item))
                i += 1

            # Creacion de lista diccionarios, en caso de que el atributo sea Continuo, el diccionario estara vacio
            self.listaDicts = []
            for i in range(len(self.tipoAtributos)):
                self.listaDicts.append({})

            # Creamos el diccionario tal y como se describe en las diapositivas, por orden y asignando valores numericos crecientes
            i = 0
            for atributo in listaDatosAtributos:
                k = 0
                if self.tipoAtributos[i] == "Nominal":
                    for dato in atributo:
                        self.listaDicts[i][dato] = k
                        k += 1
                i += 1

            # Creacion de la matriz de datos utilizando el diccionario para mapear los valores
            # En primer lugar, creamos una matriz vacia de tamaña numero de atributos.
            self.datos = np.empty((int(self.numDatos), int(len(self.tipoAtributos))))
            i = 0
            j = 0

            # Metemos los datos en la matriz, mapeando con los diccionarios en el caso de que sean Nominales, y si son continuos normal.
            for i in range(int(self.numDatos)):
                for j in range(len(self.tipoAtributos)):
                    if self.tipoAtributos[j] == 'Nominal':
                        self.datos[i][j] = self.listaDicts[j].get(str(datosFormat[i][j]))
                    else:
                        self.datos[i][j] = datosFormat[i][j]

            f.close()

    # TODO: implementar en la practica 1
    def extraeDatos(self, idx):
        return self.datos[idx]

    def calcularMediasDesv(self,datos):

        # datosTrain es la matriz directamente, no hay que extraer nada
        # Se calcula la desv. tipica y la media para los atributos continuos

        # Creamos una lista con los indices que son continuos para calcular la media y desv tipica sobre ellos.
        self.indicesContinuos = []
        for i in range(len(self.nominalAtributos)):
            if self.nominalAtributos[i] == False:
                self.indicesContinuos.append(i)

        print(len(self.nominalAtributos))
        # Matriz que guarda el valor por atributo de la desv. tipica y la media
        estadisticas = np.zeros((2,len(self.nominalAtributos)))

        # Calculamos la desv tipica y media de los indices continuos sobre todos los datos que recibimos por param.
        for i in self.indicesContinuos:
            estadisticas[0,i] = np.mean(datos[:,i])
            estadisticas[1,i] = np.std(datos[:,i])

        return estadisticas


    def normalizarDatos(self, datos):

        estadisticas = self.calcularMediasDesv(datos)

        # Normalizamos los datos
        for i in self.indicesContinuos:
            datos[:,i] -= estadisticas[0,i]
            datos[:,i] /= estadisticas[1,i]

        return datos, estadisticas




