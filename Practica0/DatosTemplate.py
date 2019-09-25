import numpy as np

class Datos:

  TiposDeAtributos=('Continuo','Nominal')

  # TODO: procesar el fichero para asignar correctamente las variables tipoAtributos, nombreAtributos, nominalAtributos, datos y diccionarios
  # NOTA: No confundir TiposDeAtributos con tipoAtributos
  def __init__(self, nombreFichero):

      with open(nombreFichero, "r") as f:
        # Guardamos el numero de datos que contiene el DataSet y esta en la primera linea
        self.numDatos = f.readline()

        # Guardamos el nombre de los atributos
        self.nombreAtributos = f.readline().strip('\n').split(',')
        print(self.nombreAtributos)

        # Leemos el tipo de los atributos de las variables y eliminamos el ultimo que es un salto de linea
        self.tipoAtributos = f.readline().strip('\n').split(',')
        print(self.tipoAtributos)

        # Comprobamos que todos los atributos sean Continuos o Nominales
        if any(atr not in Datos.TiposDeAtributos for atr in self.tipoAtributos):
            raise ValueError("Tipo de atributo erroneo")

        # Segun el atributo, asignamos True o False.
        self.nominalAtributos = []

        for tipo in self.tipoAtributos:
            if tipo == self.TiposDeAtributos[0]:
                self.nominalAtributos.append(False)
            else:
                self.nominalAtributos.append(True)
        print(self.nominalAtributos)


        # Creacion de lista diccionarios, en caso de que el atributo sea Continuo, el diccionario estará vacio
        self.listaDicts = []
        for i in range(len(self.tipoAtributos)):
            self.listaDicts.append({})
        print(self.listaDicts)

        datos = f.readlines()
        datosFormat = []
        for lista in datos:
            datosFormat.append(lista.strip('\n').split(','))

        # print(set(sorted(datosFormat[0])))
        atributo = []
        for i in range(len(self.tipoAtributos)):
            atributo.append([])

        for lista in datosFormat:
            for lista



        print(self.listaDicts)





  # TODO: implementar en la practica 1
  def extraeDatos(self, idx):
    pass
