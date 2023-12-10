
import streamlit as st
import pandas as pd
from io import BytesIO

def main():
    st.title("Descarga el manual de usuario ")

    # Ruta del archivo PDF en tu sistema de archivos local
    pdf_filepath = "D:\Guía de Usuario Método Númericos.pdf"

    # Botón para descargar el archivo
    if st.button("Descargar Archivo PDF"):
        download_pdf(pdf_filepath)

def download_pdf(pdf_filepath):
    with open(pdf_filepath, "rb") as f:
        pdf_bytes = f.read()

    st.download_button(
        label="Descargar Archivo PDF",
        data=pdf_bytes,
        file_name="Guía de Usuario Método Númericos y Optimización.pdf",  # Puedes cambiar el nombre del archivo aquí
        mime="application/pdf"
    )

if __name__ == "__main__":
    main()




def main():
    st.title("Métodos Numéricos y Optimización")

    st.header("Métodos Numéricos")
    st.markdown(
        """
        Los métodos numéricos son técnicas matemáticas que se utilizan para aproximar soluciones 
        a problemas matemáticos que no pueden resolverse de manera exacta. Algunas aplicaciones 
        comunes incluyen:

        - Resolución de ecuaciones y sistemas de ecuaciones.
        - Integración y derivación numérica.
        - Interpolación y ajuste de curvas.
        - Resolución de ecuaciones diferenciales.
        - Álgebra matricial.

        Estos métodos son esenciales cuando no es posible encontrar soluciones analíticas exactas.
        """
    )

    st.header("Optimización")
    st.markdown(
        """
        La optimización se centra en encontrar el mejor resultado posible en situaciones donde hay 
        múltiples opciones. Algunos ejemplos de aplicaciones son:

        - Optimización matemática para maximizar o minimizar funciones.
        - Diseño y control de sistemas para mejorar eficiencia.
        - Planificación y asignación de recursos.
        - Aplicaciones en finanzas y economía para maximizar rendimientos o minimizar riesgos.
        - Aprendizaje automático, donde se optimizan funciones de costo.

        La optimización es crucial para tomar decisiones informadas y eficientes en diversos campos.
        """
        
    )

if __name__ == "__main__":
    main()

st.header("Cálculo de raíces")
st.markdown("Los siguientes métodos númericos se emplean para el cálculo de raíces: ")
st.markdown("""1. Método de la bisección
2. Método de la falsa posición
3. Metodo de Newton Raphson
4. Método de la secante
5. Método de la secante modificada
6. Método de iteración de punto fijo """)

st.header("Ajuste de curvas e interpolación")
st.markdown("Los siguientes métodos númericos se emplean para ajuste de curvas e interpolación: ")
st.markdown("""1. Método de regresión por mínimos cuadrados
2. Interpolación de lagrange
3. Splines Cúbicos
4. Método de regresión polinomial""")

st.header("Diferenciación e integración")
st.markdown("Los siguientes métodos númericos se emplean para diferenciación e integración de funciones: ")
st.markdown("""1. Método de Euler 
2. Regla trapezoidal
3. Regla trapezoidal multiple
4. Regla de Simpson 1/3
5. Regla de Simpson 1/3 múltiple
6. Regla de Simpson 3/8
7. Regla de Simpson 3/8 múltiple""")

st.header("Optimización irrestricta")
st.markdown("Los siguientes métodos númericos se emplean para optimización irrestrica de funciones: ")
st.markdown("""1. Sección dorada para máximos
2. Sección dorada para mínimos
3. Interpolación cuadrática para máximos
4. Interpolación cuadrática para mínimos
5. Método de Newton Raphson
6. Método del gradiente para máximos
7. Método del gradiente para mínimos
""")

st.header("Ecuaciones Diferenciales Ordinarias")
st.markdown("Los siguientes métodos númericos se emplean para la solución de ecuaciones diferenciales ordinarias: ")
st.markdown("""1. Método de Euler
2. Runge Kutta de Orden 2
3. Ejemplo Runge Kutta de Orden 2 (Módelo de Lotka-Volterra)
4. Interpolación cuadrática para mínimos
5. Runge Kutta de Orden 3
6. Runge Kutta de Orden 4
             """)

st.header("Programación lineal - Optimización con restricciones")
st.markdown("Los siguientes métodos númericos se emplean para la optimización con restricciones : ")
st.markdown("O para modelos de programación lineal")
st.markdown("""1. Método gráfico
2. Método Simplex
             """)
