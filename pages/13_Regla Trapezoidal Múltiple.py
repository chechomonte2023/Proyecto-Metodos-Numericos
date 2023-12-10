from matplotlib import widgets
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.sidebar.markdown("# Regla Trapezoidal Múltiple")

# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Configuración de la página
st.title("Método Regla Trapezoidal Múltiple ")
st.write('''
Mejora la regla trapezoidal con el fin de partir el intervalo de integración en varios segmentos y aplicar la regla trapezoidal varias veces para dar mayor precisión.
''')
st.image("https://www.neurochispas.com/wp-content/uploads/2022/12/Regla-de-los-trapecios-ejercicio-3-grafica.jpg", caption='Método gráfico ', use_column_width=True)
st.write('''Donde


$$
h = \\frac{b - a}{n}
$$

$h =$ ancho del segmento

$n =$ número de segmentos deseados

$a = x_0$

$b = x_n$


Entonces la formula queda:

$$
I = \\frac{h}{2} [f(x_0) + 2 ∑_{i=1}^{n-1} f(x_i) + f(x_n)]
$$

que se traduce en:

$$
I = (b-a) [\\frac{f(x_0) + 2 ∑_{i=1}^{n-1} f(x_i) + f(x_n)}{2n}]
$$

## Error absoluto

$$
e_{absoluto} = |\\frac{I_{real} - I_{aprox}}{I_{real}}|
$$''')

# Definir el rango de entrada
start_range = st.sidebar.slider("Inicio del rango", -20.0, 20.0, 0.1)
end_range = st.sidebar.slider("Fin del rango", -20.0, 20.0, 2.0)

# Ingresar la función
var = st.sidebar.text_input("Variable", "x")
x = sp.symbols(var)
fx = st.sidebar.text_input("Función", "3*x**2")
fx = sp.sympify(fx)
a= st.sidebar.number_input("Valor 1", 1)
a = float(a)
b= st.sidebar.number_input("Valor 2", 2)
b = float(b)
n= st.sidebar.number_input("Número de segmentos", 2)

# Espacio reservado para la figura
fig_placeholder = st.empty()
tablita = st.empty()

r = np.linspace(start_range, end_range, 100)

y = [float(round(fx.subs({x: ti}), 3)) for ti in r]
f= sp.lambdify(x,fx)
sum=0.0

h = (b-a) / n

for i in range(1,len(r)-1):
  sum+=f(r[i])

I = h / 2 * (f(r[0]) + 2 * sum + f(r[-1]))

# Calcular la integral real utilizando sympy
I_real = sp.integrate(fx, (x, a, b))
error = np.abs((I_real - I) / I_real) * 100

y = [float(fx.subs({x: val})) for val in r]

fig, ax = plt.subplots()
ax.plot(r, y, color='blue', label=f"${fx}$")
ax.grid()

# Ejes del plano cartesiano
ax.vlines(x=0, ymin=min(y), ymax=max(y), color='k')
ax.hlines(y=0, xmin=min(r), xmax=max(r), color='k')

# Límites xl y xu
ax.vlines(x=a, ymin=0, ymax=float(fx.subs({x: a})), color='r', linestyle='--')
ax.vlines(x=b, ymin=0, ymax=float(fx.subs({x: b})), color='r', linestyle='--')

x_values = np.arange(a, b + h, h)
y_values = [float(fx.subs({x: val})) for val in x_values]

for i in range(n):
    ax.vlines(x=x_values[i + 1], ymin=0, ymax=y_values[i + 1], color='r', linestyle='--')
    ax.plot([x_values[i], x_values[i + 1], x_values[i + 1]], [y_values[i], y_values[i + 1], y_values[i + 1]], 'r', alpha=0.2)
    ax.fill_between([x_values[i], x_values[i + 1]], [y_values[i], y_values[i + 1]], color='r', alpha=0.2)

plt.grid(True)
plt.legend()

# Mostrar gráfico
plt.show()
st.text(f"La integral por aproximación es: {I}")
st.text(f"La integral por sympy es: {I_real}")
st.text(f"La integración tiene un error de {error:.2f}%")

# Mostrar la figura en el espacio reservado
fig_placeholder.pyplot(fig)