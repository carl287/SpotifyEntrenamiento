import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Dinámico - ITY1101", layout="wide")
st.title("Visualización e Integración de Resultados en Tiempo Real")
st.markdown("### Asignatura: Gestión de Datos para IA (ITY1101)")

# --- COMPROBACIÓN DE INTEGRACIÓN (LECTURA DINÁMICA) ---
if os.path.exists('metricas_rendimiento.json') and os.path.exists('predicciones_modelo.csv'):

    # 1. Leer archivos dinámicos generados por el pipeline en Colab
    with open('metricas_rendimiento.json', 'r') as f:
        datos_rendimiento = json.load(f)
    df_rendimiento = pd.DataFrame(datos_rendimiento)

    df_predicciones = pd.read_csv('predicciones_modelo.csv')

    st.header("📈 Rendimiento del Sistema (Métricas del Pipeline)")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Último Tiempo de Ejecución", value=f"{df_rendimiento.iloc[0, 2]} s")
    with col2:
        st.metric(label="Uso de CPU (Última Prueba)", value=f"{df_rendimiento.iloc[1, 2]} %")
    #with col3:
        #st.metric(label="Errores detectados", value=int(df_rendimiento.iloc[3, 2]))

    st.markdown("#### 📋 Tabla Comparativa de Rendimiento Actualizada")
    st.table(df_rendimiento)

    st.header("Predicciones y Evaluación del Modelo")

    st.markdown("#### 🔍 Tabla Interactiva de Predicciones del Dataset")
    st.dataframe(df_predicciones, use_container_width=True)

    st.markdown("#### 📉 Gráfico de Dispersión (Ajuste del Modelo)")
    fig, ax = plt.subplots(figsize=(10, 3.5))
    col_x = df_predicciones.columns[1]
    col_y = df_predicciones.columns[2]

    sns.scatterplot(data=df_predicciones, x=col_x, y=col_y, ax=ax, color='purple', alpha=0.7)
    ax.set_title(f"Comparativa Real: {col_x} vs {col_y}")
    st.pyplot(fig)

    st.success("Los datos se están leyendo dinámicamente desde el pipeline.")

else:
    st.warning(" Por favor, ejecuta las celdas del pipeline en tu Notebook para generar los reportes de métricas.")
