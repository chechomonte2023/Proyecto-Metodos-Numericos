import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.title("Métodos cerrados de optimización")
st.subheader("Método de la sección dorada para máximos")

st.markdown("""Es similar al método de la bisección porque necesita un $x_l$ y $x_u$. 
            Para hallar la posición de los puntos $x_1$ y $x_2$, se usa la sección dorada. 
            El objetivo de usar la sección dorada, es ahorrar costos computacionales porque
             con ella se logra hacer la menor cantidad de operaciones. Es decir, con la 
            sección dorada, no se calcula el máximo ni el mínimo sino la posición de $x_1$ 
            y $x_2$.""")
st.image("https://4.bp.blogspot.com/-gP4CPYOaIFI/WnsjXu2rk3I/AAAAAAAABJ8/Hd6Ya44v6sob5EAEKJKAa-d-kq5c45SAQCLcBGAs/s1600/3.png",use_column_width=True)

st.latex(r"l_0 = l_1 + l_2")
st.latex(r"\frac{l_1}{l_0} = \frac{l_2}{l_1}")
st.latex(r"\frac{l_1}{l_1 + l_2} = \frac{l_2}{l_1}")
st.latex(r"\frac{l_1}{l_2} = \frac{l_1 + l_2}{l_1}")
st.latex(r"\frac{l_1}{l_2} = 1+ \frac{l_2}{l_1}")
st.markdown(r"Hacemos $R = \frac{l_2}{l_1}$")

st.latex(r"\frac{1}{R} = 1 + R")
st.latex(r"1 = R (1 + R)")
st.latex(r"1 = R + R^2")
st.latex(r"0 = -1 + R + R^2")
st.markdown("Resolvemos por formula cuadrática y tomamos solo el positivo")
st.latex(r"R = \frac{\sqrt{5}-1}{2}")
st.latex(r"R = 0.61803")

st.image("https://static.filadd.com/files/f%2317954/html/external_resources/bg9.png",use_column_width=True)
st.subheader("Algoritmo de la sección dorada")
st.markdown("A) calcular d como:")
st.latex(r"d = R(x_u - x_l)")
st.markdown("B) Calculamos $x_1$ y $x_2$ con la formula:")
st.latex(r"x_1 = x_l + d")
st.latex(r"x_2 = x_u - d")
st.markdown("Siempre $x_1 > x_2$ por la sección dorada.")
st.markdown("""C)1 . Si $f(x_1) > f(x_2)$, el máximo está entre $x_2$ y $x_u$. Entonces,
             $x_l = x_2$, $x_2 = x_1$, $x_0 = x_1$ y se recalcula $x_1 = x_l + d$""")
st.markdown("""2. Si $f(x_1) < f(x_2)$, el máximo está entre $x_l$ y $x_1$. Entonces, 
            $x_u = x_1$, $x_1 = x_2$, $x_0 = x_2$ y se recalcula $x_2 = x_u - d$""")
st.markdown("D) Repetir hasta convergencia")

st.subheader("Error relativo")
st.latex(r"e_r = (1-R)*|\frac{x_u - x_l}{x_{0}}| * 100\%")

st.markdown("""A continuación, se encuentra el metódo de la sección dorada para el hallazgo de puntos maximos""")

st.subheader("\t Método de la sección dorada para maximos")

fya = st.sidebar.text_input("Ingrese la función","2*sin(x)-((x**2)/10)")
xla = st.sidebar.slider("Limite inferior Xl", -20.0, 20.0, 0.0)
xua = st.sidebar.slider("Limite superior Xu", -20.0, 20.0, 4.0)
tola = st.sidebar.slider("Tolerancia", -5.0, 5.0, 1.0)
var_inda= st.sidebar.text_input("Variable independiente","x")

xloa=xla
xuoa=xua

x=sp.symbols(var_inda)
fa=sp.sympify(fya)

Ra = (np.sqrt(5)-1)/2
errora = tola + 1
ita = 1
x0a = 0.01

ta = np.linspace(xloa-0.5,xuoa+0.5,100)
ya = [fa.subs({x:xi}) for xi in ta]

columnasa = ['xl', 'xu', 'x1', 'x2', 'f(x1)', 'f(x2)', 'x0', 'error(%)']
tablaa = pd.DataFrame(columns=columnasa)

fig_placeholder= st.empty()
tablita= st.empty()

while errora>tola:
  da = Ra*(xua-xla)
  x1a = xla + da
  x2a = xua - da

  fx1a = round(fa.subs({x:x1a}),4)
  fx2a = round(fa.subs({x:x2a}),4)
  fx0a = round(fa.subs({x:x0a}),4)

  plt.figure()
  figa, ax = plt.subplots()

  ax.plot(ta,ya)
  ax.grid()

  ax.vlines(x=0,ymin=min(ya)-0.5,ymax=max(ya)+0.5,color='k')
  ax.hlines(y=0,xmin=min(ta)-0.5,xmax=max(ta)+0.5,color='k')

  ax.vlines(x=xla, ymin=0, ymax=fa.subs({x:xla}), color='g', linestyle='--',label=f"$x_l$ = {round(xla,3)}")
  ax.vlines(x=xua, ymin=0, ymax=fa.subs({x:xua}), color='b', linestyle='--',label=f"$x_u$ = {round(xua,3)}")

  ax.set_title(f"${fya}$")

  ax.vlines(x=x0a, ymin=0, ymax=fx0a, color='orange', linestyle='--')
  ax.vlines(x=x1a, ymin=0, ymax=fx1a, color='r', linestyle='--',label=f"$x_1$ = {round(x1a,3)}")
  ax.vlines(x=x2a, ymin=0, ymax=fx2a, color='purple', linestyle='--',label=f"$x_2$ = {round(x2a,3)}")

  ax.plot([x0a],[fx0a],'*',label=f"$x_0 = ${round(x0a,3)}")

  ax.legend()

  errora = (1-Ra)*np.abs((xua-xla)/x0a)*100

  dataa = {'xl':[xla], 'xu':[xua], 'x1':[x1a], 'x2':[x2a], 'f(x1)':[fx1a], 'f(x2)':[fx2a], 'x0':[x0a], 'error(%)':[round(errora,2)]}
  filaa = pd.DataFrame(data = dataa)
  tablaa = pd.concat([tablaa,filaa],ignore_index=True)

  if fx1a > fx2a:
    xla = x2a
    x2a = x1a
    x0a = x1a
    x1a = xla + da
  elif fx1a < fx2a:
    xua = x1a
    x1a = x2a
    x0a = x2a
    x2a = xua - da

  ita+=1
  
  fig_placeholder.pyplot(figa)
  tablita.dataframe(tablaa)

  plt.close(figa)

st.success(f"El maximo esta en x= {round(x0a,4)}")
