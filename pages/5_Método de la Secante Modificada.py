import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.sidebar.markdown("# Secante modificada")

# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Configuración de la página
st.title("Método de la Secante Modificada")
st.write('''El método de la secante tiene una variación, llamada la secante modificada. Esta versión NO usa dos valores, sino un $Δ$ muy pequeño para estimar la derivada.''')
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Derivative.svg/250px-Derivative.svg.png",width=300, caption='Método gráfico ',use_column_width=False)
st.write('''
$$
f'(x) = \\frac{f(x_i+Δx_i)-f(x_{i})}{Δx_i}
$$
## Demostración del método

$$
f'(x) = \\frac{f(x_i+Δx_i)-f(x_{i})}{Δx_i}
$$

## Recordemos de newton Raphson

$$
x_{i+1} = x_i - \\frac{f(x_i)}{f'(x_i)} 
$$

Reemplacemos la aproximación de la derivada por la secante modificada en la de newton raphson

$$
x_{i+1} = x_i - \\frac{f(x_i)}{\\frac{f(x_i+Δx_i)-f(x_{i})}{Δx_i}}
$$

despejando tenemos

$$
x_{i+1} = x_i - \\frac{f(x_i)Δx_i}{f(x_i+Δx_i)-f(x_{i})}
$$

## Algoritmo de la secante modificada
1. Se calcula el siguiente $x_{i+1}$ con la formula.

 $$
 x_{i+1} = x_i - \\frac{f(x_i)Δx_i}{f(x_i+Δx_i)-f(x_{i})}
 $$

2. Se repite el paso **1** hasta convergencia.

### Error relativo
$$
e_r = \lvert \\frac{x_{i+1}-x_{i}}{x_{i+1}}\rvert
$$

### Tolerancia

Precisión que se requiere en el método''')
# Definir el rango de entrada
start_range = st.sidebar.slider("Inicio del rango", -20.0, 20.0, 0.1)
end_range = st.sidebar.slider("Fin del rango", -20.0, 20.0, 2.0)

# Ingresar la función
var = st.sidebar.text_input("Variable", "x")
x = sp.symbols(var)
func = st.sidebar.text_input("Función", "exp(-x)-x")
y = sp.sympify(func)
delta = st.sidebar.number_input("Valor delta", 1)
xi_ant = st.sidebar.number_input("Valor anterior", 0)
xi= st.sidebar.number_input("Valor inicial", 0)
tol= st.sidebar.number_input("Tolerancia", 1)
f= sp.lambdify(x,y)

# Tolerancia y valores iniciales
error = tol + 1
it = 1

# Dataframe para almacenar los resultados
columnas = ['Xi-1','xi','Xi+1','f(Xi-1)',"f(Xi)",'Error(%)']
tabla = pd.DataFrame(columns=columnas)

# Espacio reservado para la figura
fig_placeholder = st.empty()
tablita = st.empty()

while error > tol:
    # Evaluamos la función en los puntos del intervalo
    fxi=round(f(xi+delta), 4)
    fxa=round(f(xi),4)
        
    # Crear la figura
    plt.figure()
    fig, ax = plt.subplots()
    
    r = np.linspace(start_range, end_range, 100)
    fx = calculate_y(r, y)

    ax.plot(r, fx, color='blue', label=f"${sp.latex(y)}$")
   
    ## Plano cartesiano (Ejes)
    ax.vlines(x=0, ymin=min(fx)-1, ymax=max(fx)+1, color='k')
    ax.hlines(y=0, xmin=min(r)-1, xmax=max(r)+1, color='k')
    ax.set_title(f"${sp.latex(y)}$")
    ax.grid()

    ## Punto inicial
    ax.plot([xi+delta],[fxi], color='red', marker='o', label=f'$(x_{it},f(x_{it}))= ({xi+delta},{fxi})$')
    ax.plot([xi],[fxa], color='red', marker='o', label=f'$(x_{it},f(x_{it}))= ({xi},{fxa})$')

    ## Calculemos el x_i+1 (siguiente)
    xs = round(xi - ((fxi*(xi-delta))/(fxi-fxa)),4)
    ax.plot([xs],[0], color='green', marker='x', label=f'$(x_{it+1},0) = ({xs},0)$')

    # Pintar la recta secante
    ax.plot([xi,xi+delta],[fxa,fxi],color='purple',linestyle='--')
    ax.vlines(x=xi_ant,ymin=0,ymax=fxa,linestyle="--",color="black")
    ax.vlines(x=xi,ymin=0,ymax=fxi,linestyle="--",color="black")
    
    ## Calculo del error
    error = np.abs((xs-xi)/(xs)) * 100
        
    ax.legend()
    plt.show()
    ## Actualicemos la tabla de iteraciones
    nueva_fila = {'Xi-1':xi,'xi':xi+delta,'Xi+1':xs,'f(Xi-1)':fxa,'f(Xi)':fxi,'Error(%)':round(error,4)}
    nueva_fila = pd.DataFrame([nueva_fila])
    tabla = pd.concat([tabla, nueva_fila], ignore_index=True)

    if error==0:
        break
    it += 1
    xi_ant=xi
    xi = xs

    # Mostrar la figura en el espacio reservado
    fig_placeholder.pyplot(fig)
    tablita.dataframe(tabla)
    # Borra la figura para la siguiente iteración
    plt.close(fig)