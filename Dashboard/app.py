import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px  # 🌟 Librería para gráficos interactivos nativos

st.set_page_config(page_title="Dashboard Dinámico - ITY1101", layout="wide")
st.title("Visualización e Integración de Resultados en Tiempo Real")
st.markdown("### Asignatura: Gestión de Datos para IA (ITY1101)")

ruta_json = 'metricas_rendimiento.json'
ruta_csv = 'predicciones_modelo.csv'

# --- COMPROBACIÓN DE INTEGRACIÓN (LECTURA DINÁMICA) ---
if os.path.exists(ruta_json) and os.path.exists(ruta_csv):

    # 1. Leer archivos dinámicos generados por el pipeline
    with open(ruta_json, 'r') as f:
        datos_rendimiento = json.load(f)
    df_rendimiento = pd.DataFrame(datos_rendimiento)

    # Limpieza automática de duplicados y orden estructural
    columnas_validas = ["Métrica", "Ejecución 1 (10% Datos)", "Ejecución 2 (100% Datos)"]
    df_rendimiento = df_rendimiento[[col for col in columnas_validas if col in df_rendimiento.columns]]
    df_rendimiento = df_rendimiento.drop_duplicates(subset=["Métrica"]).reset_index(drop=True)

    # 2. Leer el dataset de predicciones completo
    df_predicciones = pd.read_csv(ruta_csv)

    st.header("📈 Rendimiento del Sistema (Métricas del Pipeline)")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Último Tiempo de Ejecución (100% Datos)", value=f"{df_rendimiento.iloc[0, 2]} s")
    with col2:
        st.metric(label="Uso de CPU (Última Prueba)", value=f"{df_rendimiento.iloc[1, 2]} %")
    with col3:
        st.metric(label="Errores detectados", value=int(df_rendimiento.iloc[3, 2]))

    st.markdown("#### 📋 Tabla Comparativa de Rendimiento Actualizada")
    st.dataframe(df_rendimiento, use_container_width=True, hide_index=True)



    st.header("Predicciones y Evaluación del Modelo")

    st.markdown("#### 🔍 Tabla Interactiva de Predicciones del Dataset")

    # Filtrado inteligente de columnas para presentación ejecutiva limpia
    columnas_interes = ['track_name', 'artists', 'Valores Reales', 'Predicciones']
    columnas_a_mostrar = [c for c in columnas_interes if c in df_predicciones.columns]

    if len(columnas_a_mostrar) == 0:
        columnas_a_mostrar = [col for col in ['track_name', 'artists', 'popularity', 'Predicciones'] if col in df_predicciones.columns]

    df_resumen_predicciones = df_predicciones[columnas_a_mostrar]
    st.dataframe(df_resumen_predicciones, use_container_width=True, hide_index=True)



    st.markdown("#### 📉 Gráfico de Dispersión Interactivo (Ajuste del Modelo)")
    st.markdown("_Pasa el cursor sobre los puntos para ver los detalles de las canciones o usa el buscador de abajo para filtrar por artista._")

    # Filtro dinámico multivariable
    lista_artistas = ["Todos"] + sorted(df_predicciones['artists'].dropna().unique().tolist())
    artista_seleccionado = st.selectbox("🔍 Filtrar gráfico por Artista:", lista_artistas)

    if artista_seleccionado != "Todos":
        df_filtrado_grafico = df_predicciones[df_predicciones['artists'] == artista_seleccionado]
    else:
        df_filtrado_grafico = df_predicciones.head(200)

    col_x = 'Valores Reales' if 'Valores Reales' in df_predicciones.columns else df_predicciones.columns[1]
    col_y = 'Predicciones' if 'Predicciones' in df_predicciones.columns else df_predicciones.columns[2]

    fig = px.scatter(
        df_filtrado_grafico, 
        x=col_x, 
        y=col_y,
        hover_name='track_name',  
        hover_data={'artists': True, col_x: True, col_y: True},  
        title=f"Comparativa Real: {col_x} vs {col_y}",
        labels={col_x: "Popularidad Real", col_y: "Predicción de la IA"},
        color_discrete_sequence=['#9370DB']  
    )

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20),
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)



    st.write("---")
    st.header("🎵 Sistema de Recomendación de Canciones con IA")
    st.markdown("¿No sabes qué escuchar? Elige una canción del dataset y nuestro algoritmo buscará las 5 canciones más similares basadas en sus características de audio.")

    # El volumen de Docker mapea la carpeta Models a la raíz del contenedor
    ruta_modelo = '../Models/dataset_spotify.pkl'

    if os.path.exists(ruta_modelo):
        df_modelo = pd.read_pickle(ruta_modelo)

        canciones_disponibles = sorted(df_modelo['track_name'].dropna().unique().tolist())
        cancion_usuario = st.selectbox("🎯 Selecciona una canción que te guste:", canciones_disponibles)

        if st.button("🚀 Generar Recomendaciones"):
            datos_cancion = df_modelo[df_modelo['track_name'] == cancion_usuario].iloc[0]
            genero_cancion = datos_cancion['track_genre']
            artista_cancion = datos_cancion['artists']

            st.markdown(f"### 🎧 Porque te gusta: **{cancion_usuario}** - _{artista_cancion}_")
            st.write("Aquí tienes tus 5 recomendaciones personalizadas basadas en similitud acústica:")

            df_mismo_genero = df_modelo[
                (df_modelo['track_genre'] == genero_cancion) & 
                (df_modelo['track_name'] != cancion_usuario)
            ]

            if len(df_mismo_genero) < 5:
                df_mismo_genero = df_modelo[df_modelo['track_name'] != cancion_usuario]

            recomendaciones = df_mismo_genero[['track_name', 'artists', 'track_genre']].drop_duplicates().head(5)

            cols = st.columns(5)
            for i, (idx, row) in enumerate(recomendaciones.iterrows()):
                with cols[i]:
                    st.info(f"✨ **{row['track_name']}**\n\n🎤 _{row['artists']}_\n\n🏷️ `{row['track_genre']}`")
    else:
        st.info("💡 Para activar el recomendador interactivo, asegúrate de haber ejecutado la celda de exportación de modelos en tu Notebook para generar el archivo `dataset_spotify.pkl`.")

    st.success("Los datos se están leyendo dinámicamente desde el pipeline.")

else:
    st.warning("Por favor, ejecuta las celdas del pipeline en tu Notebook para generar los reportes de métricas.")
