import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.sidebar.markdown("# Newton Rapson")

# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Configuración de la página
st.title("Método Newton Rapson")

st.write('''Es el método más usado  y trabaja como referencia la pendiente ($m$) de la recta tangente en una raíz $x_i$ incial para hallar el $x_{i+1}$.

Este método tiende a acercarse muy rápido a la raíz. Pero también puede tender a la divergencia rápidamente.''')

st.image("https://www.neurochispas.com/wp-content/uploads/2022/12/Diagrama-para-provar-el-metodo-de-Newton-Raphson.png", caption='Método gráfico ', use_column_width=True)
st.write('''
$$
f'(x_i)= \\frac{f(xi)-0}{x_i - x_{i+1}}
$$
$$
f'(x_i)[x_i - x_{i+1}] = f(x_i)
$$
$$
f'(x_i)(x_i) - f'(x_i)(x_{i+1}) = f(x_i)
$$
$$
f'(x_i)(x_{i+1}) = f'(x_i)(x_i) - f(x_i)
$$

$$
x_{i+1} = x_i - \\frac{f(x_i)}{f'(x_i)} 
$$

## Algoritmo de Newton Raphson

1. Se calcula el siguiente $x_{i+1}$ con la formula.

  $$x_{i+1} = x_i - \\frac{f(x_i)}{f'(x_i)} $$

2. Se repite el paso **1** hasta convergencia.

### Error relativo
$$
e_r = \lvert \\frac{x_{i+1}-x_{i}}{x_{i+1}}\rvert
$$

### Tolerancia

Precisión que se requiere en el método!!''')
# Definir el rango de entrada
start_range = st.sidebar.slider("Inicio del rango", -20.0, 20.0, 0.1)
end_range = st.sidebar.slider("Fin del rango", -20.0, 20.0, 2.0)

# Ingresar la función
var = st.sidebar.text_input("Variable", "x")
x = sp.symbols(var)
func = st.sidebar.text_input("Función", "x**3 - x")
y = sp.sympify(func)
xi = st.sidebar.number_input("Punto inicial", 0.75)
tol= st.sidebar.number_input("Tolerancia", 0)

f= sp.lambdify(x,y)

# Tolerancia y valores iniciales
error = tol + 1
it = 1

# Dataframe para almacenar los resultados
columnas = ['xi','Xi+1','f(xi)',"f'(Xi)",'er(%)']
tabla = pd.DataFrame(columns=columnas)

# Espacio reservado para la figura
fig_placeholder = st.empty()
tablita = st.empty()

while error > tol:
    # Evaluamos la función en los puntos del intervalo
    fxi = round(y.subs({x: xi}), 4).evalf()

    # Crear la figura
    fig, ax = plt.subplots()
    r = np.linspace(start_range, end_range, 100)
    fx = calculate_y(r, y)

    ax.plot(r, fx, color='blue', label=f"${sp.latex(y)}$")
   
    ## Plano cartesiano (Ejes)
    ax.vlines(x=0, ymin=min(fx)-0.5, ymax=max(fx)+0.5, color='k')
    ax.hlines(y=0, xmin=min(r)-0.5, xmax=max(r)+0.5, color='k')
    ax.set_title(f"${sp.latex(y)}$")
    ax.grid()

    ## Punto inicial
    ax.plot([xi],[fxi], color='red', marker='o', label=f'$(x_{it},f(x_{it}))= ({xi},{fxi})$')

    ## Calculemos la derivada de la función
    dy = y.diff()
    ## Evaluemos la derivada en x_i
    dfxi = round(dy.subs({x:xi}),4)
    
    ## Calculemos el x_i+1 (siguiente)
    xs = round(xi - ((fxi)/(dfxi)),4)
    ax.plot([xs],[0], color='red', marker='x', label=f'$(x_{it+1},0) = ({xs},0)$')

    h=0.1
    #Se halla la pendiente de la recta tangente
    dfx = (y.subs({x:xi+h})-y.subs({x:xi}))/h # derivative
    tan = y.subs({x:xi})+dfx*(r-xi)  # tangent
    ax.plot(r,tan,color='purple',linestyle='--',label=f"${sp.latex(dy)}$")
    
    ax.legend()

    # Actualizamos el error y la tabla
    error = np.abs((xs-xi)/(xs)) * 100 if xi != 0 else 0
    nueva_fila = {'xi':xi,'Xi+1':xs,'f(xi)':fxi,"f'(Xi)":dfxi,'er(%)':round(error,4)}
    nueva_fila = pd.DataFrame([nueva_fila])
    tabla = pd.concat([tabla, nueva_fila], ignore_index=True)
    
    xi = xs
    it += 1

    # Mostrar la figura en el espacio reservado
    fig_placeholder.pyplot(fig)
    tablita.dataframe(tabla)
    # Borra la figura para la siguiente iteración
    plt.close(fig)