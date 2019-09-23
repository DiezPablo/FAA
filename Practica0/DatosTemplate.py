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
          self.nombreAtributos = f.readline().split(',')
          print(self.nombreAtributos)

          # Eliminamos el ultimo \n que hay en la linea
          #self.nombreAtributos.pop()

          # Leemos el tipo de los atributos de las variables y eliminamos el ultimo que es un salto de linea
          try:
              self.tipoAtributos = f.readline().split(',')
              #self.tipoAtributos.pop()
              self.nominalAtributos = []
              for tipo in self.tipoAtributos:
                  if tipo == self.TiposDeAtributos[0]:
                      self.nominalAtributos.append(False)
                  else:
                      self.nominalAtributos.append(True)
          except ValueError:
              print("Error")


          # Guardamos el numero de atributos
          self.numAtributos = len(self.nombreAtributos)

          datosAux = f.readlines()
          datosN = []
          for dat in datosAux:
              datosN.append(dat.split(','))

          #datos = f.readline().split(',')
          #print(datos)
          #j = 0
          #i = 0
          #k = 0
          #valores = []
          #dic = []
          #for j in range(self.numAtributos):
            #  for i in range(int(self.numDatos)):
            #      if datosN[i][j] not in valores:
            #          valores.append(datosN[i][j])
          #print(valores)
          self.diccionarios = []
          i = 0
          for i in range(self.numAtributos-1):
              print(self.nominalAtributos[i])
              if self.nominalAtributos[i] == True:
                  self.diccionarios.append({'x':0,'o':1,'b':2})
              else:
                  self.diccionarios.append({})
          self.diccionarios.append({'positive\r\n':1, 'negative\r\n':0})
          self.datos = np.empty((int(self.numDatos),int(self.numAtributos)))
          print(self.datos.shape)
          i = 0
          j = 0
          for i in range(int(self.numDatos)):
              for j in range(self.numAtributos):
                  self.datos[i][j] = self.diccionarios[j].get(str(datosN[i][j]))
          print(self.numAtributos)
          print(self.numDatos)
          print(self.diccionarios)
          print(self.datos[0])


  # TODO: implementar en la practica 1
  def extraeDatos(self, idx):
    pass
