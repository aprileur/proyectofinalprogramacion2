#clase para guardar consultas en base de datos csv

import csv
import os
from abc import ABC, abstractmethod
from datetime import datetime

class repo(ABC):
    @abstractmethod
    def guardar(self, registro: dict): ...
    @abstractmethod
    def listar(self,list) -> list: ...

class rcsv(repo):
    campos = ['fecha', 'fico', 'dti', 'revol_util', 'inq_last_6mths', 'delinq_2yrs', 'ingreso_anual', 'probabilidad']

    def __init__(self, ruta = 'data/historial.csv'):
        self._ruta = ruta
        os.makedirs(os.path.dirname(self._ruta), exist_ok=True)
        if not os.path.exists(self._ruta):
            with open(self._ruta, 'w', newline='', encoding= 'UTF-8') as f: csv.DictWriter(f, fieldnames = self.campos).writeheader()

    def guardar(self, registro):
        registro = {**registro, "fecha": datetime.now().isoformat(timespec="seconds")}
        with open(self._ruta, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=self.campos).writerow(registro)

    def listar(self):
        with open(self._ruta, newline="", encoding="utf-8") as f:
            filas = list(csv.DictReader(f))
        return filas[::-1] 

