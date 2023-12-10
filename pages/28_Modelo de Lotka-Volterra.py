import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.title("Modelo de Lotka Volterra")
st.markdown("""El modelo Lotka-Volterra es un par de ecuaciones diferenciales utilizadas 
            para describir las dinámicas de interacción entre dos especies en un ecosistema.
             Este modelo lleva el nombre de los matemáticos Alfred Lotka y Vito Volterra, 
            quienes independientemente desarrollaron las ecuaciones en la década de 1920.

El modelo básico describe la interacción entre una presa y un depredador y se expresa 
            mediante las siguientes ecuaciones: """)
st.subheader("Ecuación de la presa (presas o presa)")
st.latex(r"\frac{dx}{dt}={αx-βxy}")
st.markdown(""" Donde:
*   x es la población de la presa
*   α es la tasa de crecimiento natural de la presa en ausencia de depredadores.
*   β es la tasa de depredación de la presa por el depredador.
*   y es la población del depredador.""")

st.subheader("Ecuación del depredador (depredadores o depredador)")
st.latex(r"\frac{dy}{dt}={δxy-γy}")
st.markdown("""Donde:

*   y es la población del depredador.
*   δ es la tasa de crecimiento natural del depredador.
*   γ es la tasa de mortalidad del depredador en ausencia de presas.
*   x es la población de la presa.""")

st.markdown("""Estas ecuaciones describen cómo cambian las poblaciones de presas y 
            depredadores con el tiempo, asumiendo ciertas tasas de crecimiento y 
            depredación. El modelo Lotka-Volterra sugiere un equilibrio en el que 
            las poblaciones de presas y depredadores fluctúan de manera periódica, 
            creando ciclos en el tiempo.

Tomaremos el siguiente ejemplo:

Tomaremos como nuestra población de depredadores un grupo de zorros y como presas un grupo de conejos.

Diremos que: 
* α=0.1: Tasa de crecimiento natural de los conejos.
* β=0.02: Tasa de depredación de los conejos por los zorros.
* δ=0.01: Tasa de crecimiento natural de los zorros.
* γ=0.1: Tasa de mortalidad de los zorros en ausencia de conejos.""")


var_1 = st.sidebar.text_input("Variable dependiente 1 ","x")
var_2 = st.sidebar.text_input("Variable dependiente 2 ","y")
func_1 = st.sidebar.text_input("Función 1 ","0.1*x - 0.02*x*y")
func_2 = st.sidebar.text_input("Función 2 ","0.01*x*y - 0.1*y")
t0 = st.sidebar.number_input("Tiempo inicial t0",0)
tf = st.sidebar.number_input("Tiempo final tf",100)
dt = st.sidebar.number_input("Paso del tiempo dt",0.1)
initial_var_1=st.sidebar.number_input("Valor inicial de la variable 1",100)
initial_var_2=st.sidebar.number_input("Valor inicial de la variable 2",20)

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
axs[0].set(xlabel="Tiempo")
axs[0].set(ylabel=f'${a}(t)$')
axs[0].set_title(f"${a}(t)$")
axs[0].grid(True)
axs[0].legend()

axs[1].plot(t_values_rk2, v2, label=f'Aproximado ${b}$(t)', linestyle='--', color='red')
axs[1].set(xlabel="Tiempo", ylabel=f'${b}(t)$')
axs[1].set_title(f'${b}(t)$')
axs[1].grid(True)
axs[1].legend()

fig_placeholder.pyplot(fig)