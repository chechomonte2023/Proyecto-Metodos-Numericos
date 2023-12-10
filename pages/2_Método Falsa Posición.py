import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.sidebar.markdown("# Falsa Posición")

# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Configuración de la página
st.title("Método Falsa Posición")

st.write('''Consiste en hallar una raíz aproximada de una función en un intervalo dado, en algunos casos más eficiente que la **bisección**.

Toma en cuenta la magnitud de la función. Crea una linea recta entre los **2** puntos y la raíz de la recta se aproxima a la raíz de la función a diferencia de la bisección que parte en 2 lados iguales.
''')
st.image("https://docplayer.es/docs-images/87/95843293/images/35-0.jpg", caption='', use_column_width=True)

st.write('''
## Teorema de la semejanza

$$
\\frac{f(x_l)}{x_r - x_l} = \\frac{-f(x_u)}{x_r-x_u}
$$


$$
\\frac{f(x_l)}{x_r - x_l} = \\frac{f(x_u)}{x_u-x_r}
$$


$$
f(x_l)[x_r - x_u] = f(x_u)[x_r - x_l]
$$

$$
f(x_l)*x_r - f(x_l)*x_u = f(x_u)*x_r - f(x_u)*x_l
$$

$$
f(x_l)*x_r - f(x_u)*x_r = f(x_l)*x_u - f(x_u)*x_l
$$

$$
x_r = \\frac{f(x_l)*x_u - f(x_u)*x_l}{f(x_l)-f(x_u)}
$$

### Forma alternativa

$$
x_r = \\frac{f(x_l)*x_u}{f(x_l)-f(x_u)} - \\frac{f(x_u)*x_l}{f(x_l)-f(x_u)}
$$

$$
x_r = x_u+ \\frac{f(x_l)*x_u}{f(x_l)-f(x_u)} - \\frac{f(x_u)*x_l}{f(x_l)-f(x_u)} - x_u
$$

$$
x_r = x_u - \\frac{f(x_u)[x_l - x_u]}{f(x_l)-f(x_u)} 
$$

**Esta última forma la necesitamos más adelante**

## Algoritmo para la Falsa posición

1. Encontrar un intervalo en donde $$f(x1)*f(xu)<0$$.
2. Se haya una raíz aproximada:
  $$ x_r = \\frac{f(x_l)*x_u - f(x_u)*x_l}{f(x_l)-f(x_u)}$$

3. Encontrar el subintervalo en donde cae la raíz de la siguiente forma:

  * Si $$f(xl)*f(xr) < 0$$ la raíz está entre el intervalo $xl$ y $xr$. Por tal razón, $xu=xr$ y retorno al paso 2.
  * Si $$f(xl)*f(xr) > 0$$ la raíz está entre el intervalo $xr$ y $xu$. Por tal razón, $xl=xr$ y retorno al paso 2.
  * Si $$f(xl)*f(xr) = 0$$ la raíz es $xr$ y termina el cálculo

### Cálculo del error relativo

$$
e_r = \lvert \\frac{xr_{actual}-xr_{anterior}}{xr_{actual}}\rvert
$$

### Tolerancia

Es qué tan aproximada será la raíz calculada.''')
# Definir el rango de entrada
start_range = st.sidebar.slider("Inicio del rango", -20.0, 20.0, 0.1)
end_range = st.sidebar.slider("Fin del rango", -20.0, 20.0, 2.0)

# Ingresar la función
var = st.sidebar.text_input("Variable", "x")
x = sp.symbols(var)
func = st.sidebar.text_input("Función", "x**3 - x")
y = sp.sympify(func)
tol= st.sidebar.number_input("Tolerancia", 5)

f= sp.lambdify(x,y)

# Ingresar los límites
xl = st.sidebar.number_input("Límite inferior", -20.0, 20.0, 0.2, 0.1)
xu = st.sidebar.number_input("Límite superior", -20.0, 20.0, 1.7, 0.1)

# Tolerancia y valores iniciales
xr = None
xr_ant = xu
error = tol + 1
it = 1

# Dataframe para almacenar los resultados
columnas = ['Xl', 'Xu', 'Xr', 'er(%)', 'f(Xl)', 'f(Xu)', 'f(Xr)']
tabla = pd.DataFrame(columns=columnas)

# Espacio reservado para la figura
fig_placeholder = st.empty()
tablita = st.empty()

while error > tol:
    # Evaluamos la función en los puntos del intervalo
    fxl = y.subs({x: xl}).evalf()
    fxu = y.subs({x: xu}).evalf()

    # Crear la figura
    fig, ax = plt.subplots()
    r = np.linspace(start_range, end_range, 100)
    fx = calculate_y(r, y)

    ax.plot(r, fx, color='blue', label=f"${sp.latex(y)}$")
    ax.vlines(x=0, ymin=min(fx)-0.5, ymax=max(fx)+0.5, color='k')
    ax.hlines(y=0, xmin=min(r)-0.5, xmax=max(r)+0.5, color='k')
    ax.set_title(f"${sp.latex(y)}$")
    ax.grid()

    # Límites xl y xu
    ax.vlines(x=xl, ymin=0, ymax=fxl, color='k', linestyle='--', label=f'$x_l=${xl}')
    ax.vlines(x=xu, ymin=0, ymax=fxu, color='k', linestyle='--', label=f'$x_u=${xu}')

    # Calculamos la raíz
    xr=round(((fxl*xu)-(fxu*xl))/(fxl-fxu),4)
    fxr = y.subs({x: xr}).evalf()
    
    ## Trazo de la linea recta
    ax.plot([xl,xu],[fxl,fxu],color='red')
    
    # Pintamos el punto intermedio
    ax.plot(xr, fxr, 'ro', label=f'Raíz={xr}')
    ax.legend()

    # Actualizamos el error y la tabla
    error = np.abs((xr - xr_ant) / xr) * 100 if xr != 0 else 0
    nueva_fila = {'Xl': xl, 'Xu': xu, 'Xr': xr, 'er(%)': error, 'f(Xl)': fxl, 'f(Xu)': fxu, 'f(Xr)': fxr}
    tabla = pd.concat([tabla, pd.DataFrame([nueva_fila])], ignore_index=True)
    # Actualizamos los límites
    if fxl * fxr < 0:
        xu = xr
    elif fxl * fxr > 0:
        xl = xr
    elif fxl * fxr == 0:
        st.success(f"La raíz está en: ({round(xr,4)}, {round(fxr,4)})")
        break

    xr_ant = xr
    it += 1

    # Mostrar la figura en el espacio reservado
    fig_placeholder.pyplot(fig)
    tablita.dataframe(tabla)
    # Borra la figura para la siguiente iteración
    plt.close(fig)

st.success(f"La raíz está en: ({round(xr,4)}, {round(fxr,4)})")