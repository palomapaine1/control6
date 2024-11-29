import streamlit as st
import pandas as pd
import requests

# Cargar los datos procesados
@st.cache
def load_data():
    response = requests.get("https://restcountries.com/v3.1/all")
    data = response.json()
    countries_data = []
    for country in data:
        name = country.get("name", {}).get("common", "N/A")
        region = country.get("region", "N/A")
        population = country.get("population", 0)
        area = country.get("area", 0)
        borders = len(country.get("borders", []))
        languages = len(country.get("languages", {}))
        timezones = len(country.get("timezones", []))
        countries_data.append({
            "Nombre": name,
            "Región": region,
            "Población": population,
            "Área (km²)": area,
            "Fronteras": borders,
            "Idiomas Oficiales": languages,
            "Zonas Horarias": timezones
        })
    return pd.DataFrame(countries_data)

df = load_data()

# Configurar las páginas
st.set_page_config(page_title="Aplicación de Datos de Países", layout="wide")

# Páginas
pages = ["Inicio", "Interacción con Datos", "Visualización de Gráficos"]
page = st.sidebar.selectbox("Navegación", pages)

# Página 1: Descripción del Proyecto
if page == "Inicio":
    st.title("Proyecto de Datos de Países")
    st.write("""
    Esta aplicación utiliza la API REST Countries para obtener información sobre todos los países del mundo.
    Los datos incluyen nombre, región, población, área, fronteras, idiomas y zonas horarias. Explora la aplicación 
    para analizar y visualizar los datos de manera interactiva.
    """)
    st.markdown("[API REST Countries](https://restcountries.com/v3.1/all)")

# Página 2: Interacción con los Datos
elif page == "Interacción con Datos":
    st.title("Interacción con los Datos")
    
    st.subheader("Datos Originales")
    st.dataframe(df)

    # Selección de columna y cálculo de estadísticas
    col = st.selectbox("Selecciona una columna numérica", ["Población", "Área (km²)", "Fronteras", "Idiomas Oficiales", "Zonas Horarias"])
    st.write(f"Media: {df[col].mean():.2f}")
    st.write(f"Mediana: {df[col].median():.2f}")
    st.write(f"Desviación Estándar: {df[col].std():.2f}")

    # Ordenar datos
    orden_col = st.selectbox("Selecciona una columna para ordenar", df.columns)
    ascendente = st.checkbox("Orden Ascendente", value=True)
    df_ordenado = df.sort_values(by=orden_col, ascending=ascendente)
    st.dataframe(df_ordenado)

    # Filtro por columna numérica
    filtro = st.slider("Selecciona un rango de población", int(df["Población"].min()), int(df["Población"].max()))
    df_filtrado = df[df["Población"] <= filtro]
    st.dataframe(df_filtrado)

    # Botón para descargar datos filtrados
    if st.button("Descargar Datos Filtrados"):
        buffer = BytesIO()
        df_filtrado.to_csv(buffer, index=False)
        buffer.seek(0)
        st.download_button("Descargar CSV", buffer, file_name="datos_filtrados.csv", mime="text/csv")

# Página 3: Visualización de Gráficos
elif page == "Visualización de Gráficos":
    st.title("Visualización de Gráficos")

    # Selección de variables
    x_col = st.selectbox("Selecciona el eje X", df.select_dtypes(include="number").columns)
    y_col = st.selectbox("Selecciona el eje Y", df.select_dtypes(include="number").columns)

    # Tipo de gráfico
    tipo_grafico = st.selectbox("Selecciona el tipo de gráfico", ["Dispersión", "Línea", "Barra", "Histograma"])

    # Crear el gráfico
    fig, ax = plt.subplots()
    if tipo_grafico == "Dispersión":
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
    elif tipo_grafico == "Línea":
        sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
    elif tipo_grafico == "Barra":
        sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
    elif tipo_grafico == "Histograma":
        sns.histplot(data=df[x_col], ax=ax)

    st.pyplot(fig)

    # Descargar gráfico
    if st.button("Descargar Gráfico"):
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        st.download_button("Descargar PNG", buffer, file_name="grafico.png", mime="image/png")
