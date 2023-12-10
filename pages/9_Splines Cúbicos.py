import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd
from scipy.interpolate import CubicSpline

st.sidebar.markdown("# Splines Cubicos")

# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Configuración de la página
st.title("Método Splines Cubicos")
st.write('''
Los Splines Cúbicos son una técnica utilizada en interpolación de datos y ajuste de curvas. Se utilizan para crear una función suave que pasa por un conjunto de puntos de datos. La idea es dividir el dominio en segmentos y ajustar polinomios cúbicos a cada segmento. Estos polinomios se seleccionan de manera que la función resultante sea continua y tenga derivadas continuas hasta la segunda derivada.
''')
st.image("data:image/png;base64,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",width=200, caption='Método gráfico', use_column_width=True)

st.write('''Algoritmo:

Dado un conjunto de puntos de datos (x, y), primero se divide el dominio en segmentos (intervalos) donde se ajustarán los polinomios cúbicos. Esto se hace seleccionando puntos de anclaje o nodos.
Para cada segmento, se ajusta un polinomio cúbico que pasa por los nodos del segmento y satisface las condiciones de continuidad y continuidad de la segunda derivada en los nodos.
Estos polinomios cúbicos se ensamblan para formar la función spline cúbica.''')



Archivo=st.sidebar.file_uploader("Suba el archivo CSV")

# Ingresar la función
var_1 = st.sidebar.text_input("Variable", "X")
var_2= st.sidebar.text_input("Variable", "Y")

# Lee el archivo CSV y almacénalo en un DataFrame
df = pd.read_csv(Archivo)

# Extraer los valores de x e y
x = np.array(df[var_1])
y = np.array(df[var_2])

# Espacio reservado para la figura
fig_placeholder = st.empty()
tablita = st.empty()

# Crea el spline cúbico
spline = CubicSpline(x, y)

x_reg = np.linspace(np.min(x),np.max(x),len(x)+100)

# Realiza predicciones
y_reg = spline(x_reg)

fig, ax = plt.subplots()
plt.scatter(x, y, label="Datos reales")
plt.plot(x_reg, y_reg, color='red', label="Spline Cubico")
plt.legend()
plt.grid()
plt.show()

# Mostrar la figura en el espacio reservado
fig_placeholder.pyplot(fig)