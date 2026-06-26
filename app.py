import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Spotify - canciones recomendadas", layout="wide")
st.title("Visualización e Integración de Resultados en Tiempo Real")

# --- COMPROBACIÓN DE INTEGRACIÓN (LECTURA DINÁMICA) ---
if os.path.exists('metricas_rendimiento.json') and os.path.exists('predicciones_modelo.csv'):

    # 1. Leer archivos dinámicos generados por el pipeline en tu Notebook
    with open('metricas_rendimiento.json', 'r') as f:
        datos_rendimiento = json.load(f)
    df_rendimiento = pd.DataFrame(datos_rendimiento)

    # 🔥 LIMPIEZA DE COLUMNAS EXTRA EN RENDIMIENTO
    columnas_validas = ["Métrica", "Ejecución 1 (10% Datos)", "Ejecución 2 (100% Datos)"]
    df_rendimiento = df_rendimiento[[col for col in columnas_validas if col in df_rendimiento.columns]]
    df_rendimiento = df_rendimiento.drop_duplicates(subset=["Métrica"]).reset_index(drop=True)

    # 2. Leer el dataset de predicciones
    df_predicciones = pd.read_csv('predicciones_modelo.csv')

    # ==========================================
    # SECCIÓN 1: RENDIMIENTO DEL SISTEMA
    # ==========================================
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


    # ==========================================
    # SECCIÓN 2: PREDICCIONES Y EVALUACIÓN
    # ==========================================
    st.header("Predicciones y Evaluación del Modelo")

    st.markdown("#### 🔍 Tabla Interactiva de Predicciones del Dataset")
    
    # 🌟 FILTRADO INTELIGENTE: Seleccionamos solo columnas clave para limpiar la interfaz visual
    columnas_interes = ['track_name', 'artists', 'Valores Reales', 'Predicciones']
    columnas_a_mostrar = [c for c in columnas_interes if c in df_predicciones.columns]
    
    # Si por alguna razón tus columnas en el CSV tienen minúsculas u otros nombres:
    if len(columnas_a_mostrar) == 0:
        # Respaldo automático en caso de que no coincidan exactamente los nombres de las columnas
        columnas_a_mostrar = [col for col in ['track_name', 'artists', 'popularity', 'Predicciones'] if col in df_predicciones.columns]

    # Tomamos únicamente las primeras 10 filas para que la vista sea súper compacta y elegante
    df_resumen_predicciones = df_predicciones[columnas_a_mostrar]
    
    # Mostramos la tabla interactiva limpia y al ancho completo
    st.dataframe(df_resumen_predicciones, use_container_width=True, hide_index=True)


    # ==========================================
    # SECCIÓN 3: GRÁFICO DE AJUSTE
    # ==========================================
    st.markdown("#### 📉 Gráfico de Dispersión (Ajuste del Modelo)")
    fig, ax = plt.subplots(figsize=(10, 3.5))
    
    # Buscamos de forma segura las columnas para el gráfico (Valores Reales vs Predicciones)
    col_x = 'Valores Reales' if 'Valores Reales' in df_predicciones.columns else df_predicciones.columns[1]
    col_y = 'Predicciones' if 'Predicciones' in df_predicciones.columns else df_predicciones.columns[2]

    sns.scatterplot(data=df_predicciones.head(100), x=col_x, y=col_y, ax=ax, color='purple', alpha=0.7)
    ax.set_title(f"Comparativa Real: {col_x} vs {col_y}")
    st.pyplot(fig)

    st.success("Los datos se están leyendo dinámicamente desde el pipeline.")

else:
    st.warning("Por favor, ejecuta las celdas del pipeline en tu Notebook para generar los reportes de métricas.")