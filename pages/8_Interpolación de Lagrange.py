import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd

st.sidebar.markdown("# Lagrange")

# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Configuración de la página
st.title("Interpolación de Lagrange")

st.write('''Esta es una técnica para obtener funciones polinómicas que se ajusten a un conjunto de puntos en coordenadas rectangulares.
''')
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Lagrange_polynomial.svg/500px-Lagrange_polynomial.svg.png", caption='Método gráfico ', use_column_width=True)

st.write('''La función polinómica se define como:

$$P_n (x) = ∑_{i=0}^{n-1} f(x_i)L_i(x)$$


Donde $L_i(x)$ tiene la forma:

$$L_i(x) = 𝜫_{j=0; j \\ne i}^{n-1} \\frac{x - x_j}{xi - x_j}$$


con:

$i= 0,1,...,n-1$

$j = 0,1,...,n-1$


''')

# Definir el rango de entrada
start_range = st.sidebar.slider("Inicio del rango", -20.0, 20.0, 0.1)
end_range = st.sidebar.slider("Fin del rango", -20.0, 20.0, 2.0)

Archivo=st.sidebar.file_uploader("Suba el archivo CSV")

# Ingresar la función
var_1 = st.sidebar.text_input("Variable", "X")
var_2= st.sidebar.text_input("Variable", "Y")

# Lee el archivo CSV y almacénalo en un DataFrame
df = pd.read_csv(Archivo)

# Extraer los valores de x e y
x = np.array(df[var_1])
y = np.array(df[var_2])

# Función para calcular el polinomio de Lagrange
def lagrange_interpolation(x, y, x_interp):
    n = len(x)
    result = 0

    for i in range(n):
        term = y[i]
        for j in range(n):
            if i != j:
                term *= (x_interp - x[j]) / (x[i] - x[j])
        result += term

    return result

# Calcular los valores interpolados para x
x_interp = x  # Puedes cambiar esto por los valores de x que desees interpolar
y_interp = [lagrange_interpolation(x, y, xi) for xi in x_interp]

# Crear una tabla con los valores de x, y y P(x)
table = pd.DataFrame({'x': x_interp, 'y': y, 'P(x)': y_interp})

 # Imprimir la tabla
print(table)


fig_placeholder= st.empty()
tablita= st.empty()

# Generar la gráfica
fig, ax = plt.subplots()

ax.scatter(x, y, color='blue', label="Datos")
ax.plot(x_interp, y_interp, color='red', label="Interpolación de Lagrange")

ax.set_title("Interpolación de Lagrange")
ax.grid()
ax.legend()
plt.show()

# Imprimir el polinomio interpolante
def lagrange_polynomial(x, y):
    n = len(x)
    terms = []
    for i in range(n):
        term = f"{y[i]:.2f}"
        for j in range(n):
            if i != j:
                term = f"{term} * (x - {x[j]:.2f}) / ({x[i]:.2f} - {x[j]:.2f})"
        terms.append(term)
    return " + ".join(terms)

polynomial = lagrange_polynomial(x, y)
st.text(f"Polinomio interpolante: P(x) = {polynomial}" )

plt.close(fig)

fig_placeholder.pyplot(fig)
tablita.dataframe(table)