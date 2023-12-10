import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.title("Método del gradiente para minimos")
st.markdown("""Funciona de igual forma que para el hallazgo de los puntos máximos, sin
            embargo cambia formula para el calculo del valor siguiente, quedando
            de la siguiente forma""")

st.latex(r"x_{i+1} = x_i - α ∇f(x)")

st.markdown("A continuación, hallaremos el mínimo de una función empleando el método del gradiente")


fy = st.sidebar.text_input("Ingrese la función","2*sin(x)-((x**2)/10)")
xi = st.sidebar.number_input("Valor inicial X_i",-0.8)
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

  xs=xi-alfa*df(xi)
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