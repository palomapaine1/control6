import streamlit as st
import pandas as pd
import requests

# Título de la aplicación
st.title('Aplicación Web: Datos desde una API REST')
# URL de la API REST (puedes cambiarla por cualquier API pública que devuelva JSON)
api_url = 'https://jsonplaceholder.typicode.com/posts'
# Realizar la petición a la API
response = requests.get(api_url)
# Verificar que la respuesta sea exitosa (código 200)
if response.status_code == 200:
    # Convertir los datos JSON en un DataFrame de Pandas
    data = response.json()
    df = pd.DataFrame(data)
    # Mostrar los primeros registros
    st.write('Datos obtenidos de la API:')
    st.write(df.head())
else:
    st.error('Error al obtener los datos de la API')
# Si hay datos, mostrar el DataFrame, mostrar dataframe con las columna seleccionadas, permitir filtrado y mostrar gráficos.
# Título de la aplicación
st.title('Aplicación Web: Datos desde una API REST')
# URL de la API REST (puedes cambiarla por cualquier API pública que devuelva JSON)
api_url = 'https://jsonplaceholder.typicode.com/posts'
# Realizar la petición a la API
response = requests.get(api_url)
# Verificar que la respuesta sea exitosa (código 200)
if response.status_code == 200:
    # Convertir los datos JSON en un DataFrame de Pandas
    data = response.json()
    df = pd.DataFrame(data)
    # Mostrar los primeros registros
    st.write('Datos obtenidos de la API:')
    st.write(df.head())
else:
    st.error('Error al obtener los datos de la API')
    # Cargar datos del API
data = requests.get("https://restcountries.com/v3.1/all").json()

# Convertir los datos en un DataFrame para facilitar la manipulación
if data:
    countries_df = pd.json_normalize(data)
    countries_df = countries_df[
        ["name.common", "region", "population", "area", "languages", "borders"]]
    countries_df.rename(
        columns={
            "name.common": "Nombre",
            "region": "Región",
            "population": "Población",
            "area": "Área",
            "languages": "Idiomas",
            "borders": "Fronteras",
        },
        inplace=True,)

# Interfaz de usuario
st.title("Interacción con Datos de Países ")

# Opción para mostrar los datos originales
if st.checkbox("Mostrar datos originales"):
    st.write(countries_df)

# Seleccionar un país
selected_country = st.selectbox(
    "Selecciona un país:", countries_df["Nombre"].sort_values())
if selected_country:
    country_data = countries_df[countries_df["Nombre"] == selected_country]
    st.write(f"Datos del país seleccionado: {selected_country}")
    st.write(country_data)

# Filtrar países por población
population_threshold = st.slider(
    "Selecciona un umbral de población:", 
    min_value=int(countries_df["Población"].min()), 
    max_value=int(countries_df["Población"].max()), 
    value=int(countries_df["Población"].median()))
filtered_countries = countries_df[countries_df["Población"] > population_threshold]
st.write(f"Países con población mayor a {population_threshold}:")
st.write(filtered_countries)

# Cargar archivo adicional
uploaded_file = st.file_uploader("Cargar archivo adicional (opcional):", type=["csv"])
if uploaded_file:
    uploaded_data = pd.read_csv(uploaded_file)
    st.write("Datos cargados:")
    st.write(uploaded_data)
