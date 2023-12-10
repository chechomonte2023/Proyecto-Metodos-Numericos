import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error

st.sidebar.markdown("# Regresión Mínimos Cuadrados")

# Función para calcular y
def calculate_y(x_values, expression):
    return [expression.subs({x: xi}) for xi in x_values]

# Configuración de la página
st.title("Método Regresión Mínimos Cuadrados")
st.write('''a regresión por mínimos cuadrados es un método utilizado para encontrar la mejor línea de ajuste para un conjunto de puntos de datos.

 La regresión por mínimos cuadrados es una técnica estadística y numérica utilizada para analizar y modelar la relación entre una variable dependiente y una o más variables independientes. Su objetivo principal es encontrar la mejor línea (o superficie, en el caso de múltiples variables independientes) que se ajuste a un conjunto de datos.''')
st.image("https://www.marionomics.com/content/images/image/fetch/w_1200,h_600,c_limit,f_jpg,q_auto:good,fl_progressive:steep/https-3a-2f-2fsubstack-post-media.s3.amazonaws.com-2fpublic-2fimages-2f742471f3-2dc4-498c-9a0d-b45cfb400ebb_1024x768.jpg", caption='Método gráfico ', use_column_width=True)

st.write('''
## Algoritmo de la regresión por mínimos cuadrados

La línea de regresión lineal tiene la forma
$$Y = mX + b$$

Donde $m$ es la pendiente de la recta, $b$ es el intercepto (bias) de la recta

1. **Datos de entrada 
$
(X_n, Y_n,)
$**
2. Calcular las sumatorias
$$
∑_X
$$
$$
∑_Y
$$
$$
∑_{X^2}
$$
$$
∑_{XY}
$$

3. Calcular pendiente e intercepto

$$
m = \\frac{n∑_{XY} - ∑_X ∑_Y}{n∑_{X^2} -(∑_X)^2}
$$

Donde $n$ es la cantidad total de datos.

$$
b = \\frac{∑_Y- m∑_X}{n}
$$

## Cálculo de error de una regresión por mínimos cuadrados:

Revisar el error en la regresión por mínimos cuadrados es esencial para determinar qué tan bien se ajusta el modelo a los datos observados.

### Error cuadrático médio (ECM)
El error cuadrático medio (ECM) de un estimador mide el promedio de los errores al cuadrado, es decir, la diferencia entre el estimador y lo que se estima. El ECM es una función de riesgo, correspondiente al valor esperado de la pérdida del error al cuadrado o pérdida cuadrática.

Si $\hat{Y}$ es un vector de n predicciones y $Y$ es el vector de los verdaderos valores, entonces el (estimado) ECM del predictor es:

$$
ECM = \\frac{1}{n}∑_{i=1}^{n} (Y_{i} - \hat{Y}_{i} )^2
$$

### $R^2$: Coeficiente de determinación

El coeficiente de determinación es una medida estadística que examina cómo las diferencias en una variable pueden ser explicadas por la diferencia en una segunda variable, al predecir el resultado de un evento determinado. En otras palabras, este coeficiente, que se conoce más comúnmente como R-cuadrado (o R2), evalúa la fuerza de la relación lineal entre dos variables, y es muy utilizado por los investigadores cuando realizan análisis de tendencias.

$$
R^2 = 1 - \\frac{\\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{\\frac{1}{n} \sum_{i=1}^{n} (y_i - \\bar{y})^2}
$$''')
# Definir el rango de entrada
start_range = st.sidebar.slider("Inicio del rango", -20.0, 20.0, 0.1)
end_range = st.sidebar.slider("Fin del rango", -20.0, 20.0, 2.0)

Archivo=st.sidebar.file_uploader("Suba el archivo CSV")

# Lee el archivo CSV y almacénalo en un DataFrame
d = pd.read_csv(Archivo)

# Ingresar la función
var_1 = st.sidebar.text_input("Variable", "X")
x = np.array(d[var_1])
var_2= st.sidebar.text_input("Variable", "Y")
y = np.array(d[var_2])


# Espacio reservado para la figura
fig_placeholder = st.empty()
tablita = st.empty()

sx = np.sum(x)
sy = np.sum(y)

sx2 = np.sum(x**2)
sxy = np.sum(x*y)

n = len(x)

m = ((n*sxy) - (sx*sy))/((n*sx2)-(sx**2))
b = (sy -(m*sx))/n

st.text(f"Pendiente: {m}")
st.text(f"Intercepto: {b} ")

recta = m*x + b

r2 = r2_score(y, recta)
print(f"R^2: {r2}")

mse = mean_squared_error(y, recta)
print(f"mse: {mse}")

fig, ax = plt.subplots()

ax.scatter(d["X"].to_list(),d["Y"].to_list(),color='blue',label="datos")
ax.plot(x,recta,color='red',label="y=mx+b")

ax.set_title("Regresion")
ax.grid()
ax.legend()
plt.show()


# Mostrar la figura en el espacio reservado
fig_placeholder.pyplot(fig)