from matplotlib import widgets
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.sidebar.markdown("# Euler ")

# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Configuración de la página
st.title("Método Euler")
st.write('''En matemática y computación, el método de Euler, llamado así en honor de Leonhard Euler, es un procedimiento de integración numérica para resolver ecuaciones diferenciales ordinarias a partir de un valor inicial dado.

El método de Euler es el más simpe de los métodos numéricos. útil para resolver PVI.

Problema de valores inciales (PVI)

$$PVI => \\frac{dy}{dx} = f(x,y) ; y(x_0) = y_0 ; y(x_i) = ?$$

Consiste en dividir los intervalos que van desde $x_0$ a $x_f$ en $n$ intervalos de ancho $h$ de la forma:

$$h = \\frac{x_f - x_0}{n}$$


De esta manera se obtiene un conjunto discreto de $n+1$ puntos: $x_0,x_1,x_2,x_3,...,x_n$ del intervalo de interés $[x_0 , x_f]$. Para cualquiera de estos puntos se cumple que:

$$x_i = x_0 + i * h$$

con:  $0 ≤ i ≤ n$

La condición inicial $y(x_0) = y_0$, representa el punto $P_0 = (x_0, y_0)$ por donde pasa la curva solución de la ecuación del planteamiento inicial, la cual se denota como $F(x) = y$

Ya teniendo el punto $P_0$ se puede evaluar la primera derivada de $F(x)$ en ese punto, por lo tanto:

$$F'(x) = \\frac{dy}{dx} ]_{P_0} = f'(x_0,y_0)$$''')
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Metodo_de_Euler.png/500px-Metodo_de_Euler.png", caption='Método gráfico ', use_column_width=True)

st.write('''Con esta información se traza una recta, aquella que pasa por $P_0$ y de pendiente $f'(x_0, y_0)$. Esta recta aproxima a $F(x)$ en una vecindad de $x_0$

Tóme la recta como reemplazo de $F(x)$ y localice en la recta el valor de $y$ correspondiente $x_1$. Entonces, podemos deducir según la gráfica que:

$$\\frac{y_1 - y_0}{x_1 - x_0} = f'(x_0,y_0)$$

Si se resuelve para $y_1$

$$y_1 = y_0 + (x_1 - x_0)f'(x_0,y_0) = y_0 +h f'(x_0,y_0)$$

El valor de la imágen puede iterarse de la siguiente forma:

$$y_1 = y_0 + hf'(x_0,y_0)$$
$$y_2 = y_1 + hf'(x_1,y_1)$$
$$…$$
$$y_{i+1} = y_i + hf'(x_i,y_i)$$
$$…$$
$$y_n = y_{n-1} + hf'(x_{n-1},y_{n-1})$$

## Algoritmo de Euler para la integración


1. Hacer $y_{i+1} = y_i + hf'(x_i,y_i)$
2. Hacer $x_{i} = x_{i+1}$''')
# Definir el rango de entrada
start_range = st.sidebar.slider("Inicio del rango", -20.0, 20.0, 0.1)
end_range = st.sidebar.slider("Fin del rango", -20.0, 20.0, 2.0)

# Ingresar la función
var = st.sidebar.text_input("Variable", "x")
x = sp.symbols(var)
func = st.sidebar.text_input("Función", "3*x**2")
df = sp.sympify(func)
y0= st.sidebar.number_input("y(0)", 1)
ti= st.sidebar.number_input("Tiempo Inicial", -2)
h= st.sidebar.number_input("Paso de integración", 0.2)
tf= st.sidebar.number_input("Tiempo Final", 2)
xe = np.arange(ti, tf + h, h)
y=np.empty_like(xe)

# Espacio reservado para la figura
fig_placeholder = st.empty()
tablita = st.empty()

f=sp.integrate(df)
y[0] = f.subs({x:0})

for i in range(ti,len(y)-1):
  y[i+1] = y[i] + h * df.subs({x:xe[i]})

xg=np.linspace(ti,tf,100)
fg=[f.subs({x:xi}) for xi in xg]

plt.figure()
fig, ax = plt.subplots()
ax.grid()
ax.plot(xe,y, marker='o', label ="Metodo Euler")
ax.plot(xg,fg, label="Real")
ax.legend()
plt.figure()
# Mostrar la figura en el espacio reservado
fig_placeholder.pyplot(fig)