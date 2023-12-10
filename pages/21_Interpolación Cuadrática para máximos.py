import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.title("Método de la interpolación cuadrática para maximos")
st.markdown(""" Consiste en aproximar un máximo o un mínimo de cualquier curva a una 
            parabola, el óptimo de esta parabola es el aproximado de la curva de interés.""")
st.image("https://static.filadd.com/files/f%2317954/html/external_resources/bgf.png",use_column_width=True)
st.markdown("""Es un método cerrado o de intervalo que necesita inicialmente 3 puntos para
             aproximar a una única parabola, y el máximo de esa parábola es el otro punto

Para que el método funcione entre los 3 puntos debe existir un óptimo.


En la imagen anterior $x_3$ se calcula como las raices de la derivada de la parábola.""")
st.latex(r"x_3 = \frac{f(x_0)[{x_1}^2 - {x_2}^2] + f(x_1)[{x_2}^2 - {x_0}^2] + f(x_2)[{x_0}^2 - {x_1}^2]}{2f(x_0)[x_1 - x_2] + 2f(x_1)[x_2 - x_0] + 2f(x_2)[x_0 - x_1]}")

st.subheader("Algoritmo del método")
st.markdown(""" 1. Se calcula $x_3$
2. Si $x_3 ≥ x_1 \Rightarrow$ Si $f(x_3) > f(x_1) ⇒ x_0 = x_1 , x_1 = x_3$. Se recalcula $x_3$
3. Si $x_3 ≥ x_1 \Rightarrow$ Si $f(x_3) < f(x_1) ⇒ x_2 = x_3$. Se recalcula $x_3$
4. Si $x_3 < x_1 \Rightarrow$ Si $f(x_3) < f(x_1) ⇒ x_0 = x_3$. Se recalcula $x_3$
5. Si $x_3 < x_1 \Rightarrow$ Si $f(x_3) > f(x_1) ⇒ x_2 = x_1, x_1 = x_3$. Se recalcula $x_3$""")

st.subheader("Error relativo")
st.latex(r"er = |\frac{x_{3-actual} - x_{3-ant}}{x_{3-actual}}|* 100\%")

st.markdown("""A continuación, se encuentra el metódo de la interpolación cuadrática para el hallazgo de puntos maximos""")

st.subheader("\t Interpolación cuadrática para máximos")

fy = st.sidebar.text_input("Ingrese la función","2*sin(x)-((x**2)/10)")
x0 = st.sidebar.slider("Valor de X_0", -20.0, 20.0, 0.0)
x1 = st.sidebar.slider("Valor de X_1", -20.0, 20.0, 1.0)
x2 = st.sidebar.slider("Valor de X_2", -20.0, 20.0, 4.0)
tol = st.sidebar.slider("Tolerancia", -5.0, 5.0, 1.0)
var_ind= st.sidebar.text_input("Variable independiente","x")

x=sp.symbols(var_ind)
fx=sp.sympify(fy)
f=sp.lambdify(x,fx)

x3_ant=x0

error = tol + 1
it = 1

t = np.linspace(x0-0.5,x2+0.5,100)
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
  plt.show()

  error=np.abs((x3-x3_ant)/x3)*100

  data = {'x0':[x0],'x1':[x1], 'x2':[x2],'f(x0)':[fx0], 'f(x1)':[fx1], 'f(x2)':[fx2], 'x3':[x3], 'error(%)':[round(error,2)]}
  fila = pd.DataFrame(data = data)
  tabla = pd.concat([tabla,fila],ignore_index=True)

  if (x3>=x1):
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
  