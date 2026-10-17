<<<<<<< HEAD
#clase de usuario, valida datos y crea diccionario 
=======
#clase de usuario, valida datos
>>>>>>> 2aa5f19bbb89525a6e94576873558b06062f3ca0

from pathlib import Path
import math
import pandas as pd

csv_path = Path('proyectofinalprogramacion2/data/loan_data.csv')



class Datosinvalidos(Exception):
    """"clase para datos fuera de rango"""
class solicitante:
    r_datos = {"fico": (300, 850), "dti": (0, 40), "revol_util": (0, 120), "inq_last_6mths": (0, 40), "delinq_2yrs": (0, 20), "ingreso_anual": (1, 5_000_000)}

    def __init__(self, **datos):
        self._datos = {}
        for campo, (minimo, maximo) in self.r_datos.items():
            valor = datos.get(campo)
            if valor is None or not maximo <= valor <= maximo: #valida la entrada de datos
                raise Datosinvalidos(                           
                    f'El campo: {campo} debe estar entre {minimo} y {maximo}'
                )
            self._datos[campo] = valor

    def a_dict(self):
        return dict(self._datos)        #Devuelve como diccionario(getter solo devuelve un atributo)

    def a_dataframe(self):
        d = self.a_dict()
        d['log_annual_inc'] = math.log(d.pop('Ingreso_anual')) #csv usa log
<<<<<<< HEAD
        return pd.DataFrame([d]) 
=======
        return pd.DataFrame([d])

#prueba
p0 = solicitante(fico = 900, dti = 0, revol_util = 0, inq_last_6mths = 0, delinq_yrs = 0, ingreso_anual = 1)

>>>>>>> 2aa5f19bbb89525a6e94576873558b06062f3ca0
