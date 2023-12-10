from matplotlib import widgets
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.sidebar.markdown("# Regla de Simpson 1/3 Simple ")

# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Configuración de la página
st.title("Método Simpson 1/3 Simple ")
st.write('''Esta regla no ajusta la curva a integrar por medio de una recta sino por una interpolación polinomial de segundo orden.''')
st.image("https://www.freecodecamp.org/news/content/images/2020/02/sim01.jpg", caption='Método gráfico ', use_column_width=True)
st.write('''Como se muestra en el diagrama anterior, el integrando $f(x)$ es aproximado por un polinomio de segundo orden, el interpolante cuadrático es $P(x)$.

Sigue la aproximación para $I$ ''')
st.image("https://www.freecodecamp.org/news/content/images/2020/02/sim3.png", caption='Método gráfico ', use_column_width=True)
st.write('''Reemplazando $\\frac{(b-a)}{2}$ como $h$ , obtenemos $I$ como: ,''')
st.image("https://www.freecodecamp.org/news/content/images/2020/02/sim4.png", caption='Método gráfico ', use_column_width=True)
st.write('''
Como puedes ver, hay un factor de $\\frac{1}{3}$ en la expresión anterior. Por eso, se llama la Regla de $\\frac{1}{3}$ de Simpson.
### Error absoluto

$$
e_{absoluto} = |\\frac{I_{real} - I_{aprox}}{I_{real}}|
$$''')

# Definir el rango de entrada
start_range = st.sidebar.slider("Inicio del rango", -20.0, 20.0, 0.1)
end_range = st.sidebar.slider("Fin del rango", -20.0, 20.0, 2.0)

# Ingresar la función
var = st.sidebar.text_input("Variable", "x")
x = sp.symbols(var)
y = st.sidebar.text_input("Función", "3*x**2")
fx = sp.sympify(y)
lim_inf= st.sidebar.number_input("Límite inferior", 1)
lim_sup= st.sidebar.number_input("Límite superior", 2)

f = sp.lambdify(x, fx)


# Espacio reservado para la figura
fig_placeholder = st.empty()
tablita = st.empty()

m=(lim_inf+lim_sup)/2

fa=f(lim_inf)
fb=f(lim_sup)
fm=f(m)

I = (lim_sup-lim_inf) * ((fa + 4*fm + fb)/6)
st.text(f"I = {round(I , 4)} U^2")

ar = sp.integrate(fx, (x, lim_inf, lim_sup))
st.text(f"Área real = {round(ar, 4)} U^2")

e = np.abs((ar - I) / ar) * 100
st.text(f"El error es del {round(e, 2)}%")

plt.figure()

r = np.linspace(start_range, end_range, 100)
fg=[fx.subs({x:xi}) for xi in r]

fig, ax = plt.subplots()
ax.plot(r,fg,color='blue',label=f"${fx}$")
ax.grid()

ax.vlines(x=0,ymin=min(fg),ymax=max(fg),color='k')
ax.hlines(y=0,xmin=min(r),xmax=max(r),color='k')

ax.vlines(x=lim_inf, ymin=0, ymax=fa, color='r', linestyle='--')
ax.vlines(x=lim_sup, ymin=0, ymax=fb, color='r', linestyle='--')

ax.fill([lim_inf,lim_inf,m,lim_sup,lim_sup],[0,fa,fm,fb,0], 'r', alpha=0.2)

plt.grid(True)
plt.legend()

plt.show()

# Mostrar la figura en el espacio reservado
fig_placeholder.pyplot(fig)