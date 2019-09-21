import numpy as np

class Datos:

  TiposDeAtributos=('Continuo','Nominal')

  # TODO: procesar el fichero para asignar correctamente las variables tipoAtributos, nombreAtributos, nominalAtributos, datos y diccionarios
  # NOTA: No confundir TiposDeAtributos con tipoAtributos
  def __init__(self, nombreFichero):

      with open(nombreFichero, "r") as f:


          # Guardamos el numero de datos que contiene el DataSet y está en la primera linea
          self.numDatos = f.readline()

          # Guardamos el nombre de los atributos
          self.nombreAtributos = f.readline().split(',')

          # Eliminamos el ultimo \n que hay en la linea
          self.nombreAtributos.pop()

          # Leemos el tipo de los atributos de las variables y eliminamos el ultimo que es un salto de linea
          try:
              self.tipoAtributos = f.readline().split(',')
              self.tipoAtributos.pop()
              self.nominalAtributos = []
              for tipo in self.tipoAtributos:
                  if tipo == self.TiposDeAtributos[0]:
                      self.nominalAtributos.append('False')
                  else:
                      self.nominalAtributos.append('True')
              print(self.nominalAtributos)
          except ValueError:
              print("Error")


          # Guardamos el numero de atributos
          self.numAtributos = len(self.nombreAtributos)



  # TODO: implementar en la pr�ctica 1
  def extraeDatos(self, idx):
    pass
