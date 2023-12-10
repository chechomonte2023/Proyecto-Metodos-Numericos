from matplotlib import widgets
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd
st.title("Método Simpson 1/3 Múltiple ")
st.sidebar.markdown("# Regla de Simpson 1/3 Múltiple ")
st.image("http://blog.espol.edu.ec/analisisnumerico/files/2018/08/reglasimpson03.png",use_column_width=True)
st.markdown("""Así como con la regla trapezoidal, la regla de Simpson se puede mejorar al
            dividir el intervalo de integración en un número de segmentos de igual anchura """)
st.latex(r"h=\frac{b-a}{n}")
st.markdown("Al sustituir la regla de Simpson 1/3 para integral individual se obtiene")
st.latex(r"""A=2h\frac{f(x_0) + 4f(x_1) + f(x_2)}{6} + 
         2h\frac{f(x_2) + 4f(x_3) + f(x_4)}{6} + .... +""")
st.latex(r"2h\frac{f(x_{n-2}) + 4f(x_{n-1} + f(x_n)) + f(x_4)}{6}")
# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Definir el rango de entrada
start_range = st.sidebar.slider("Inicio del rango", -20.0, 20.0, 0.1)
end_range = st.sidebar.slider("Fin del rango", -20.0, 20.0, 2.0)

# Ingresar la función
var = st.sidebar.text_input("Variable", "x")
x = sp.symbols(var)
y = st.sidebar.text_input("Función", "x**2")
fx = sp.sympify(y)
a= st.sidebar.number_input("Límite inferior", 1)
b= st.sidebar.number_input("Límite superior", 2)
n= st.sidebar.number_input("Cantidad de segmentos", 2)

f = sp.lambdify(x, fx)

# Espacio reservado para la figura
fig_placeholder = st.empty()
tablita = st.empty()

# Calcular el ancho de cada subintervalo
h = (b - a) / n

# Inicializar la suma de la integral
integral_sum = 0

# Crear un arreglo para almacenar los puntos medios
x_midpoints = np.linspace(a + h / 2, b - h / 2, n)

for x_mid in x_midpoints:
    fa = fx.subs({x: a})
    fb = fx.subs({x: b})
    fm = fx.subs({x: x_mid})

    # Aplicar la regla de Simpson 1/3 en el subintervalo
    subintegral = h * (fa + 4 * fm + fb) / 6

    integral_sum += subintegral

st.text(f"I = {integral_sum}")

# Calcular la integral real utilizando sympy
I_real = sp.integrate(fx, (x, a, b))
st.text(f"La integral por sympy es {I_real}" )

error = sp.Abs((I_real - integral_sum) / I_real) * 100
st.text(f"La integración tiene un error de {error:.2f}%")

# Crear una función lambda para evaluar fx en un arreglo de puntos
fx_lambda = sp.lambdify(x, fx, 'numpy')
x_values = np.linspace(a-1, b+1, 100)
y = fx_lambda(x_values)

plt.figure()

fig, ax = plt.subplots()
ax.plot(x_values, y, color='blue', label=f"${fx}$")
ax.grid()

# Plano cartesiano (Ejes)
ax.vlines(x=0, ymin=min(y), ymax=max(y), color='k')
ax.hlines(y=0, xmin=a, xmax=b, color='k')

# Límites xl y xu
ax.vlines(x=a, ymin=0, ymax=fa, color='r', linestyle='--')
ax.vlines(x=b, ymin=0, ymax=fb, color='r', linestyle='--')

# Dibujar los subintervalos
for i in range(n):
    x_start = a + i * h
    x_end = x_start + h
    ax.vlines(x=x_start, ymin=0, ymax=fx.subs({x: x_start}), color='g', linestyle='--')
    ax.fill([x_start, x_start, x_end, x_end, x_start], [0, fx.subs({x: x_start}), fx.subs({x: x_end}), 0, 0], 'g', alpha=0.2)

plt.grid(True)
plt.legend()

# Mostrar gráfico
plt.show()

# Mostrar la figura en el espacio reservado
fig_placeholder.pyplot(fig)