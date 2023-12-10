import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd


# Configuración de la página
st.title("Método Simpson 3/8 Múltiple ")
st.markdown("# Métodos Numéricos y Optimización ")

st.sidebar.markdown("# Regla de Simpson 3/8 Múltiple ")
st.image("https://multimedia.uned.ac.cr/pem/metodos_numericos_ensenanza/glosario/img/Simpson2.jpg",use_column_width=True)
st.markdown("""La regla de Simpson 3/8 múltiple se utiliza para aproximar la integral 
            definida de una función sobre un intervalo dado. La fórmula básica para la 
            regla de Simpson 3/8 simple es: """)
st.latex(r'\int_{a}^{b} f(x) \,dx \approx \frac{8}{3h} \left[ f(a) + 3f(x_1) + 3f(x_2) + 2f(x_3) + 3f(x_4) + \ldots + 3f(x_{n-2}) + 3f(x_{n-1}) + f(b) \right]')
st.markdown("""donde $h$ es el ancho de cada subintervalo, dado por $h=(b-a)/n$ y $n$
            el es un número total de subintervalos.
            Para la regla de Simpson 3/8 múltiple, el número total de puntos $(n)$
             debe ser un múltiplo de 3, y la fórmula se aplica a cada conjunto de tres
             subintervalos.
            Supongamos que tenemos $n$ puntos equidistantes en el intervalo $[a,b]$ con $n$
             divisible por 3, entonces la aproximación de la integral utilizando la regla 
            de Simpson 3/8 múltiple sería:""")
st.latex(r'\int_{a}^{b} f(x) \,dx \approx \frac{8}{3h} \left[ f(a) + 3f(x_1) + 3f(x_2) + 2f(x_3) + 3f(x_4) + \ldots + 3f(x_{n-2}) + 3f(x_{n-1}) + f(b) \right]')
# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]


# Definir el rango de entrada
start_range = st.sidebar.slider("Inicio del rango", -20.0, 20.0, 0.1)
end_range = st.sidebar.slider("Fin del rango", -20.0, 20.0, 2.0)

# Ingresar la función
var = st.text_input("Variable", "x")
x = sp.symbols(var)
y = st.text_input("Función", "x**2")
fx = sp.sympify(y)
a = st.number_input("Límite inferior", 1)
b = st.number_input("Límite superior", 2)
n = st.number_input("Cantidad de segmentos", 2)

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

    # Aplicar la regla de Simpson 3/8 compuesto en el subintervalo
    subintegral = (3 * h / 8) * (fa + 3 * fm + 3 * fx.subs({x: x_mid + h / 3}) + fx.subs({x: x_mid + 2 * h / 3}) + fb)

    integral_sum += subintegral

# Mostrar la suma de la integral en Streamlit
st.text(f"I = {integral_sum}")

# Calcular la integral real utilizando sympy
I_real = sp.integrate(fx, (x, a, b))
st.text(f"La integral por sympy es {I_real}" )

error = sp.Abs((I_real - integral_sum) / I_real) * 100
st.text(f"La integración tiene un error de {error:.2f}%")

# Crear una función lambda para evaluar fx en un arreglo de puntos
fx_lambda = sp.lambdify(x, fx, 'numpy')
x_values = np.linspace(a - 1, b + 1, 100)
y = fx_lambda(x_values)

# Crear el gráfico en Streamlit
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

# Añadir leyenda y etiquetas
ax.legend()
ax.set_xlabel("x")
ax.set_ylabel("f(x)")

# Mostrar el gráfico en Streamlit
fig_placeholder.pyplot(fig)