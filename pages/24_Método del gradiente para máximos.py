import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.title("Método del gradiente")
st.markdown("""El método de descenso del gradiente es una técnica de optimización iterativa
             utilizada para encontrar el mínimo local de una función diferenciable. Es 
            especialmente útil para funciones que tienen muchos mínimos locales y globales.
             Su popularidad ha crecido en las últimas décadas debido a su eficacia en el
             entrenamiento de modelos de aprendizaje automático, especialmente redes 
            neuronales. """)
st.image("https://www.codificandobits.com/img/posts/2018-07-02/concepto-de-gradiente.png",use_column_width=True)
st.image("https://aimlsite.files.wordpress.com/2018/03/gradient-descent.png",use_column_width=True)

st.subheader("Algoritmo de la gradiente descendiente")
st.markdown("""La idea básica detrás del método es simple: dada una función objetivo
$f(x)$, queremos encontrar el valor de $x$ que minimiza $f$. Para hacerlo, comenzamos en un
             punto inicial y seguimos los pasos en la dirección que decrece el valor de 
            $f$ más rápidamente, es decir, en la dirección del gradiente negativo. 
            La formula para el cálculo del valor siguiente es """)
st.latex(r"x_{i+1} = x_i + α ∇f(x)")

st.markdown("Acá $α$ es el **factor de sensibilidad** o **Tasa de aprendizaje**")
st.markdown("""Un aspecto crucial del método es la elección de la **"tasa de aprendizaje"**,
             que determina cuán grandes son los pasos que tomamos en cada iteración. Una 
            tasa de aprendizaje demasiado grande puede hacer que el método oscile o 
            incluso diverja, mientras que una tasa demasiado pequeña puede hacer que el 
            método converja muy lentamente. """)
st.markdown("El error del método de puede calcular de varias formas")
st.image("https://koldopina.com/wp-content/uploads/2018/05/gd_tasa_aprendizaje.jpg",use_column_width=True)
st.latex(r"er = |\frac{x_{i+1} - x_i}{x_{i+1}}| * 100\%")
st.latex(r"|x_{i+1}-x_i| ≈ 0")
st.latex(r"|∇f(x_i)| ≈ 0")
st.markdown("""Como este método es divergente se debe agregar una condición de parada. Si 
            no se alcanza convergencia el método no va a parar, entonces se debe agregar 
            otro parámetro, el **max_iterations** que si no se alcanza convergencia entonces
             cuando se llegue al **máximo de iteraciones** se frena el algoritmo. """)

st.markdown("A continuación, hallaremos el máximo de una función empleando el método del gradiente")

fy = st.sidebar.text_input("Ingrese la función","2*sin(x)-((x**2)/10)")
xi = st.sidebar.number_input("Valor inicial X_i",1)
alfa = st.sidebar.slider("Tasa de aprendizaje",-5.0, 5.0, 0.1)
tol = st.sidebar.slider("Tolerancia", -5.0, 5.0, 0.1)
max_iterations = st.sidebar.number_input("Máximo de iteraciones",1000)
var_ind= st.sidebar.text_input("Variable independiente","x")

x=sp.symbols(var_ind)
fx=sp.sympify(fy)

d=sp.diff(fx)

f=sp.lambdify(x,fx)
df=sp.lambdify(x,d)


error = tol + 1
it = 1

t = np.linspace(xi-1.5,xi+1.5,100)
y = [fx.subs({x:xi}) for xi in t]

columnas = ['xi', 'xi+1', 'f(xi)', 'f(xi+1)','error(%)']
tabla = pd.DataFrame(columns=columnas)

fig_placeholder= st.empty()
tablita= st.empty()

while (error>tol and it<max_iterations):
  
  
  fig, ax= plt.subplots()

  fxi=round(f(xi),4)

  xs=xi+alfa*df(xi)
  fxs=round(f(xs),4)

  ax.plot(t,y)
  ax.grid()

  ax.vlines(x=0,ymin=min(y)-0.5,ymax=max(y)+0.5,color='k')
  ax.hlines(y=0,xmin=min(t)-0.5,xmax=max(t)+0.5,color='k')

  ax.set_title(f"${fy}$")

  ax.scatter(xs,fxs,c="red")

  error=np.abs((xs-xi)/xs)*100

  data = {'xi':[xi], 'xi+1':[xs], 'f(xi)':[fxi], 'f(xi+1)':[fxs],'error(%)':[round(error,2)]}
  fila = pd.DataFrame(data = data)
  tabla = pd.concat([tabla,fila],ignore_index=True)

  xi=xs
  it+=1

ax.scatter(xs,fxs,c="green",label=f"$x_s = ${round(xs,3)}")
ax.legend()
tabla.head(max_iterations) 

fig_placeholder.pyplot(fig)
tablita.dataframe(tabla)

plt.close(fig)

st.success(f"El maximo esta en x= {round(xs,4)}")