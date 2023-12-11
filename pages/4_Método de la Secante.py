import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.sidebar.markdown("# Secante")

# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Configuración de la página
st.title("Método De la Secante")
st.write('''Este método es muy parecido a Newton Raphson,pero con la diferencia que no necesita evaluar en la derivada. Hay problemas en los que la derivada es dificil de calcular, el método de la secante permite resolver el problema ya que aproxima la raíz mediante rectas secantes.
''')
st.image("data:image/png;base64,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", caption='Método gráfico ', use_column_width=True)
st.write('''## Demostración del método

$$
f'(x) = \\frac{f(x_i)-f(x_{i-1})}{x_i - x_{i-1}}
$$

### Recordemos de newton Raphson

$$
x_{i+1} = x_i - \\frac{f(x_i)}{f'(x_i)} 
$$

Reemplacemos la aproximación de la derivada por la secante en la de newton raphson

$$
x_{i+1} = x_i - \\frac{f(x_i)}{\\frac{f(x_i)-f(x_{i-1})}{x_i - x_{i-1}}}
$$

despejando tenemos

$$
x_{i+1} = x_i - \\frac{f(x_i)[x_i - x_{i-1}]}{f(x_i)-f(x_{i-1})}
$$

## Algoritmo de la secante
1. Se calcula el siguiente $x_{i+1}$ con la formula.

  $$
  x_{i+1} = x_i - \\frac{f(x_i)[x_i - x_{i-1}]}{f(x_i)-f(x_{i-1})}
  $$

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
func = st.sidebar.text_input("Función", "exp(-x)-x")
y = sp.sympify(func)
xi_ant = st.sidebar.number_input("Valor anterior", 0)
xi= st.sidebar.number_input("Valor inicial", 1)
tol= st.sidebar.number_input("Tolerancia", 0.1)
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
    fxi=round(f(xi), 4)
    fxa=round(f(xi_ant),4)
        
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
    ax.plot([xi],[fxi], color='red', marker='o', label=f'$(x_{it},f(x_{it}))= ({xi},{fxi})$')
    ax.plot([xi_ant],[fxa], color='red', marker='o', label=f'$(x_{it},f(x_{it}))= ({xi_ant},{fxa})$')

    ## Calculemos el x_i+1 (siguiente)
    xs = round(xi - ((fxi*(xi-xi_ant))/(fxi-fxa)),4)
    ax.plot([xs],[0], color='green', marker='x', label=f'$(x_{it+1},0) = ({xs},0)$')

    # Pintar la recta secante
    ax.plot([xi_ant,xi],[fxa,fxi],color='purple',linestyle='--')
    ax.vlines(x=xi_ant,ymin=0,ymax=fxa,linestyle="--",color="black")
    ax.vlines(x=xi,ymin=0,ymax=fxi,linestyle="--",color="black")

     ## Calculo del error
    error = np.abs((xs-xi)/(xs)) * 100
        
    ax.legend()
    plt.show()
    ## Actualicemos la tabla de iteraciones
    nueva_fila = {'Xi-1':xi_ant,'xi':xi,'Xi+1':xs,'f(Xi-1)':fxa,'f(Xi)':fxi,'Error(%)':round(error,4)}
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