import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd
from scipy.optimize import minimize

st.title("Optimización unidiemensional no restringida")
st.image("https://www.disfrutalasmatematicas.com/algebra/images/function-max-min.svg",use_column_width=True)
st.image("https://bioaiteamlearning.github.io/Metodos_2023_03_UAM/_static/images/Optimizacion.png",use_column_width=True)

st.header("Obtención de puntos críticos mediante la matriz Hessiana")
st.markdown("""La matriz hessiana es una matriz cuadrada de segundas derivadas parciales de una función 
            escalar. Es una herramienta importante en cálculo multivariable y optimización,
             y proporciona información sobre la concavidad y la geometría local de una 
            función.""")
st.markdown("""Dada una función $f : R^{n} = R$ con derivadas parciales continuas
            hasta segundo orden, la matriz hessiana de $f$, denoda como $H(f)$ o 
            $Hessian(f)$ es una matriz de $n x n$ cuyas entradas son las segundas derivadas
            parciales de $f$ con respecto a las variables involucradas. La entrada en la fila 
            $i$ y la columna $j$ de la matriz hessiana es la segunda derivada parcial de 
            $f$ con respecto a la variable $i$-ésima y la variable $j$-ésima""")
st.markdown("Matematicamente, la matriz hessiana se expresa de la siguiente manera ")

st.latex(r""" H(f) = \begin{bmatrix}
    \frac{\partial^2 f}{\partial x_1^2} & \frac{\partial^2 f}{\partial x_1 \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_1 \partial x_n} \\
    \frac{\partial^2 f}{\partial x_2 \partial x_1} & \frac{\partial^2 f}{\partial x_2^2} & \cdots & \frac{\partial^2 f}{\partial x_2 \partial x_n} \\
    \vdots & \vdots & \ddots & \vdots \\
    \frac{\partial^2 f}{\partial x_n \partial x_1} & \frac{\partial^2 f}{\partial x_n \partial x_2} & \cdots & \frac{\partial^2 f}{\partial x_n^2}
\end{bmatrix}""")


st.markdown("""El objetivo es encontrar el máximo o el mínimo de una función de una 
            variable sin restricciones, es decir, no lineal.""")

st.subheader("Ejemplo de la matriz hessiana")
st.markdown("Hallaremos el punto crítico de la siguiente función:")

fy = st.text_input("Ingrese la función","x**2 + y**2")

x, y = sp.symbols('x y')

# Pide al usuario que ingrese la expresión de la función
my_function = sp.sympify(fy)

# Calcula las segundas derivadas parciales con SymPy
df_dx = sp.diff(my_function, x)
df_dy = sp.diff(my_function, y)
d2f_dx2 = sp.diff(df_dx, x)
d2f_dy2 = sp.diff(df_dy, y)
d2f_dxdy = sp.diff(df_dx, y)

# Define la matriz hessiana
hessian = sp.Matrix([[d2f_dx2, d2f_dxdy],
                  [d2f_dxdy, d2f_dy2]])

# Paso 3: Encuentra los puntos críticos
def find_critical_points(expression):
   
    n = 2  # Cambia esto al número de variables (N) de tu función
    initial_guess = np.ones(n)  # Supongamos un punto inicial
    result = minimize(lambda vars: my_function.subs({x: vars[0], y: vars[1]}), initial_guess, method='BFGS', jac=None)

    if result.success:
        # Calcula la matriz hessiana en el punto crítico
        hessian_at_critical = np.array(hessian.subs({x: result.x[0], y: result.x[1]}), dtype=float)
        eigenvalues, _ = np.linalg.eig(hessian_at_critical)

        if all(eigenvalues > 0):
            return result.x, "Mínimo local"
        elif all(eigenvalues < 0):
            return result.x, "Máximo local"
        else:
            return result.x, "Punto de silla"
    else:
        return None, None

# Encuentra y clasifica los puntos críticos para la función proporcionada por el usuario
critical_point, point_type = find_critical_points(my_function)

st.subheader("Solución:")

if critical_point is not None:
    st.write(f"Punto crítico encontrado en: {round(critical_point[0],10)} , {round(critical_point[0],10)}")
    st.write("Tipo de punto crítico:", point_type)
else:
    st.write("No se encontró un punto crítico.")

numeric_function = sp.lambdify((x, y), my_function, 'numpy')


x_vals = np.linspace(-10, 10, 100)
y_vals = np.linspace(-10, 10, 100)
x_grid, y_grid = np.meshgrid(x_vals, y_vals)
z_vals = numeric_function(x_grid, y_grid)

fig_placeholder= st.empty()
# Muestra la gráfica de la función
fig1,ax= plt.subplots()

ax = fig1.add_subplot(111, projection='3d')
ax.plot_surface(x_grid, y_grid, z_vals, cmap='viridis')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Gráfica de la función')

fig_placeholder.pyplot(fig1)

fig_placeholder= st.empty()

fig2d, ax2d = plt.subplots()
contour = ax2d.contour(x_grid, y_grid, z_vals, levels=20, cmap='viridis')
ax2d.set_xlabel('x')
ax2d.set_ylabel('y')
ax2d.set_title('Contorno de la función')

fig_placeholder.pyplot(fig2d)