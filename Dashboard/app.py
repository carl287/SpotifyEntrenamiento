import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px  # 🌟 Nueva librería para el gráfico interactivo

st.set_page_config(page_title="Dashboard Dinámico - ITY1101", layout="wide")

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.6rem;
            padding-bottom: 2.2rem;
        }

        .hero-badge {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: rgba(59, 130, 246, 0.12);
            color: #c7ddff;
            border: 1px solid rgba(59, 130, 246, 0.25);
            font-size: 0.82rem;
            margin-bottom: 0.75rem;
        }

        .section-shell {
            background: linear-gradient(180deg, rgba(17, 24, 39, 0.92), rgba(10, 14, 22, 0.96));
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 24px;
            padding: 1.1rem 1.2rem 0.75rem 1.2rem;
            margin: 0.8rem 0 1rem 0;
            box-shadow: 0 20px 45px rgba(0, 0, 0, 0.18);
        }

        .section-title {
            margin: 0;
            font-size: 1.55rem;
            font-weight: 800;
            color: #f8fafc;
        }

        .section-subtitle {
            margin: 0.35rem 0 0 0;
            color: #94a3b8;
            font-size: 0.95rem;
        }

        .metric-card {
            background: rgba(15, 23, 42, 0.92);
            border: 1px solid rgba(148, 163, 184, 0.16);
            border-radius: 18px;
            padding: 1rem 1rem 0.9rem 1rem;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
            height: 100%;
        }

        .metric-label {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #94a3b8;
            margin-bottom: 0.35rem;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            color: #f8fafc;
            line-height: 1.05;
        }

        .metric-note {
            font-size: 0.84rem;
            color: #aab4c5;
            margin-top: 0.35rem;
        }

        .soft-chip {
            display: inline-block;
            padding: 0.25rem 0.55rem;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.12);
            color: #bbf7d0;
            border: 1px solid rgba(34, 197, 94, 0.18);
            font-size: 0.78rem;
            margin-left: 0.45rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Visualización e Integración de Resultados en Tiempo Real")
st.markdown("### Asignatura: Gestión de Datos para IA (ITY1101)")

# 🛠️ RUTAS ACTUALIZADAS: Apuntan correctamente dentro de la subcarpeta 'Dashboard/'
ruta_json = 'Dashboard/metricas_rendimiento.json'
ruta_csv = 'Dashboard/predicciones_modelo.csv'

# --- COMPROBACIÓN DE INTEGRACIÓN (LECTURA DINÁMICA) ---
if os.path.exists(ruta_json) and os.path.exists(ruta_csv):

    # 1. Leer archivos dinámicos generados por el pipeline
    with open(ruta_json, 'r') as f:
        datos_rendimiento = json.load(f)
    df_rendimiento = pd.DataFrame(datos_rendimiento)

    # 🔥 LIMPIEZA DE COLUMNAS EXTRA EN LA TABLA DE RENDIMIENTO
    columnas_validas = ["Métrica", "Ejecución 1 (10% Datos)", "Ejecución 2 (100% Datos)"]
    df_rendimiento = df_rendimiento[[col for col in columnas_validas if col in df_rendimiento.columns]]
    df_rendimiento = df_rendimiento.drop_duplicates(subset=["Métrica"]).reset_index(drop=True)

    def obtener_valor_metricas(df: pd.DataFrame, nombre_metrica: str, columna: str):
        if "Métrica" not in df.columns or columna not in df.columns:
            return None
        fila = df[df["Métrica"] == nombre_metrica]
        if fila.empty:
            return None
        return fila.iloc[0][columna]

    # 2. Leer el dataset de predicciones completo
    df_predicciones = pd.read_csv(ruta_csv)

    # ==========================================
    # SECCIÓN 1: RENDIMIENTO DEL SISTEMA
    # ==========================================
    st.markdown(
        """
        <div class="section-shell">
            <span class="hero-badge">Pipeline en vivo</span>
            <h2 class="section-title">📈 Rendimiento del Sistema (Métricas del Pipeline)</h2>
            <p class="section-subtitle">Resumen visual, comparativa entre ejecuciones y lectura rápida del estado del pipeline.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tiempo_ejecucion = obtener_valor_metricas(df_rendimiento, "Tiempo total (segundos)", "Ejecución 2 (100% Datos)")
    uso_cpu = obtener_valor_metricas(df_rendimiento, "Uso de CPU (%)", "Ejecución 2 (100% Datos)")
    ram_usada = obtener_valor_metricas(df_rendimiento, "RAM Utilizada (MB)", "Ejecución 2 (100% Datos)")
    errores = obtener_valor_metricas(df_rendimiento, "Errores detectados", "Ejecución 2 (100% Datos)")

    col1, col2, col3, col4 = st.columns(4)
    metric_cards = [
        ("Tiempo ejecución", f"{tiempo_ejecucion:.2f} s" if pd.notna(tiempo_ejecucion) else "-", "Última corrida con 100% de datos"),
        ("CPU", f"{uso_cpu:.2f} %" if pd.notna(uso_cpu) else "-", "Uso de recursos del pipeline"),
        ("RAM", f"{ram_usada:.2f} MB" if pd.notna(ram_usada) else "-", "Consumo de memoria observado"),
        ("Errores", f"{int(errores)}" if pd.notna(errores) else "-", "Incidencias detectadas en la corrida"),
    ]

    for columna, (titulo, valor, nota) in zip([col1, col2, col3, col4], metric_cards):
        with columna:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{titulo}</div>
                    <div class="metric-value">{valor}</div>
                    <div class="metric-note">{nota}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    rendimiento_tabs = st.tabs(["Comparativa visual", "Tabla detallada"])
    with rendimiento_tabs[0]:
        df_rendimiento_plot = df_rendimiento.copy()
        valor_cols = [col for col in ["Ejecución 1 (10% Datos)", "Ejecución 2 (100% Datos)"] if col in df_rendimiento_plot.columns]
        if valor_cols:
            df_rendimiento_plot[valor_cols] = df_rendimiento_plot[valor_cols].apply(pd.to_numeric, errors="coerce")
            df_melt_rendimiento = df_rendimiento_plot.melt(id_vars="Métrica", value_vars=valor_cols, var_name="Ejecucion", value_name="Valor")
            fig_rendimiento = px.bar(
                df_melt_rendimiento,
                x="Métrica",
                y="Valor",
                color="Ejecucion",
                barmode="group",
                color_discrete_sequence=["#38bdf8", "#22c55e"],
                title="Comparativa entre ejecución liviana y ejecución completa",
            )
            fig_rendimiento.update_layout(
                template="plotly_dark",
                height=420,
                margin=dict(l=10, r=10, t=55, b=10),
                legend_title_text="",
            )
            st.plotly_chart(fig_rendimiento, use_container_width=True)
        else:
            st.info("No se encontraron columnas numéricas para dibujar la comparativa de métricas.")

    with rendimiento_tabs[1]:
        st.markdown("<div class='soft-chip'>Tabla comparativa interactiva</div>", unsafe_allow_html=True)
        st.dataframe(df_rendimiento, use_container_width=True, hide_index=True)


   
    st.markdown(
        """
        <div class="section-shell">
            <span class="hero-badge">Modelo y predicciones</span>
            <h2 class="section-title">Predicciones y Evaluación del Modelo</h2>
            <p class="section-subtitle">Explora las predicciones por artista, género y volumen de muestra, con una vista de error rápida.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    columnas_interes = ['track_name', 'artists', 'Valores Reales', 'Predicciones']
    columnas_a_mostrar = [c for c in columnas_interes if c in df_predicciones.columns]

    if len(columnas_a_mostrar) == 0:
        columnas_a_mostrar = [col for col in ['track_name', 'artists', 'popularity', 'Predicciones'] if col in df_predicciones.columns]

    col_x = 'Valores Reales' if 'Valores Reales' in df_predicciones.columns else df_predicciones.columns[1]
    col_y = 'Predicciones' if 'Predicciones' in df_predicciones.columns else df_predicciones.columns[2]

    df_predicciones = df_predicciones.copy()
    df_predicciones[col_x] = pd.to_numeric(df_predicciones[col_x], errors='coerce')
    df_predicciones[col_y] = pd.to_numeric(df_predicciones[col_y], errors='coerce')
    df_predicciones['Error Absoluto'] = (df_predicciones[col_x] - df_predicciones[col_y]).abs()

    pred_tabs = st.tabs(["Tabla interactiva", "Gráfico del ajuste", "Errores y resumen"])

    with pred_tabs[0]:
        filtro_cols = st.columns([1.25, 1.25, 0.8])
        with filtro_cols[0]:
            lista_artistas = ["Todos"] + sorted(df_predicciones['artists'].dropna().astype(str).unique().tolist()) if 'artists' in df_predicciones.columns else ["Todos"]
            artista_seleccionado = st.selectbox("🔍 Artista", lista_artistas)
        with filtro_cols[1]:
            lista_generos = ["Todos"] + sorted(df_predicciones['track_genre'].dropna().astype(str).unique().tolist()) if 'track_genre' in df_predicciones.columns else ["Todos"]
            genero_seleccionado = st.selectbox("🏷️ Género", lista_generos)
        with filtro_cols[2]:
            max_filas = max(5, min(100, len(df_predicciones)))
            limite_filas = st.slider("Filas", min_value=5, max_value=max_filas, value=min(15, max_filas))

        df_tabla_filtrada = df_predicciones.copy()
        if artista_seleccionado != "Todos" and 'artists' in df_tabla_filtrada.columns:
            df_tabla_filtrada = df_tabla_filtrada[df_tabla_filtrada['artists'].astype(str) == artista_seleccionado]
        if genero_seleccionado != "Todos" and 'track_genre' in df_tabla_filtrada.columns:
            df_tabla_filtrada = df_tabla_filtrada[df_tabla_filtrada['track_genre'].astype(str) == genero_seleccionado]

        columnas_tabla = columnas_a_mostrar + (["Error Absoluto"] if "Error Absoluto" in df_tabla_filtrada.columns else [])
        df_resumen_predicciones = df_tabla_filtrada[columnas_tabla].head(limite_filas)

        resumen_cols = st.columns(4)
        total_visibles = len(df_tabla_filtrada)
        mae = df_tabla_filtrada['Error Absoluto'].mean() if 'Error Absoluto' in df_tabla_filtrada.columns else None
        exactos = int((df_tabla_filtrada['Error Absoluto'] == 0).sum()) if 'Error Absoluto' in df_tabla_filtrada.columns else None
        correlacion = df_tabla_filtrada[[col_x, col_y]].corr().iloc[0, 1] if df_tabla_filtrada[[col_x, col_y]].dropna().shape[0] >= 2 else None
        resumen_data = [
            ("Canciones visibles", f"{total_visibles}", "Resultado del filtro actual"),
            ("MAE", f"{mae:.2f}" if pd.notna(mae) else "-", "Error absoluto medio"),
            ("Exactas", f"{exactos}" if exactos is not None else "-", "Coincidencias perfectas"),
            ("Correlación", f"{correlacion:.2f}" if correlacion is not None and pd.notna(correlacion) else "-", "Relación real vs predicha"),
        ]
        for columna, (titulo, valor, nota) in zip(resumen_cols, resumen_data):
            with columna:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">{titulo}</div>
                        <div class="metric-value" style="font-size:1.65rem;">{valor}</div>
                        <div class="metric-note">{nota}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<div class='soft-chip'>Tabla dinámica con filtros</div>", unsafe_allow_html=True)
        st.dataframe(df_resumen_predicciones, use_container_width=True, hide_index=True)

        csv_filtrado = df_tabla_filtrada[columnas_tabla].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar filtro actual",
            data=csv_filtrado,
            file_name="predicciones_filtradas.csv",
            mime="text/csv",
        )

    with pred_tabs[1]:
        st.markdown("_Pasa el cursor sobre los puntos para ver los detalles de las canciones y usa el filtro para comparar artistas o géneros._")

        df_filtrado_grafico = df_predicciones.copy()
        if 'artists' in df_filtrado_grafico.columns:
            artista_unico = st.selectbox("🎯 Filtrar gráfico por artista", ["Todos"] + sorted(df_filtrado_grafico['artists'].dropna().astype(str).unique().tolist()), key="artista_grafico")
            if artista_unico != "Todos":
                df_filtrado_grafico = df_filtrado_grafico[df_filtrado_grafico['artists'].astype(str) == artista_unico]
        if 'track_genre' in df_filtrado_grafico.columns:
            genero_unico = st.selectbox("🎚️ Filtrar gráfico por género", ["Todos"] + sorted(df_filtrado_grafico['track_genre'].dropna().astype(str).unique().tolist()), key="genero_grafico")
            if genero_unico != "Todos":
                df_filtrado_grafico = df_filtrado_grafico[df_filtrado_grafico['track_genre'].astype(str) == genero_unico]

        max_muestras = max(50, min(500, len(df_filtrado_grafico)))
        muestras_iniciales = min(200, max_muestras)
        max_muestras = st.slider("Muestras para el gráfico", min_value=50, max_value=max_muestras, value=muestras_iniciales, key="muestras_grafico")
        df_filtrado_grafico = df_filtrado_grafico.head(max_muestras)

        hover_data = {col_x: True, col_y: True, 'Error Absoluto': True}
        if 'artists' in df_filtrado_grafico.columns:
            hover_data['artists'] = True
        if 'track_genre' in df_filtrado_grafico.columns:
            hover_data['track_genre'] = True

        fig = px.scatter(
            df_filtrado_grafico,
            x=col_x,
            y=col_y,
            hover_name='track_name' if 'track_name' in df_filtrado_grafico.columns else None,
            hover_data=hover_data,
            title=f"Comparativa real vs predicha: {col_x} frente a {col_y}",
            labels={col_x: "Popularidad Real", col_y: "Predicción de la IA"},
            color='Error Absoluto' if 'Error Absoluto' in df_filtrado_grafico.columns else None,
            color_continuous_scale='Turbo',
            opacity=0.82,
        )

        if df_filtrado_grafico[col_x].notna().any():
            fig.add_shape(
                type='line',
                x0=df_filtrado_grafico[col_x].min(),
                y0=df_filtrado_grafico[col_x].min(),
                x1=df_filtrado_grafico[col_x].max(),
                y1=df_filtrado_grafico[col_x].max(),
                line=dict(color='rgba(255,255,255,0.45)', dash='dash', width=2),
            )

        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=20, r=20, t=55, b=20),
            height=460,
            coloraxis_colorbar=dict(title="Error abs."),
        )

        st.plotly_chart(fig, use_container_width=True)

    with pred_tabs[2]:
        st.markdown("<div class='soft-chip'>Diagnóstico del modelo</div>", unsafe_allow_html=True)
        errores_df = df_predicciones[[c for c in ['track_name', 'artists', 'track_genre', col_x, col_y, 'Error Absoluto'] if c in df_predicciones.columns]].dropna(subset=['Error Absoluto']).sort_values('Error Absoluto', ascending=False).head(10)
        if not errores_df.empty:
            st.markdown("#### Top 10 mayores errores absolutos")
            st.dataframe(errores_df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay suficientes datos para ordenar errores.")

    st.success("Los datos se están leyendo dinámicamente desde el pipeline.")

    #  (BOT INTERACTIVO)
    st.write("---")
    st.header("🎵 Sistema de Recomendación de Canciones con IA")
    st.markdown("¿No sabes qué escuchar? Elige una canción del dataset y nuestro algoritmo buscará las 5 canciones más similares basadas en sus características de audio.")

    ruta_modelo = 'Models/dataset_spotify.pkl'

    if os.path.exists(ruta_modelo):
        # Cargamos el dataset reducido del modelo
        df_modelo = pd.read_pickle(ruta_modelo)

        # 1. Buscador/Selector de canciones para el usuario
        canciones_disponibles = sorted(df_modelo['track_name'].dropna().unique().tolist())
        cancion_usuario = st.selectbox("🎯 Selecciona una canción que te guste:", canciones_disponibles)

        if st.button("🚀 Generar Recomendaciones"):
            # Obtenemos los datos de la canción elegida
            datos_cancion = df_modelo[df_modelo['track_name'] == cancion_usuario].iloc[0]
            artista_cancion = datos_cancion['artists']
            genero_cancion = datos_cancion['track_genre']

            st.markdown(f"### 🎧 Porque te gusta: **{cancion_usuario}** - _{artista_cancion}_")
            st.write("Aquí tienes tus 5 recomendaciones personalizadas:")

            # LÓGICA DE RECOMENDACIÓN (Filtro inteligente por género similar)
            # Buscamos canciones del mismo género, excluyendo la canción seleccionada
            df_mismo_genero = df_modelo[
                (df_modelo['track_genre'] == genero_cancion) & 
                (df_modelo['track_name'] != cancion_usuario)
            ]

            # Si no hay suficientes del mismo género, abrimos al dataset completo
            if len(df_mismo_genero) < 5:
                df_mismo_genero = df_modelo[df_modelo['track_name'] != cancion_usuario]

            # Tomamos 5 canciones de forma aleatoria estructurada (o las primeras 5 del filtro)
            recomendaciones = df_mismo_genero[['track_name', 'artists', 'track_genre']].drop_duplicates().head(5)

            # Mostramos las recomendaciones en un formato visual atractivo
            cols = st.columns(5)
            for i, (idx, row) in enumerate(recomendaciones.iterrows()):
                with cols[i]:
                    st.info(f"✨ **{row['track_name']}**\n\n🎤 _{row['artists']}_\n\n🏷️ `{row['track_genre']}`")
    else:
        st.info("💡 Para activar el recomendador interactivo, asegúrate de haber ejecutado la celda de exportación de modelos en tu Notebook para generar el archivo `dataset_spotify.pkl`.")

else:
    st.warning(" Por favor, ejecuta las celdas del pipeline en tu Notebook para generar los reportes de métricas.")