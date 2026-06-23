# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="Spotify Recommendation API")

# 1. Al iniciar la API, cargamos los archivos guardados en memoria
try:
    df = pd.read_pickle("dataset_spotify.pkl")
    scaler = joblib.load("scaler_spotify.pkl")
    
    # Preparamos la matriz de características de audio escaladas
    features = [
        'duration_ms', 'explicit', 'danceability', 'energy', 'key', 
        'loudness', 'mode', 'speechiness', 'acousticness', 
        'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature'
    ]
    X_scaled = scaler.transform(df[features])
except Exception as e:
    print(f"Error cargando los modelos: {e}")

# Definimos el formato de los datos que recibirá la API
class PeticionCancion(BaseModel):
    nombre_cancion: str
    top_n: int = 5

@app.post("/recomendar")
def recomendar(peticion: PeticionCancion):
    nombre = peticion.nombre_cancion.lower()
    
    # Buscamos la canción en nuestro dataset local
    indices = df[df['track_name'].str.lower() == nombre].index
    if len(indices) == 0:
        raise HTTPException(status_code=404, detail="Canción no encontrada en el catálogo.")
        
    idx = indices[0]
    vector_cancion = X_scaled[idx].reshape(1, -1)
    
    # Calculamos la similitud contra el resto de canciones
    similitudes = cosine_similarity(vector_cancion, X_scaled)[0]
    
    df_temp = df.copy()
    df_temp['similitud'] = similitudes
    
    # Obtenemos las más recomendadas (excluyendo la primera que es sí misma)
    recomendaciones = df_temp.sort_values(by='similitud', ascending=False).iloc[1:peticion.top_n+1]
    
    # Convertimos los resultados a un formato JSON compatible para el chatbot
    resultados = []
    for _, fila in recomendaciones.iterrows():
        resultados.append({
            "cancion": fila['track_name'],
            "artista": fila['artists'],
            "genero": fila['track_genre'],
            "similitud": round(float(fila['similitud']), 3)
        })
        
    return {
        "cancion_buscada": df.iloc[idx]['track_name'],
        "artista_buscado": df.iloc[idx]['artists'],
        "recomendaciones": resultados
    }
