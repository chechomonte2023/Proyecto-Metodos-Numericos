import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.sidebar.markdown("# Bisección ")

# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Configuración de la página
st.title("Método Bisección")
st.write('''Consiste en hallar una raíz aproximada de una función en un intervalo dado. 

Tiende a ser menos eficiente por ser más lento, debido a la cantidad de iteraciones que se 
requieren para lograr un resultado (convergencia). 

Consiste en subdividir el intervalo 
en otros 2 iguales y evaluar la función con el objetivo de ubicar en donde se hace el 
cambio de signo, y se sigue repitiendo hasta encontrar la raíz.''')

# Carga la imagen desde un archivo local
st.image("https://bioaiteamlearning.github.io/Metodos_2023_03_UAM/_images/014ec9c5da7850b12b002cf32807b8aac8c1e14713a78331b81a90d7ebdcec3a.png", caption='Método gráfico Bisección', use_column_width=True)

st.header("Algoritmo para la bisección")
st.write(''' 1. Encontrar un intervalo en donde $$f(x1)*f(xu)<0$$.
2. Se haya una raíz aproximada:
   $xr = \\frac{xl+xu}{2}$"
3. Encontrar el subintervalo en donde cae la raíz de la siguiente forma:

  * Si $$f(xl)*f(xr) < 0$$ la raíz está entre el intervalo $xl$ y $xr$. Por tal razón, $xu=xr$ y retorno al paso 2.
  * Si $$f(xl)*f(xr) > 0$$ la raíz está entre el intervalo $xr$ y $xu$. Por tal razón, $xl=xr$ y retorno al paso 2.
  * Si $$f(xl)*f(xr) = 0$$ la raíz es $xr$ y termina el cálculo
''')
st.header("Cálculo del error relativo")
st.write('''$$
e_r = \lvert \\frac{xr_{actual}-xr_{anterior}}{xr_{actual}}\rvert
$$''')
st.header("Tolerancia")
st.write("Es qué tan aproximada será la raíz")

st.write("Este segmento muestra la gráfica de Bisección.")


# Definir el rango de entrada
start_range = st.sidebar.slider("Inicio del rango", -20.0, 20.0, 0.1)
end_range = st.sidebar.slider("Fin del rango", -20.0, 20.0, 2.0)

# Ingresar la función
var= st.sidebar.text_input ("Variable", "x")
x = sp.symbols(var)
func = st.sidebar.text_input("Función", "x**3 - x")
y = sp.sympify(func)
tol= st.sidebar.number_input("Tolerancia", 5)

# Ingresar los límites
xl = st.sidebar.number_input("Límite inferior", -10.0, 10.0, 0.2, 0.1)
xu = st.sidebar.number_input("Límite superior", -10.0, 10.0, 1.7, 0.1)

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
    xr = round((xl + xu) / 2, 4)
    fxr = y.subs({x: xr}).evalf()

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
print(xl, xu)