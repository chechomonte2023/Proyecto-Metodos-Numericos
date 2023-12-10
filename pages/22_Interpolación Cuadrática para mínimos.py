import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.title("Interpolación cuadrática para minimos")
st.markdown("""Funciona de igual forma que para el hallazgo de los puntos máximos, sin
            embargo cambia la redefinición de las variables y los limites luego del 
            calculo de las variables involucradas""")

st.markdown("A continuación, hallaremos el mínimo de una función empleando el método de la interpolación cuadrática")


fy = st.sidebar.text_input("Ingrese la función","2*sin(x)-((x**2)/10)")
x0 = st.sidebar.slider("Valor de X_0", -20.0, 20.0, -1.0)
x1 = st.sidebar.slider("Valor de X_1", -20.0, 20.0, -3.0)
x2 = st.sidebar.slider("Valor de X_2", -20.0, 20.0, -4.0)
tol = st.sidebar.slider("Tolerancia", -5.0, 5.0, 1.0)
var_ind= st.sidebar.text_input("Variable independiente","x")

x=sp.symbols(var_ind)
fx=sp.sympify(fy)
f=sp.lambdify(x,fx)

x3_ant=x0

error = tol + 1
it = 1

t = np.linspace(x2-0.5,x0+0.5,100)
y = f(t)

columnas = ['x0','x1', 'x2', 'f(x0)','f(x1)', 'f(x2)', 'x3', 'error(%)']
tabla = pd.DataFrame(columns=columnas)

fig_placeholder= st.empty()
tablita= st.empty()

while(error>tol):

  fx0=round(f(x0),4)
  fx1=round(f(x1),4)
  fx2=round(f(x2),4)

  x3=(fx0*(x1**2-x2**2)+fx1*(x2**2-x0**2)+fx2*(x0**2-x1**2))/(2*fx0*(x1-x2)+2*f(x1)*(x2-x0)+2*f(x2)*(x0-x1))

  plt.figure()
  fig, ax = plt.subplots()

  ax.plot(t,y)
  ax.grid()

  ax.vlines(x=0,ymin=min(y)-0.5,ymax=max(y)+0.5,color='k')
  ax.hlines(y=0,xmin=min(t)-0.5,xmax=max(t)+0.5,color='k')

  ax.set_title(f"${fy}$")

  fx3=round(f(x3),4)

  ax.vlines(x=x0, ymin=0, ymax=fx0, color='orange', linestyle='--',label=f"$x_0$ = {round(x0,3)}")
  ax.vlines(x=x1, ymin=0, ymax=fx1, color='red', linestyle='--',label=f"$x_1$ = {round(x1,3)}")
  ax.vlines(x=x2, ymin=0, ymax=fx2, color='purple', linestyle='--',label=f"$x_2$ = {round(x2,3)}")
  ax.vlines(x=x3, ymin=0, ymax=fx3, color='green', linestyle='--')

  ax.plot([x3],[fx3],'*',label=f"$x_3 = ${round(x3,3)}")

  ax.legend()
  
  error=np.abs((x3-x3_ant)/x3)*100

  data = {'x0':[x0],'x1':[x1], 'x2':[x2],'f(x0)':[fx0], 'f(x1)':[fx1], 'f(x2)':[fx2], 'x3':[x3], 'error(%)':[round(error,2)]}
  fila = pd.DataFrame(data = data)
  tabla = pd.concat([tabla,fila],ignore_index=True)

  if (x3<x1):
    if(f(x3)>f(x1)):
      x0=x1
      x1=x3
    else:
      x2=x3
  else:
    if(f(x3)<f(x1)):
      x0=x3
    else:
      x2=x1
      x1=x3

  x3_ant=x3

  it+=1

  fig_placeholder.pyplot(fig)
  tablita.dataframe(tabla)

  plt.close(fig)

st.success(f"El maximo esta en x= {round(x3,4)}")
  