import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold, cross_val_predict
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from EstrategiaParticionado import Particion
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

def validacion_cruzada_sklearn(dataset, k):
    # Matriz con los atributos
    X = dataset.datos[:, :-1]

    # Array con las clases
    y = dataset.datos[:, -1]

    kf = KFold(n_splits=k, shuffle=True)

    particiones = []

    for train_index, test_index in kf.split(X, y):
        particiones.append(Particion(train_index, test_index))

    return particiones

def nb_sklearn(x_train, y_train, x_test, tipo="Multinomial", laplace=True):
    if tipo == "Gaussian":
        clf = GaussianNB()
    elif tipo == "Multinomial":
        if laplace == True:
            clf = MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None)
        else:
            clf = MultinomialNB(alpha=0.01, fit_prior=True, class_prior=None)
    else:
        print("Error, clasificador no valido. Utilizar GaussianNB o MultinomialNB")
        return

    # Entrenamos el modelo
    clf.fit(x_train, y_train)

    # Clasificacion
    prediccion = clf.predict(x_test)

    return prediccion

def nb_sklearn_validacion_cruzada(x_train, y_train, k, tipo="Multinomial", laplace=True):
    if tipo == "Gaussian":
        clf = GaussianNB()

    elif tipo == "Multinomial":
        if laplace == True:
            clf = MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None)
        else:
            clf = MultinomialNB(alpha=0.01, fit_prior=True, class_prior=None)
    else:
        print("Error, clasificador no valido. Utilizar GaussianNB o MultinomialNB")
        return

    acierto = cross_val_score(clf, x_train, y_train, cv=k)

    return acierto, acierto.std()

def matriz_confusion_sklearn(prediccion, clase_real):
    matriz = confusion_matrix(clase_real, prediccion)
    tn, fp, fn, tp = matriz.ravel()

    # Calculamos las tasas extraídas de la matriz de confusión
    tpr = tp / (tp + fn)
    fpr = fp / (fp + fn)

    return matriz, tpr, fpr

def curvaROC_sklearn(fpr, tpr):
    x = np.linspace(0, 1, 100)
    plt.plot(x, x, c='blue')
    plt.plot(fpr, tpr, 'ro')
    plt.show()

def error(clases_predichas, clases_reales):

    error =  1 - (np.sum(np.equal(clases_predichas, clases_reales)) / len(clases_predichas))

    return error