#interfaz grafica y de usuario

import pandas as pd
import streamlit as st
from usuario import solicitante, Datosinvalidos
from modelo import modelomorosidad
from repo import rcsv

@st.cache_data
def cargar_modelo():
    m = modelomorosidad()
    m.cargar()
    return m

modelo = cargar_modelo()
repo = rcsv()

st.title('Prediccion de morosidad')

with st.form('formulario'):
    fico = st.number_input('Puntaje de credito', 300, 850, 700)
    dti = st.number_input('Deuda/ingreso (dti%)', 0.0, 42.0, 12.0)
    revol_util = st.number_input('Uso de credito revolvente (%)', 0.0, 120.0, 45.0)
    inq = st.number_input('Consultas de credito en 6 meses', 0, 40, 1)
    delinq = st.number_input('Atrasos en 2 años', 0, 20, 0)
    ingreso = st.number_input('ingreso anual', 1.00, 5_000_000.0, 50000.0)
    enviar = st.form_submit_button('Calcular')

if enviar:
    try:
        s = solicitante(fico = fico, dti = dti, revol_util = revol_util, inq_last_6mths = inq, delinq_2yrs = delinq, ingreso_anual = ingreso)
        p = modelo.predecir(s)
        st.metric('Probabilidad de morosidad:', f'{p:.1%}')
        repo.guardar({**s.a_dict(),'probabilidad': p})
    except Datosinvalidos as e:
        st.error(str(e))
st.subheader('Historial')
st.dataframe(pd.DataFrame(repo.listar()))