import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd
from scipy.optimize import linprog
from pulp import LpProblem, LpMinimize, LpVariable, LpStatus


st.title("Metódo grafico para Programación Lineal")
st.markdown("""El Método Gráfico es una técnica intuitiva para resolver problemas de 
            programación lineal con dos variables. Permite visualizar las restricciones 
            y la región factible, facilitando la identificación de la solución óptima. """)
st.image("https://www.gestiondeoperaciones.net/wp-content/uploads/2015/09/metodo-grafico-vitivinicola.gif",use_column_width=True)
st.subheader("Algoritmo del método gráfico")
st.markdown("""El proceso para aplicar el método gráfico incluye:

1. **Representación de Restricciones**: Dibujar las restricciones del problema en un plano bidimensional.
2. **Región Factible**: Identificar la región factible donde se cumplen todas las restricciones.
3. **Puntos extremos**: Encontrar los puntos extremos del área.
4. **Reemplazar en la función objetivo**: Reemplazar en la función objetivo y encontrar la solución. """)

st.subheader("Tipos de soluciones:")
st.markdown("""**Solución Óptima Única:** Este es el caso más común y deseado. 
            Ocurre cuando el algoritmo encuentra un único punto que maximiza o minimiza la 
            función objetivo dentro de la región factible. Este resultado se da cuando 
            existe un vértice de la región factible que proporciona el valor más alto o 
            más bajo de la función objetivo, y no hay otros puntos con el mismo valor.

**Soluciones Múltiples (o Degeneradas):** En este escenario, hay más de un punto óptimo. 
            Esto significa que existen múltiples vértices en la región factible que 
            proporcionan el mismo valor óptimo para la función objetivo. A menudo, esto
             ocurre en problemas donde la función objetivo es paralela a una de las
             restricciones del problema.

**Problema No Acotado:** Sucede cuando la región factible es abierta en la dirección en la 
            que se está optimizando la función objetivo. En otras palabras, no hay un 
            límite en el valor de la función objetivo; puede ir al infinito. Esto 
            generalmente ocurre cuando las restricciones no confinan completamente la 
            región factible en la dirección de optimización.

**Solución Inexistente:** Se da cuando no hay una región factible, es decir, el conjunto 
            de restricciones es tal que no hay ningún punto que satisfaga todas las 
            restricciones al mismo tiempo. Esto puede suceder si las restricciones se 
            contradicen entre sí.

**Ciclo Infinito (menos común):** Aunque raro y generalmente evitado mediante técnicas 
            como la regla de Bland, teóricamente es posible que el método simplex entre 
            en un ciclo infinito, rotando entre un conjunto de soluciones sin llegar
             nunca a una conclusión. Esto puede ocurrir en ciertas situaciones particulares
             donde el algoritmo no logra avanzar hacia una solución óptima debido a la 
            naturaleza de las restricciones y la función objetivo. """)

st.subheader("Pasos del Método Gráfico")
st.markdown("""1. **Definir Restricciones:** El primer paso es definir las restricciones 
            del problema. Estas restricciones son representadas por ecuaciones o 
            inecuaciones lineales.

2. **Representación Gráfica:** Cada restricción se representa gráficamente en un plano 
            bidimensional. Esto se realiza trazando las líneas correspondientes a cada
             ecuación.

3. **Región Factible:** La intersección de todas las restricciones forma la región 
            factible. Es el conjunto de todos los puntos que satisfacen todas las 
            restricciones.

4. **Puntos clave**: Se extraen los vertices en los que se ubica la región factible.

5. **Solución Óptima:** El punto donde la función objetivo es óptima (ya sea máxima o 
            mínima) y que sigue siendo parte de la región factible es la solución al 
            problema de programación lineal. """)


st.subheader("Ejemplo 1 Método gráfico")
st.markdown("Resolveremos el siguiente problema usando el método gráfico")
st.markdown("""$$Max Z= 16x_1 + 10x_2$$
sujeto a:
$$2x_1+2x_2\leq9$$
$$2x_1+x_2 \leq6$$
$$x_1,x_2\geq 0 $$ """)

x, y = sp.symbols('x y')
restriccion1a = 2*x + 2*y - 9
restriccion2a = 2*x + y - 6

# Configurar el rango para las variables
x_valsa = np.linspace(0, 10, 100)

# Convertir restricciones a funciones para y
y_restriccion1a = sp.solve(restriccion1a, y)[0]
y_restriccion2a = sp.solve(restriccion2a, y)[0]

# Convertir a funciones numéricas
func_restriccion1a = sp.lambdify(x, y_restriccion1a, modules=['numpy'])
func_restriccion2a = sp.lambdify(x, y_restriccion2a, modules=['numpy'])

verticesa = [
  (0,6),
  (0,4.5),
  (3,0),
  (4.5,0),
  (1.5,3)
]

optimoa = max(verticesa, key=lambda punto: 3*punto[0] + 2*punto[1])

fig_placeholder= st.empty()

figa,ax =plt.subplots()


ax.plot(x_valsa, func_restriccion1a(x_valsa), label=sp.latex(restriccion1a))
ax.plot(x_valsa, func_restriccion2a(x_valsa), label=sp.latex(restriccion2a))
ax.plot(optimoa[0], optimoa[1], 'ro', label="solución")
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set(xlabel="x", ylabel="y")
ax.grid()
ax.axhline(0, color='black', lw=2)
ax.axvline(0, color='black', lw=2)
ax.fill_between(x_valsa, func_restriccion1a(x_valsa), func_restriccion2a(x_valsa), where=(x_valsa <= 10), color='gray', alpha=0.3,label="Región Factible")
ax.legend()

fig_placeholder.pyplot(figa)

plt.close(figa)



st.header("Ejemplo 2 Método gráfico")
st.markdown("""Un artesano produce cestas y sombreros de mimbre. Por cada cesta gana 
            \$2000 y por cada sombrero \$3000. Para hacer una cesta o un sombrero utiliza
             $1m^2$ de mimbre y en total se dispone de $80m^2$ de mimbre. 1 cesta requiere 
            una hora hombre y 1 sombrero 2 horas hombre. Se disponen de 100 horas. 
            Por razones de almacenamiento, se pueden fabricar como máximo 70 cestas. 
            Plantear el PPL y resolverlo mediante método gráfico """)

st.subheader("Solución:")

st.subheader("Variables de decisión:")
st.markdown("""$x_{1}$ = cantidad de cestas por cada 100 horas.
$x_{2}$ = cantidad de sombreros por cada 100 horas. """)

st.subheader("Función objetivo: (Ganancias):")
st.markdown("Maximizar $Z= 2000 x_{1} + 3000 x_{2}$")

st.subheader("Restricciones estructurales:")
st.markdown("""* $x_{1} + x_{2}<=80$
* $x_{1} + 2x_{2}<=100$
* $x_{1}<=70$ """)
st.subheader("Restricciones de rango o positividad:")
st.markdown("* $x_{1},x_{2}>=0$")

restriccion1b = x + y - 80
restriccion2b = x + 2*y - 100

# Configurar el rango para las variables
x_valsb = np.linspace(0, 120, 200)

# Convertir restricciones a funciones para y
y_restriccion1b = sp.solve(restriccion1b, y)[0]
y_restriccion2b = sp.solve(restriccion2b, y)[0]

# Convertir a funciones numéricas
func_restriccion1b = sp.lambdify(x, y_restriccion1b, modules=['numpy'])
func_restriccion2b = sp.lambdify(x, y_restriccion2b, modules=['numpy'])

verticesb = [
    (60, 20),
    (0, 50),
    (0, 80),
    (70, 0),
    (70,10)
]

optimob = max(verticesb, key=lambda punto: 3*punto[0] + 2*punto[1])

fig_placeholder= st.empty()

figb,axb =plt.subplots()


axb.plot(x_valsb, func_restriccion1b(x_valsb), label=sp.latex(restriccion1b))
axb.plot(x_valsb, func_restriccion2b(x_valsb), label=sp.latex(restriccion2b))
axb.plot(optimob[0], optimob[1], 'ro', label="solución")
axb.axvline(x=70, color='green')
axb.set_xlim(0, 120)
axb.set_ylim(0, 100)
axb.set(xlabel="x", ylabel="y")
axb.grid()
axb.axhline(0, color='black', lw=2)
axb.axvline(0, color='black', lw=2)
axb.fill_between(x_valsb, 0, func_restriccion2b(x_valsb), where=((x_valsb >= 0) & (x_valsb <= 60)), color='gray', alpha=0.3, label="Región Factible")
axb.fill_between(x_valsb, 0, func_restriccion1b(x_valsb), where=((x_valsb >= 60) & (x_valsb <= 70)), color='gray', alpha=0.3)
axb.legend()

fig_placeholder.pyplot(figb)

plt.close(figb)

###########################################################


st.header("Ejemplo 3 Método gráfico")

st.markdown("""La empresa X ha sacado del mercado un producto que ya no era rentable, lo cual 
            genera que haya una capacidad disponible semanal que no se está utilizando en 
            sus tres departamentos así: 200 horas en corte, 240 horas en soldadura y 150 
            horas en empaque.
Producción propone que dicha capacidad sea utilizada en la producción de puertas, ventanas 
            y claraboyas en la forma más eficiente posible, para dichos artículos se ha 
            establecido los siguientes precios de venta \$5000, \$3000 y \$4000 por unidad 
            respectivamente. Además se ha determinado que para producir una puerta se 
            requiere dos horas en corte, 3 horas en soldadura y 5 horas en empaque. Para 
            producir una ventana se requiere 5 horas en corte, 4 horas en soldadura y 1 
            hora en empaque, maientras que para producir una claraboya se requiere 4 horas
             en corte, 2 horas en soldadura y 3 horas en empaque. Plantee el modelo se 
            programación lineal que se genera si se sabe que mercadeo informo que mínimo 
            se venderán 20 ventanas y como máximo 10 claraboyas. """)

st.subheader("Solución:")

st.subheader("Variables de decisión:")
st.markdown("""$x_{1}$ = cantidad de puertas.
$x_{2}$ = cantidad de ventanas.
$x_{3}$ = cantidad de claraboyas. """)

st.subheader("Función objetivo: (Ganancias):")
st.markdown("Maximizar $Z= 5000 x_{1} + 3000 x_{2} + 4000x_{3}$")

st.subheader("Restricciones estructurales:")
st.markdown("""* * $2x_{1} + 5x_{2} + 4x_{3}<=200$
* $3x_{1} + 4x_{2} + 2x_{3}<=240$
* $5x_{1} + x_{2} + 3x_{3}<=150$
* $x_{2}>=20$
* $x_{3}<=10$""")
st.subheader("Restricciones de rango o positividad:")
st.markdown("* $x_{1},x_{2},x_{3}>=0$")

restriccion1b = x + y - 80
restriccion2b = x + 2*y - 100

# Coeficientes de la función objetivo
c = [-5000, -3000, -4000]

# Coeficientes de las restricciones
A = [
    [2, 5, 4],
    [3, 4, 2],
    [5, 1, 3],
    [0, -1, 0],  # Restricción de x2 >= 20
    [0, 0, -1]   # Restricción de x3 <= 10
]

# Límites de las restricciones
b = [200, 240, 150, -20, 10]

# Resolviendo el problema de programación lineal
result = linprog(c, A_ub=A, b_ub=b)

# Imprimiendo la solución
print("Resultados de la optimización:\n", result)

# Extrayendo los valores de las variables de decisión
x1, x2, x3 = result.x

# Puntos extremos para graficar
xc = np.linspace(0, 30, 100)

# Restricciones
eq1 = (200 - 2 * xc) / 4
eq2 = (240 - 3 * xc) / 2
eq3 = (150 - 5 * xc)

# Restricciones adicionales para x2 y x3
x2_constraint = np.full_like(xc, 20)  # x2 >= 20
x3_constraint = np.full_like(xc, 10)  # x3 <= 10

# Gráficos
fig_placeholder= st.empty()

figc, axc= plt.subplots()

axc.plot(xc, eq1, label=r'$2x_1 + 5x_2 + 4x_3 \leq 200$')
axc.plot(xc, eq2, label=r'$3x_1 + 4x_2 + 2x_3 \leq 240$')
axc.plot(xc, eq3, label=r'$5x_1 + x_2 + 3x_3 \leq 150$')
axc.plot(xc, x2_constraint, label=r'$x_2 \geq 20$', linestyle='--')
axc.plot(xc, x3_constraint, label=r'$x_3 \leq 10$', linestyle='--')

axc.fill_between(xc, np.minimum(np.minimum(eq1, eq2), eq3), where=(xc >= 0) & (xc <= x1), color='gray', alpha=0.5, label='Factible')
axc.scatter(x1, x2, color='red', marker='o', label='Solución óptima')

axc.set_xlabel(r'$x_1$')
axc.set_ylabel(r'$x_2$')
axc.set_title('Programación Lineal - Método Gráfico')
axc.legend()
axc.grid(True)

fig_placeholder.pyplot(figc)

plt.close(figc)


########################################
st.header("Ejemplo 4 Programación Lineal")

st.markdown("""Para una cafetería que trabaja 24 horas se requieren las 
            siguientes meseras: """)
st.image("https://github.com/BioAITeamLearning/Metodos_2023_03_UAM/blob/main/_static/images/problemaopt.png?raw=true",use_column_width=True)
st.markdown("""Cada mesera trabaja 8 horas consecutivas por día. El administrador de la 
            cafetería debe determinar el numero mínimo de meseras para cumplir los 
            requisitos anteriores. """)

st.subheader("Solución:")

st.subheader("Variables de decisión:")
st.markdown("""$x_{1}$ = cantidad de meseras para el turno 1.
$x_{2}$ = cantidad de meseras para el turno 2.
$x_{3}$ = cantidad de meseras para el turno 3.
$x_{4}$ = cantidad de meseras para el turno 4.
$x_{5}$ = cantidad de meseras para el turno 5.
$x_{6}$ = cantidad de meseras para el turno 6.""")

st.subheader("Función objetivo: (Meseras):")
st.markdown("""Minimizar el numero de meseras
Minimizar $Z= x_{1} +  x_{2} + x_{3} + x_{4} +  x_{5} + x_{6}$ """)

st.subheader("Restricciones estructurales:")
st.markdown("""* $x_{6} + x_{1}>=4$
* $x_{1} + x_{2}>=8$
* $x_{2} + x_{3}>=10$
* $x_{3} + x_{4}>=7$
* $x_{4} + x_{5}>=12$
* $x_{5} + x_{6}>=4$ """)

st.subheader("Restricciones de rango o positividad:")
st.markdown("* $x_{1},x_{2},x_{3},x_{4},x_{5},x_{6}>=0$")

restriccion1b = x + y - 80
restriccion2b = x + 2*y - 100

# Crea el problema
problema = LpProblem("Minimizar_Numero_Meseras", LpMinimize)

# Variables de decisión
x1d = LpVariable("x1", lowBound=0)
x2d = LpVariable("x2", lowBound=0)
x3d = LpVariable("x3", lowBound=0)
x4d = LpVariable("x4", lowBound=0)
x5d = LpVariable("x5", lowBound=0)
x6d = LpVariable("x6", lowBound=0)

# Función objetivo
problema += x1d + x2d + x3d + x4d + x5d + x6d, "Z"

# Restricciones
problema += x6d + x1d >= 4
problema += x1d + x2d >= 8
problema += x2d + x3d >= 10
problema += x3d + x4d >= 7
problema += x4d + x5d >= 12
problema += x5d + x6d >= 4

# Resuelve el problema
problema.solve()

# Imprime los resultados
st.write("Estado:", LpStatus[problema.status])
st.write("Número de meseras:")
for var in problema.variables():
    st.write(f"{var.name} = {var.varValue}")

st.write("Valor de Z (Número mínimo de meseras):", problema.objective.value())
