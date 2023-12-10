import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.title("Método de Runge Kutta para solución de ecuaciones diferenciales")
st.markdown("""El método de Runge-Kutta de segundo orden, a menudo denominado método RK, 
            es una técnica numérica utilizada para resolver ecuaciones diferenciales 
            ordinarias (EDOs). Es una mejora respecto al método de Euler, ofreciendo 
            mayor precisión. En general, los métodos de Runge-Kutta son muy populares 
            debido a su balance entre precisión y eficiencia computacional, pero todos
             tienen la forma generalizada de la ecuación: """)
st.latex(r"y_{i+1} = y_i + ϕ(x_i,y_i,h)h")
st.markdown("""Donde $ϕ(x_i,y_i,h)$ se conoce como __funcion incremento__, la cual puede 
            interpretarse como una pendiente representativa en el intervalo. La función 
            incremento se escribe de la forma general como: """)
st.latex(r"ϕ = a_1k_1 + a_2k_2 + a_3k_3 + ... + a_nk_n")
st.markdown("Donde a son constantes y las $k$ son:")
st.latex(r"k_1 = f(x_i,y_i)")
st.latex(r"k_2 = f(x_i + p_1h,y_i +q_{11}k_1h)")
st.latex(r"k_3 = f(x_i + p_2h,y_i +q_{21}k_1h + q_{22}k_2h)")
st.markdown("""Donde las $p$ y las $q$ son constantes. Observe que las $k$ son relaciones 
            de recurrencia. Es decir, $k_1$ aparece en la ecuación $k_2$, la cual aparece 
            en la ecuación $k_3$, etcétera. Como cada k es una evaluación funcional, esta
             recurrencia vuelve eficientes a los métodos RK para cálculos en computadora.
 Es posible tener varios tipos de métodos de Runge-Kutta empleando diferentes
             números de términos en la función incremento especificada por n. Observe que
             el método de Runge-Kutta (RK) de primer orden con n = 1 es, de hecho, el 
            método de Euler.""")


st.header("Runge Kutta de Orden 2")
st.markdown(" La versión de segundo orden del método es")
st.latex(r"y_{i+1} = y_i + (a_1k_1 + a_2k_2)h")
st.markdown("Donde: ")
st.latex(r"k_1 = f(x_i,y_i)")
st.latex(r"k_2 = f(x_i+p_1h, y_i + q_{11}k_1h)")
st.markdown("En este punto por igualación y semenjanza con la relación de series de taylor podemos decir que:")
st.latex(r"a_1 = 1 - a_2")
st.latex(r"p_1 = q_{11} = \frac{1}{2a_2}")
st.markdown("""Debido a que podemos elegir un número infinito de valores para a2, hay un 
            número infinito de métodos RK de segundo orden. Cada versión daría exactamente
             los mismos resultados si la solución de la EDO fuera cuadrática, lineal o una 
            constante. Sin embargo, se obtienen diferentes resultados cuando (como 
            típicamente es el caso) la solución es más complicada. """)

st.markdown("### Método de Heun con un solo corrector ($a_2 = 1/2)$")
st.markdown("La fórmula para calcular el siguiente queda:")
st.latex(r"y_{i+1} = y_i + (\frac{1}{2}k_1 + \frac{1}{2}k_2)h")
st.markdown("Donde: ")
st.latex(r"k_1 = f(x_i,y_i)")
st.latex(r"k_2 = f(x_i+h, y_i +k_1h)")

st.markdown("""A continuación, emplearemos el método de Runge-Kutta de orden 2 para la solución del
            siguiente sistema de ecuaciones diferenciales """)
st.markdown("Estas ecuaciones modelan un Circuito RLC, de la forma:")
st.latex(r"\frac{{di}}{{dt}} =  - \frac{R}{L}i(t) - \frac{1}{L}v(t) + \frac{1}{L}vi\\")
st.latex(r"\frac{{dv}}{{dt}} = \frac{1}{C}i(t)")
st.markdown("Asumiremos los valores $R,L,C=1$")

var_1 = st.sidebar.text_input("Variable dependiente 1 ","i")
var_2 = st.sidebar.text_input("Variable dependiente 2 ","v")
func_1 = st.sidebar.text_input("Función 1 ","1-i-v")
func_2 = st.sidebar.text_input("Función 2 ","i")
t0 = st.sidebar.number_input("Tiempo inicial t0",0)
tf = st.sidebar.number_input("Tiempo final tf",10)
dt = st.sidebar.slider("Paso del tiempo dt",0.0,2.0,0.1)
initial_var_1=st.sidebar.number_input("Valor inicial de la variable 1",0.1)
initial_var_2=st.sidebar.number_input("Valor inicial de la variable 2",0.1)


fig_placeholder= st.empty()

def runge_kutta_2(funcs, y0, t0, tf, dt):
    t_values = np.arange(t0, tf, dt)
    y_values = [np.array(y0)]

    for t in t_values[:-1]:
        y_current = y_values[-1]
        k1 = np.array([f(*y_current, t) for f in funcs])
        k2 = np.array([f(*(y_current + k1 * dt), t + dt) for f in funcs])

        y_next = y_current + dt * (0.5 * k1 + 0.5 * k2)
        y_values.append(y_next)

    return t_values, np.array(y_values).T

func_1 = sp.sympify(func_1)
func_2 = sp.sympify(func_2)

# Condiciones iniciales y rango de tiempo
time_range = (t0, tf)

# Condiciones iniciales para i y v
initial_conditions = [initial_var_1, initial_var_2]

# Modifica las funciones para devolver valores numéricos
a=sp.symbols(var_1)
b=sp.symbols(var_2)

def func_a(a,b, t):
    return func_1.evalf(subs={sp.symbols(var_1): a, sp.symbols(var_2): b})

def func_b(a, b, t):
    return func_2.evalf(subs={sp.symbols(var_1): a, sp.symbols(var_2): b})

# Solución aproximada para i(t) y v(t) usando el Método de Euler para sistemas
t_values_rk2, [v1, v2] = runge_kutta_2(
    [func_a, func_b], initial_conditions, t0, tf, dt
)

fig, axs = plt.subplots(1,2,figsize=(20,6))

axs[0].plot(t_values_rk2, v1, label=f'Aproximado ${a}$(t)', linestyle='--')
axs[0].set(xlabel=f"${a}$")
axs[0].set(ylabel=f'${a}(t)$')
axs[0].set_title(f"${a}(t)$")
axs[0].grid(True)
axs[0].legend()

axs[1].plot(t_values_rk2, v2, label=f'Aproximado ${b}$(t)', linestyle='--', color='red')
axs[1].set(xlabel=f'${b}$', ylabel=f'${b}(t)$')
axs[1].set_title(f'${b}(t)$')
axs[1].grid(True)
axs[1].legend()

fig_placeholder.pyplot(fig)
plt.close(fig)