import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Dinámico - ITY1101", layout="wide")
st.title("Visualización e Integración de Resultados en Tiempo Real")
st.markdown("### Asignatura: Gestión de Datos para IA (ITY1101)")


ruta_json = 'Dashboard/metricas_rendimiento.json'
ruta_csv = 'Dashboard/predicciones_modelo.csv'


if os.path.exists(ruta_json) and os.path.exists(ruta_csv):

    
    with open(ruta_json, 'r') as f:
        datos_rendimiento = json.load(f)
    df_rendimiento = pd.DataFrame(datos_rendimiento)

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
    
    # 🌟 FILTRADO INTELIGENTE: Mostramos solo las columnas clave para que no sature la pantalla
    columnas_interes = ['track_name', 'artists', 'Valores Reales', 'Predicciones']
    columnas_a_mostrar = [c for c in columnas_interes if c in df_predicciones.columns]
    
    # Respaldo automático por si los nombres del CSV difieren por mayúsculas
    if len(columnas_a_mostrar) == 0:
        columnas_a_mostrar = [col for col in ['track_name', 'artists', 'popularity', 'Predicciones'] if col in df_predicciones.columns]

    # Tomamos todas las canciones del CSV filtrando solo las columnas bonitas
    df_resumen_predicciones = df_predicciones[columnas_a_mostrar]
    st.dataframe(df_resumen_predicciones, use_container_width=True, hide_index=True)

    st.markdown("#### 📉 Gráfico de Dispersión (Ajuste del Modelo)")
    fig, ax = plt.subplots(figsize=(10, 3.5))
    
    # Configuración segura de los ejes del gráfico
    col_x = 'Valores Reales' if 'Valores Reales' in df_predicciones.columns else df_predicciones.columns[1]
    col_y = 'Predicciones' if 'Predicciones' in df_predicciones.columns else df_predicciones.columns[2]

    sns.scatterplot(data=df_predicciones, x=col_x, y=col_y, ax=ax, color='purple', alpha=0.7)
    ax.set_title(f"Comparativa Real: {col_x} vs {col_y}")
    st.pyplot(fig)

    st.success("Los datos se están leyendo dinámicamente desde el pipeline.")

else:
    st.warning(" Por favor, ejecuta las celdas del pipeline en tu Notebook para generar los reportes de métricas.")