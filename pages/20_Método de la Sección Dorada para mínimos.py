import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.title("Método de la sección dorada para minimos")
st.markdown("""Funciona de igual forma que para el hallazgo de los puntos máximos, sin
            embargo cambia la redefinición de las variables y los limites luego del 
            calculo de las variables involucradas""")

st.markdown("A continuación, hallaremos el mínimo de una función empleando el método de la sección dorada")


fy = st.sidebar.text_input("Ingrese la función","2*sin(x)-((x**2)/10)")
xl = st.sidebar.slider("Limite inferior Xl", -20.0, 20.0, -2.5)
xu = st.sidebar.slider("Limite superior Xu", -20.0, 20.0, -1.0)
tol = st.sidebar.slider("Tolerancia", -5.0, 5.0, 1.0)
var_ind= st.sidebar.text_input("Variable independiente","x")

xlo=xl
xuo=xu

x=sp.symbols(var_ind)
f=sp.sympify(fy)

R = (np.sqrt(5)-1)/2
error = tol + 1
it = 1
x0 = 0.01

t = np.linspace(xlo-0.5,xuo+0.5,100)
y = [f.subs({x:xi}) for xi in t]

columnas = ['xl', 'xu', 'x1', 'x2', 'f(x1)', 'f(x2)', 'x0', 'error(%)']
tabla = pd.DataFrame(columns=columnas)

fig_placeholder= st.empty()
tablita= st.empty()

while error>tol:
  d = R*(xu-xl)
  x1 = xl + d
  x2 = xu - d

  fx1 = round(f.subs({x:x1}),4)
  fx2 = round(f.subs({x:x2}),4)
  fx0 = round(f.subs({x:x0}),4)

  plt.figure()
  fig, ax = plt.subplots()

  ax.plot(t,y)
  ax.grid()

  ax.vlines(x=0,ymin=min(y)-0.5,ymax=max(y)+0.5,color='k')
  ax.hlines(y=0,xmin=min(t)-0.5,xmax=max(t)+0.5,color='k')

  ax.vlines(x=xl, ymin=0, ymax=f.subs({x:xl}), color='g', linestyle='--',label=f"$x_l$ = {round(xl,3)}")
  ax.vlines(x=xu, ymin=0, ymax=f.subs({x:xu}), color='b', linestyle='--',label=f"$x_u$ = {round(xu,3)}")

  ax.set_title(f"${fy}$")

  ax.vlines(x=x0, ymin=0, ymax=fx0, color='orange', linestyle='--')
  ax.vlines(x=x1, ymin=0, ymax=fx1, color='r', linestyle='--',label=f"$x_1$ = {round(x1,3)}")
  ax.vlines(x=x2, ymin=0, ymax=fx2, color='purple', linestyle='--',label=f"$x_2$ = {round(x2,3)}")

  ax.plot([x0],[fx0],'*',label=f"$x_0 = ${round(x0,3)}")

  ax.legend()
  plt.show()

  error = (1-R)*np.abs((xu-xl)/x0)*100

  data = {'xl':[xl], 'xu':[xu], 'x1':[x1], 'x2':[x2], 'f(x1)':[fx1], 'f(x2)':[fx2], 'x0':[x0], 'error(%)':[round(error,2)]}
  fila = pd.DataFrame(data = data)
  tabla = pd.concat([tabla,fila],ignore_index=True)

  if fx1 < fx2:
    xl = x2
    x2 = x1
    x0 = x1
    x1 = xl + d
  elif fx1 > fx2:
    xu = x1
    x1 = x2
    x0 = x2
    x2 = xu - d

  it+=1
  
  fig_placeholder.pyplot(fig)
  tablita.dataframe(tabla)

  plt.close(fig)

st.success(f"El mínimo esta en x= {round(x0,4)}")