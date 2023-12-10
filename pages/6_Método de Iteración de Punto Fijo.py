import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.sidebar.markdown("# Iteración Punto Fijo")

# Configuración de la página
st.title("Método Iteración Punto Fijo")
st.write('''Los métodos abiertos emplean una fórmula que predice la raíz. Tal fórmula puede ser desarrollada para una *simple iteración de punto fijo* (o también llamada iteración de un punto o sustitución sucesiva) al rearreglar la ecuación $f(x)=0$ de tal modo que $x$ quede al lado izquierdo de la ecuación:



$$
x=g(x)
$$

La utilidad de esta ecuación es que proporciona una fórmula para predecir un nuevo valor de $x$ en función del valor anterior de $x$. De esta manera, dado un valor de inicio a la raíz $x_{i}$, la ecuación se puede usar para obtener una nueva aproximación $x_{i+1}$, expresada por la fórmula iterativa

$$
x_{i+1}=g(x_{i})
$$
''')
st.image("https://4.bp.blogspot.com/-OgzdiC_H1X4/VHt0vGkWCSI/AAAAAAAAAC4/mI3t1igbqhk/s1600/Met%2BPunto%2BFijo.jpg", caption='Método gráfico ', use_column_width=True)
st.write('''
Esta imagen es un esquema gráfico de la convergencia a) y v) y la divergencia c) y d) de la iteración de punto fijo simple. A las gráficas a) y c) se les conoce como patrones monófonos, mientras que b) y d) son llamados patrones oscilatorios o en espiral. Es importante saber que la convergecnia se obiente cuando:
$$
|g´(x)|<1
$$

## Algoritmo de la iteración de punto fijo
1. Expresar la ecuación original en la forma $f(x) = 0$
2. Reescribir la ecuación en la forma 
$
x = g(x)
$ 
al despejar x de la ecuación 
$
(x = f(x) + x)
$
3. Elija una estimación inicial para la solución, $x_{0}$
4. Aplique repetidamente la función $g(x)$ a la estimación inicial para obtener una secuencia de valores: $x_{1} = g(x_{0}), x_{2} = g(x_{1}), x_{3} = g(x_{2})$, y así sucesivamente.
5. Repita el paso 4 hasta que la secuencia de valores converja a una solución, es decir, hasta que $x_{k} ≈ x_{k+1}$ para algún valor de $k$.
### Error relativo
$$
e_r = \lvert \\frac{x_{i+1}-x_{i}}{x_{i+1}}\rvert
$$

### Tolerancia

Precisión que se requiere en el método!!''')
yf = st.sidebar.text_input("Ingrese la función","exp(-x)-x")
xi = st.sidebar.number_input("Valor inicial X_i",0)
tol = st.sidebar.number_input("Tolerancia",1)
var_ind= st.sidebar.text_input("Variable independiente","x")

x=sp.symbols(var_ind)
y=sp.sympify(yf)

s=sp.expand(y+x)

columnas = ['xi','Xi+1','f(xi)','er(%)']
tabla = pd.DataFrame(columns=columnas)

tol = 1

er = tol+1
it = 1

fig_placeholder= st.empty()
tablita= st.empty()

while er > tol:
  fxi = round(y.subs({x: xi}), 4)

  ##################
  plt.figure()
  fig, ax = plt.subplots()

  r = np.linspace(-0.5,1.5, 100)
  fx = [y.subs({x:x_i}) for x_i in r]

  ax.plot(r,fx,color='blue',label="$e^{-x} - x$")

  ## Plano cartesiano (Ejes)
  ax.vlines(x=0,ymin=min(fx)-0.1,ymax=max(fx)+0.1,color='k')
  ax.hlines(y=0,xmin=min(r)-0.1,xmax=max(r)+0.1,color='k')

  ## Punto inicial

  ax.plot([xi],[fxi], color='red', marker='o', label=f'$(x_{it},f(x_{it}))= ({xi},{fxi})$')

  ## Calculemos el x_i+1 (siguiente)
  xs = round(s.subs({x: xi}), 4)
  ax.plot([xs],[0], color='red', marker='x', label=f'$(x_{it+1},0) = ({xs},0)$')


  ax.set_title("$e^{-x} - x$")
  ax.grid()
  ax.legend()

  ## Calculo del error
  er = np.abs((xs-xi)/(xs)) * 100

  ## Actualicemos la tabla de iteraciones
  nueva_fila = {'xi':xi,'Xi+1':xs,'f(xi)':fxi,'er(%)':round(er,4)}
  nueva_fila = pd.DataFrame([nueva_fila])
  tabla = pd.concat([tabla, nueva_fila], ignore_index=True)

  #Actualizamos la iteración y el valor de x actual (xi)
  it += 1
  xi = xs

  fig_placeholder.pyplot(fig)
  tablita.dataframe(tabla)

  plt.close(fig)