from matplotlib import widgets
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.title("Método Simpson 3/8 Simple ")
st.sidebar.markdown("# Regla de Simpson 3/8 Simple ")
st.image("https://www.lifeder.com/wp-content/uploads/2020/03/Simpson-01.jpg",use_column_width=True)
st.markdown("""Es una manera similar a la derivación de la regla trapezoidal y de Simpson
            1/3, un polinomio de Lagrange de tercer orden se puede ajustar a cuatro puntos
            a integrarse """)
st.image("https://1.bp.blogspot.com/_3RQwjNtZeSY/TEHQQr2r1TI/AAAAAAAAADc/2Cb_UxIQVvI/s400/Integral+definida.jpg",width=200,)
st.markdown("Para obtener: ")
st.latex(r"A=\frac{3h}{8}(f(x_0) + 3f(x_1) + 3f(x_2) + f(x_3))")
st.markdown("""donde $h=(b-a)/3$. Esta ecuación se llama $regla de Simpson 3/8$ debido 
            a que $h$ se multiplica por 3/8. Esta es la fórmula de integración cerrada
            de Newton-Cotes. La regla 3/8 también se puede expresar de la forma:""")
st.latex(r"A=(b-a)\frac{f(x_0) + 3f(x_1) + 3f(x_2) + f(x_3)}{8}")
# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Ingresar la función
var = st.sidebar.text_input("Variable", "x")
x = sp.symbols(var)
y = st.sidebar.text_input("Función", "x**2")
fx = sp.sympify(y)
lim_inf= st.sidebar.number_input("Límite inferior", 1)
lim_sup= st.sidebar.number_input("Límite superior", 2)

f = sp.lambdify(x, fx)


# Espacio reservado para la figura
fig_placeholder = st.empty()
tablita = st.empty()
t = np.linspace(lim_inf, lim_sup, 4)

m=(lim_inf+lim_sup)/2

I=(lim_sup-lim_inf)*((f(t[0])+3*f(t[1])+3*f(t[2])+f(t[3]))/8)

st.text(f"I = {round(I,4)} U^2")
ar = sp.integrate(fx, (x, lim_inf, lim_sup))
st.text(f"Área real ={round(ar, 4)} U^2")
e = np.abs((ar - I) / ar) * 100
st.text(f"El error es del {round(e, 2)}%")
plt.figure()

r = np.linspace(lim_inf-1,lim_sup+1, 100)
fg=[fx.subs({x:xi}) for xi in r]

fig, ax = plt.subplots()
ax.plot(r,fg,color='blue',label=f"${fx}$")
ax.grid()

ax.vlines(x=0,ymin=min(fg),ymax=max(fg),color='k')
ax.hlines(y=0,xmin=min(r),xmax=max(r),color='k')

ax.vlines(x=lim_inf, ymin=0, ymax=f(t[0]), color='r', linestyle='--')
ax.vlines(x=lim_sup, ymin=0, ymax=f(t[3]), color='r', linestyle='--')

ax.fill([lim_inf,lim_inf,m,lim_sup,lim_sup],[0,f(t[0]),f(m),f(t[3]),0], 'r', alpha=0.2)

plt.grid(True)
plt.legend()

plt.show()


# Mostrar la figura en el espacio reservado
fig_placeholder.pyplot(fig)