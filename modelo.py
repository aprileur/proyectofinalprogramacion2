#entrenamiento, prediccion y persistencia de datos

import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression #calcula probabilidad de morosidad
from sklearn.metrics import roc_auc_score #regresa un real 0.5-1, 0.5 azar 1 perfecto
from sklearn.model_selection import train_test_split  #reparte filas entre entrenamiento y test
from sklearn.pipeline import Pipeline #encadenamos pasos
from sklearn.preprocessing import StandardScaler #estandariza las variables para compararlas


func = ["fico", "dti", "revol_util", "inq_last_6mths",
        "delinq_2yrs", "log_annual_inc"]
class modelomorosidad():
    ruta = 'modelos/modelo.joblib' #ruta para persistencia de datos con joblib

    def __init__(self):
        self.pipe = None

    def entrenar(self, ruta_csv):
        datos = pd.read_csv(ruta_csv)
        datos.columns = [c.replace('.', '_') for c in datos.columns]
        X, y = datos[func], datos['not_fully_paid']
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,stratify=y, random_state=50)  #random state elegido arbitrario para reproducir resultados
        self._pipe = Pipeline([('Escala', StandardScaler()), ('lr', LogisticRegression(max_iter=1000))]) 
        self._pipe.fit(X_tr, y_tr) #aprendizaje
        return roc_auc_score(y_te, self._pipe.predict_proba(X_te)[:, 1] )    

    def guardado(self):
        os.makedirs('modelos', exist_ok=True) #crea la ruta, github no permite subir carpeta vacia
        joblib.dump(self._pipe, self.ruta)

    def cargar(self):
        self._pipe = joblib.load(self.ruta)

    def predecir(self, solicitante):
        X = solicitante.a_dataframe()[func]
        return float(self._pipe.predict_proba(X)[0,1])