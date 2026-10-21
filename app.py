#interfaz grafica y de usuario

from kivymd.app import MDApp
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.metrics import dp
from usuario import solicitante, Datosinvalidos
from modelo import modelomorosidad
from repo import rcsv
campos = [
    ("fico", "Puntaje FICO (300-850)", "700"),
    ("dti", "Deuda/ingreso DTI % (0-40)", "12"),
    ("revol_util", "Uso crédito revolvente % (0-120)", "45"),
    ("inq_last_6mths", "Consultas de crédito (6 meses)", "1"),
    ("delinq_2yrs", "Atrasos en 2 años", "0"),
    ("ingreso_anual", "Ingreso anual", "50000"),
]

class app(MDApp):
    title = 'Prediccion de morosidad'

    def build(self):
        Window.size = (1920,1080)
        self.modelo = modelomorosidad()
        self.repo = rcsv()
        self.entradas = {}

        panel = TabbedPanel(do_default_tab = False)
        tab = TabbedPanelItem(text = 'Prediccion')
        tab.add_widget(self.formulario())   
        tab1 = TabbedPanelItem(text = 'Historial')
        tab1.add_widget(self.historial())
        panel.add_widget(tab)
        panel.add_widget(tab1)
        panel.default_tab = tab
        try:
            self.modelo.cargar()

        except:
            self.resultado.text = 'Modelo no encontrado, ejecuta \'entrenar.py\''

        self.actualizar_historial()
        return panel

    def formulario(self):
        self.resultado = Label(text='', font_size='20sp', halign='center')
        raiz = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))
        form = GridLayout(cols=2, spacing=dp(12), size_hint_y=None)
        form.bind(minimum_height=form.setter('height'))
        for clave, etiqueta, defecto in campos:
            form.add_widget(Label(text=etiqueta, size_hint_y=None, height=dp(40), halign='left', text_size=(dp(220), None)))
            campo = TextInput(text=defecto, multiline=False, input_filter='float', size_hint_y=None, height=dp(40))
            self.entradas[clave] = campo
            form.add_widget(campo)
        raiz.add_widget(form)
        raiz.add_widget(Button(text='Calcular Probabilidad', size_hint_y=None, height=dp(48), on_release=self.calcular)) 
        raiz.add_widget(self.resultado)
        return raiz

    def historial(self):
        scroll = ScrollView()
        self.lista = GridLayout(cols=1, spacing=dp(4), size_hint_y=None)
        self.lista.bind(minimum_height=self.lista.setter("height"))
        scroll.add_widget(self.lista)
        return scroll

    def calcular(self, _boton):
        try:
            datos = {k: float(c.text) for k, c in self.entradas.items()}
            Solicitante = solicitante(**datos)
            p = self.modelo.predecir(Solicitante)
            self.repo.guardar({**Solicitante.a_dict(), "probabilidad": p})
            self.resultado.text = f"Probabilidad de morosidad: {p:.1%}"
            self.actualizar_historial()
        except ValueError:
            self.resultado.text = "Completa todos los campos con números."
        except Datosinvalidos as e:
            self.resultado.text = f"Dato inválido: {e}"
        except Exception as e:
            self.resultado.text = f"No se pudo calcular {e}."

    def actualizar_historial(self):
        self.lista.clear_widgets()
        for fila in self.repo.listar():
            p = float(fila('Probabilidad:'))
            texto = (f"{fila['fecha']}  |  FICO {float(fila['fico']):.0f}  |  ", f"DTI{float(fila['dti']):.1f}  | {p:.1%}")
            self.lista.add_widget(Label(text = texto, size_hint_y = None, height = dp(30)))




if __name__ == '__main__':
    app().run()