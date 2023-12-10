import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.title("Método de Newton Raphson")

st.markdown("Recordemos que para hallar raices:")
st.latex(r"x_{i+1} = x_i - \frac{f(x_i)}{f'(x_i)}")
st.markdown("""Es un método abierto que parte de un valor arbitrario para llegar al óptimo,
             pero tiene la desventaja de que puede ser divergente.
Entonces para hallar óptimos: """)
st.latex(r"x_{i+1} = x_i - \frac{f'(x_i)}{f''(x_i)}")

st.image("https://1.bp.blogspot.com/-C6p0jqL9iCw/YO0MpD2D6uI/AAAAAAAAS58/5RbpYBD7FFI9rgX5IF544Ukbt0mG15kVACLcBGAsYHQ/s750/simulacion-de-procesos-metodo-newton-rapshon-explicacion-del-metodo-numerico-newton-raphson.jpg",use_column_width=True)

st.subheader("Algoritmo de Newton Raphson")
st.markdown("""1. Se haya el "siguiente" $x_{i+1}$
2. La raíz es $x_{i+1}$
3. Calcular el error.
4. Iterar hasta convergencia. """)

st.subheader("Error absoluto")
st.latex(r"er = |\frac{x_{i+1} - x_{i}}{x_{i+1}}| * 100 \%")

st.markdown(""" A continuación hallaremos el maximo de la siguiente función empleando
            el método de Newton-Raphson""")
st.latex(r"f(x) = 2*\sin(x) - \frac{x^2}{10}")
st.markdown("Con $x_i = 2.5$ y una tolerancia del $1\%$")

y = st.sidebar.text_input("Ingrese la función","2*sin(x)-((x**2)/10)")
xi = st.sidebar.number_input("Valor inicial X_i",2.5)
tol = st.sidebar.number_input("Tolerancia",1)
var_ind= st.sidebar.text_input("Variable independiente","x")

x=sp.symbols(var_ind)
yf=sp.sympify(y)

df=yf.diff()
df1=sp.lambdify(x,df)

error = tol+1
it = 1

columnas = ["xi","Xi+1","f'(xi)","f''(Xi)","Error(%)"]
tabla = pd.DataFrame(columns=columnas)

fig_placeholder= st.empty()
tablita= st.empty()

while error > tol:
  xi=float(xi)
  fxi = round(df1(xi), 4)

  plt.figure()
  fig, ax = plt.subplots()

  r = np.linspace(xi-2.0,xi+2.0, 100)
  fx = [yf.subs({x:x_i}) for x_i in r]

  ax.plot(r,fx,color='blue',label=f"${y}$")

  ax.vlines(x=0,ymin=min(fx)-1,ymax=max(fx)+1,color='k')
  ax.hlines(y=0,xmin=min(r)-1,xmax=max(r)+1,color='k')

  ax.plot([xi],[yf.subs({x:xi})], color='red', marker='o', label=f'$(x_{it},f(x_{it}))= ({xi},{yf.subs({x:xi})})$')

  df2 = df.diff()

  dfxi = round(df2.subs({x:xi}),4)

  xs = round(xi - ((fxi)/(dfxi)),4)
  ax.plot([xs],[yf.subs({x:xs})], color='red', marker='x', label=f'$(x_{it+1},0) = ({xs},{yf.subs({x:xs})})$')

  h=0.1
  dfx = (yf.subs({x:xi+h})-yf.subs({x:xi}))/h
  tan = yf.subs({x:xi})+dfx*(r-xi)
  ax.plot(r,tan,color='purple',linestyle='--',label=f"${sp.latex(df2)}$")

  ax.set_title(f"${y}$")
  ax.grid()
  ax.legend()
  

  error = np.abs((xs-xi)/(xs)) * 100

  nueva_fila = {"xi":xi,"Xi+1":xs,"f'(xi)":fxi,"f''(Xi)":dfxi,"Error(%)":round(error,4)}
  nueva_fila = pd.DataFrame([nueva_fila])
  tabla = pd.concat([tabla, nueva_fila], ignore_index=True)

  it += 1
  xi = xs

  fig_placeholder.pyplot(fig)
  tablita.dataframe(tabla)

  plt.close(fig)

st.success(f"El maximo esta en x= {round(xs,4)}")