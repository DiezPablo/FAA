from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt

def validacion_simple_sklearn(dataset, porcentaje):
    # Matriz con los atributos
    X = dataset.datos[:, :-1]

    # Array con las clases
    y = dataset.datos[:, -1]

    # Realizamos la divison en train-test, X_train es la partición sobre la que se va a entrenar e X_test sobre la que se va a clasificar
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=porcentaje, shuffle=True)

    return X_train, X_test, y_train, y_test

def knn_val_simple(x_train, y_train, x_test, k, weights = 'uniform'):

    if weights == 'uniform':
        neigh = KNeighborsClassifier(n_neighbors = k, metric = 'euclidean', weights = weights)
    elif weights == 'distance':
        neigh = KNeighborsClassifier(n_neighbors = k, metric = 'euclidean', weights = weights)
    else:
        print('Introduzca uniform/distance')
        return

    neigh.fit(x_train, y_train)

    predicciones = neigh.predict(x_test)

    return predicciones

def knn_val_cruzada(x_train, y_train, k, n_vecinos, weights = 'uniform'):

    if weights == 'uniform':
        neigh = KNeighborsClassifier(n_neighbors = n_vecinos, metric = 'euclidean', weights = weights)
    elif weights == 'distance':
        neigh = KNeighborsClassifier(n_neighbors = n_vecinos, metric = 'euclidean', weights = weights)
    else:
        print('Introduzca uniform/distance')
        return

    acierto = cross_val_score(neigh, x_train, y_train, cv=k)

    return acierto, acierto.std()

def error(clases_predichas, clases_reales):

    error =  1 - (np.sum(np.equal(clases_predichas, clases_reales)) / len(clases_predichas))

    return error

def regresionLog_val_simple(x_train, y_train, x_test):

    logistic_regression = LogisticRegression(max_iter = 1000000, solver = 'lbfgs')
    logistic_regression.fit(x_train, y_train)
    predicciones = logistic_regression.predict(x_test)

    return predicciones

def regresionLog_val_cruzada(x_train, y_train, k):

    logistic_regression = LogisticRegression(max_iter= 1000000, solver = 'lbfgs')

    acierto = cross_val_score(logistic_regression, x_train, y_train, cv=k)

    return acierto, acierto.std()