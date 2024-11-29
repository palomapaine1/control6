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
    df['Zonas Horarias'] = df['timezones'].apply(lambda x: len(x) if isinstance(x, list) else 0)

    # Filtrar columnas seleccionadas
    columnas = ['Nombre', 'Región', 'Población', 'Área (km²)', 'Fronteras', 'Idiomas Oficiales', 'Zonas Horarias']
    df_cleaned = df[columnas]

    # Mostrar DataFrame con las columnas seleccionadas
    st.title("Interacción con los datos:")
    st.write("Mostrar datos originales:")
    st.dataframe(df_cleaned)

    st.header("Selecciona una columna del dataframe utilizando un menú desplegable")
    columnas = st.multiselect('Selecciona las columnas a visualizar', df_cleaned.columns.tolist(), default=df_cleaned.columns.tolist())
    df_seleccionado = df_cleaned[columnas]
    # Mostrar el DataFrame con las columnas seleccionadas
    st.write('Columna Selecionada:')
    st.write(df_seleccionado)
    st.write("Estadísticas de las columnas seleccionadas:")
    st.write("Media:",)
    st.write(df_seleccionado.mean(numeric_only=True))
    st.write("Mediana:",)
    st.write(df_seleccionado.mean(numeric_only=True))
    st.write("Desviación estándar:",)
    st.write(df_seleccionado.std(numeric_only=True))

    columna_ordenar = st.selectbox('Selecciona una columna para ordenar', df_seleccionado.columns)
    # Control para seleccionar el orden (ascendente o descendente)
    orden = st.radio('Selecciona el orden:', ('Ascendente', 'Descendente'))
    # Ordenar el DataFrame según la columna seleccionada y el orden elegido
    if orden == 'Ascendente':
        df_ordenado = df_seleccionado.sort_values(by=columna_ordenar, ascending=True)
    else:
        df_ordenado = df_seleccionado.sort_values(by=columna_ordenar, ascending=False)
    # Mostrar el DataFrame ordenado
    st.write('DataFrame Ordenado:')
    st.write(df_ordenado)
