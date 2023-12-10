import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.header("Método de Runge Kutta de Orden 4")
st.markdown("""El más popular de los métodos RK es el de cuarto orden. Para este modelo
            existen una infinidad de versiones, sin embargo, emplearemos la más utilizada
            en el mundo matemático. La siguiente, es la forma de uso más común y, por tanto,
            se le conoce como $método RK clásico de cuarto orden$ """)

st.markdown("La fórmula para calcular el siguiente queda:")
st.latex(r"y_{i+1} = y_i + \frac{1}{6}(k_1 + 2k_2 + 2k_3 + k_4)h")
st.markdown("Donde: ")
st.latex(r"k_1 = f(x_i,y_i)")
st.latex(r"k_2 = f(x_i+\frac{1}{2}h, y_i +\frac{1}{2}k_1h)")
st.latex(r"k_3 = f(x_i+\frac{1}{2}h, y_i +\frac{1}{2}k_2h)")
st.latex(r"k_4 = f(x_i+h, y_i + k_3h)")

st.markdown("""A continuación, emplearemos el método de Runge-Kutta de orden 4 para la solución del
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

def runge_kutta_4(funcs, y0, t0, tf, dt):
    t_values = np.arange(t0, tf, dt)
    y_values = [np.array(y0)]

    for t in t_values[:-1]:
        y_current = y_values[-1]
        k1 = np.array([f(*y_current, t) for f in funcs])
        k2 = np.array([f(*(y_current + 0.5 * k1 * dt), t + 0.5 * dt) for f in funcs])
        k3 = np.array([f(*(y_current + 0.5 * k2 * dt), t + 0.5 * dt) for f in funcs])
        k4 = np.array([f(*(y_current + k3 * dt), t + dt) for f in funcs])

        y_next = y_current + (1/6) * dt * (k1 + 2 * k2 + 2 * k3 + k4)
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
t_values_rk4, [v1, v2] = runge_kutta_4(
    [func_a, func_b], initial_conditions, t0, tf, dt
)

fig, axs = plt.subplots(1,2,figsize=(20,6))

axs[0].plot(t_values_rk4, v1, label=f'Aproximado ${a}$(t)', linestyle='--')
axs[0].set(xlabel=f"${a}$")
axs[0].set(ylabel=f'${a}(t)$')
axs[0].set_title(f"${a}(t)$")
axs[0].grid(True)
axs[0].legend()

axs[1].plot(t_values_rk4, v2, label=f'Aproximado ${b}$(t)', linestyle='--', color='red')
axs[1].set(xlabel=f'${b}$', ylabel=f'${b}(t)$')
axs[1].set_title(f'${b}(t)$')
axs[1].grid(True)
axs[1].legend()

fig_placeholder.pyplot(fig)
plt.close(fig)