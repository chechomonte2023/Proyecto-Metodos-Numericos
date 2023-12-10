from matplotlib import widgets
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.sidebar.markdown("# Regla Trapezoidal ")

# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Configuración de la página
st.title("Método Regla Trapezoidal ")
st.write('''En matemática la regla del trapecio es un método de integración numérica, es decir, un método para calcular aproximadamente el valor de la integral definida.
''')
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQn7VebhLTYA7tXpLmPqV1KqelHUBt6a7speg&usqp=CAU", caption='Método gráfico ', use_column_width=True)
st.write('''La regla se basa en aproximar el valor de la integral de $f(x)$ por el de la función lineal que pasa a través de los puntos $(a,f(a))$ y $(b,f(b))$''')
st.image("https://multimedia.uned.ac.cr/pem/metodos_numericos_ensenanza/modulo4/img/des/trapecio3.jpg", caption='Método gráfico ', use_column_width=True)
st.write('''El objetivo de la regla es aproximar la integral a un polinomio de grado 1.

$$
I = ∫^b_a f(x)dx ≈ ∫^b_a f_1(x)dx \therefore F_1(x)
$$

Se aproxima a una linea recta.

$$
y - y_1 = m(x - x_i)
$$

Reemplazando con los valores de la imágen anterior...

$$
y - f(a) = \\frac{f(b) - f(a)}{b - a} (x - a)
$$

$$
y  = f(a) + \\frac{f(b) - f(a)}{b - a} (x - a) = f_1(x)
$$

Entonces regresando la integración

$$
I = ∫^a_b [f(a) + \\frac{f(b) - f(a)}{b - a}(x - a)] dx
$$

Después de integrar tenemos la **Regla trapezoidal**

$$
I = (b-a) \\frac{f(a)+f(b)}{2}
$$

Donde:

$I=$ área del trapecio

$(b - a) =$ ancho del trapecio

$\\frac{f(a)+f(b)}{2} = $ altura promedio

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

# Espacio reservado para la figura
fig_placeholder = st.empty()
tablita = st.empty()

# Calcular f(a) y f(b)
fa = fx.subs({x: a})
fb = fx.subs({x: b})

st.text(f"f(a) = {fa}")
st.text(f"f(b) = {fb}")

# Aplicar la regla trapezoidal para aproximar la integral
I = (b - a) * ((fa + fb) / 2)
print("I =", I)
st.text(f"I = {I}")

# Calcular el error
true_value = sp.integrate(fx, (x, a, b)).evalf()
error = np.abs((true_value - I) / true_value) * 100
st.text(f"El error es de {round(error, 4)}%")

# Creación de un gráfico
x_values = np.linspace(a-1, b+1, 100)
y_values = [fx.subs({x: val}).evalf() for val in x_values]

fig, ax = plt.subplots()
ax.plot(x_values, y_values, color='blue', label=f"${fx}$")
ax.grid()

# Ejes del plano cartesiano
ax.vlines(x=0, ymin=min(y_values), ymax=max(y_values), color='k')
ax.hlines(y=0, xmin=a, xmax=b, color='k')

# Límites a y b
ax.vlines(x=a, ymin=0, ymax=fa, color='r', linestyle='--')
ax.vlines(x=b, ymin=0, ymax=fb, color='r', linestyle='--')
ax.plot([a, b], [fa, fb], color='r', linestyle='--')

# Área bajo la curva
ax.fill([a, a, b, b], [0, fa, fb, 0], 'r', alpha=0.2)

plt.grid(True)
plt.legend()

# Mostrar gráfica
plt.show()

# Mostrar la figura en el espacio reservado
fig_placeholder.pyplot(fig)