datosAux = f.readlines()
datosN = []
for dat in datosAux:
    datosN.append(dat.split(','))

#datos = f.readline().split(',')
#print(datos)
j = 0
i = 0
#k = 0
valores = []
dic = {}
for j in range(self.numAtributos):
    for i in range(int(self.numDatos)):
        if datosN[i][j] not in valores:
          valores.append(datosN[i][j])
#print(valores)
k = 0
for valor in valores:
    dic.update({valor:k})
    k = k+1
#print(dic)
self.diccionarios = []
i = 0
for i in range(self.numAtributos):
    #print(self.nominalAtributos[i])
    if self.nominalAtributos[i] == True:
        self.diccionarios.append(dic)
    else:
        self.diccionarios.append({})
#self.diccionarios.append({'positive\r\n':1, 'negative\r\n':0})
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
print(self.datos)
