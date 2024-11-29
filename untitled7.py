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
    # Cargar datos del API
data = requests.get("https://restcountries.com/v3.1/all").json()

if df is not None and not df.empty:
    # Verifica si las columnas necesarias existen
    if 'name' in df.columns:
        df['Nombre'] = df['name'].apply(lambda x: x.get('common') if isinstance(x, dict) else None)
    else:
        df['Nombre'] = None

    if 'region' in df.columns:
        df['Región'] = df['region']
    else:
        df['Región'] = None

    if 'population' in df.columns:
        df['Población'] = df['population']
    else:
        df['Población'] = None

    if 'area' in df.columns:
        df['Área (km²)'] = df['area']
    else:
        df['Área (km²)'] = None

    if 'borders' in df.columns:
        df['Fronteras'] = df['borders'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    else:
        df['Fronteras'] = 0

    if 'languages' in df.columns:
        df['Idiomas Oficiales'] = df['languages'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
    else:
        df['Idiomas Oficiales'] = 0

    if 'timezones' in df.columns:
        df['Zonas Horarias'] = df['timezones'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    else:
        df['Zonas Horarias'] = 0

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
