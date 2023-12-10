import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.header("Metodo de Euler para  ecuaciones diferenciales")
st.markdown("""El método de Euler es un procedimiento numérico simple para resolver ecuaciones
             diferenciales ordinarias (EDOs) con un valor inicial dado. Es un método 
            iterativo que comienza en un punto conocido y avanza paso a paso hasta llegar 
            al punto deseado, utilizando la pendiente de la solución (es decir, la derivada)
             para avanzar en cada paso.
             En este capítulo se enfoca la solución de ecuaciones diferenciales 
            ordinarias de la forma:""")
st.latex(r"\frac{dy}{dx} = f(x,y)")
st.markdown("En términos matemáticos calculabamos el siguiente de la forma:")
st.latex(r"y_{i+1} = y_i + mh")
st.markdown("""Donde m es la pendiente estimada que se usa para extrapolar desde un valor 
            anterior $y_i$ a un nuevo valor $y_{i+1}$ en una distancia $h$. Este valor se
             usa paso a paso para calcular un valor posterior y trazar la trayectoria de 
            la solución. Normalmente, la pendiente representa la derivada de la función en
             el punto $y_i$ """)
st.image("https://github.com/BioAITeamLearning/Metodos_2023_03_UAM/blob/main/_static/images/Euler.png?raw=true",use_column_width=True)
st.image("https://github.com/BioAITeamLearning/Metodos_2023_03_UAM/blob/main/_static/images/Euler2.png?raw=true",use_column_width=True)

st.subheader("Algoritmo de Euler para la integración")
st.markdown("""1. Hacer $y_{i+1} = y_i + hf'(x_i,y_i)$
2. Hacer $x_{i} = x_{i+1}$""")

st.markdown("""A continuación, emplearemos el método de euler para la solución del
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

def euler_method_system(funcs, y0, t0, tf, dt):
    t_values = np.arange(t0, tf, dt)
    y_values = [np.array(y0)]

    for t in t_values[:-1]:
        y_current = y_values[-1]
        y_next = y_current + dt * np.array([f(*y_current, t) for f in funcs])
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
t_values_euler, [v1, v2] = euler_method_system(
    [func_a, func_b], initial_conditions, t0, tf, dt
)

fig, axs = plt.subplots(1,2,figsize=(20,6))

axs[0].plot(t_values_euler, v1, label=f'Aproximado ${a}$(t)', linestyle='--')
axs[0].set(xlabel=f"${a}$")
axs[0].set(ylabel=f'${a}(t)$')
axs[0].set_title(f"${a}(t)$")
axs[0].grid(True)
axs[0].legend()

axs[1].plot(t_values_euler, v2, label=f'Aproximado ${b}$(t)', linestyle='--', color='red')
axs[1].set(xlabel=f'${b}$', ylabel=f'${b}(t)$')
axs[1].set_title(f'${b}(t)$')
axs[1].grid(True)
axs[1].legend()

fig_placeholder.pyplot(fig)