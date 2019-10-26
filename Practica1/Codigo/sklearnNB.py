import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold, cross_val_predict
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from EstrategiaParticionado import Particion
def validacion_simple_sklearn(dataset, porcentaje):

    # Matriz con los atributos
    X = dataset.datos[:, :-1]

    # Array con las clases
    y = dataset.datos[:, -1]

    # Realizamos la divison en train-test, X_train es la partición sobre la que se va a entrenar e X_test sobre la que se va a clasificar
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=porcentaje, test_size=1 - porcentaje, shuffle=True)

    return X_train, X_test, y_train, y_test

def validacion_cruzada_sklearn(dataset, k):

    # Matriz con los atributos
    X = dataset.datos[:, :-1]

    # Array con las clases
    y = dataset.datos[:, -1]

    kf = KFold(n_splits=k, shuffle=True)

    particiones = []

    for train_index, test_index in kf.split(X,y):
        particiones.append(Particion(train_index,test_index))

    return particiones

def nb_sklearn(x_train, y_train, x_test, tipo="Multinomial", laplace=True):

    if tipo == "Gaussian":
        if laplace == True:
            clf = GaussianNB(alpha=1.0)
        else:
            clf = GaussianNB()

    elif tipo == "Multinomial":
        if laplace == True:
            clf = MultinomialNB(alpha=1.0, fit_prior = True, class_prior = None)
        else:
            clf = MultinomialNB(fit_prior=True, class_prior=False)
    else:
        print("Error, clasificador no valido. Utilizar GaussianNB o MultinomialNB")
        return

    # Entrenamos el modelo
    clf.fit(x_train, y_train)

    # Clasificacion
    prediccion = clf.predict(x_test)

    return prediccion

def nb_sklearn_validacion_cruzada(x_train, y_train, k):

    clf = MultinomialNB(alpha = 1.0, fit_prior = True, class_prior = None)

    error = cross_val_score(clf, x_train, y_train, cv = k)

    return error



def error(clases_predichas, clases_reales):

    return 1 - np.sum(np.equal(clases_predichas, clases_reales)) / len(clases_predichas)