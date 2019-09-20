import numpy as np

class Datos:

  TiposDeAtributos=('Continuo','Nominal')

  # TODO: procesar el fichero para asignar correctamente las variables tipoAtributos, nombreAtributos, nominalAtributos, datos y diccionarios
  # NOTA: No confundir TiposDeAtributos con tipoAtributos
  def __init__(self, nombreFichero):

      with open(nombreFichero, "r") as f:

          # Guardamos el numero de datos que contiene el DataSet y está en la primera linea
          self.numDatos = f.readLine()

          # Guardamos el nombre de los atributos
          self.nombreAtributos = f.readLine().split(',')

          # Eliminamos el ultimo \n que hay en la linea
          self.nombreAtributos.pop()

          # Leemos el tipo de los atributos de las variables y eliminamos el ultimo que es un salto de linea
          try:
              self.tipoAtributos = f.readLine.split(',')
              self.tipoAtributos.pop()
          except ValueError:
              

          # Guardamos el numero de atributos
          self.numAtributos = len(self.nombreAtributos)



  # TODO: implementar en la pr�ctica 1
  def extraeDatos(self, idx):
    pass
