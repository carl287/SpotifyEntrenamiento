import requests

# Esta función se activa cuando el usuario escribe en Telegram: /recomendar Comedy
def responder_usuario_telegram(update, context):
    cancion_usuario = " ".join(context.args)
    
    # Hacemos la consulta a nuestra API local
    url_api = "http://127.0.0.1:8000/recomendar"
    payload = {"nombre_cancion": cancion_usuario, "top_n": 3}
    
    respuesta = requests.post(url_api, json=payload)
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        mensaje = f"🎵 Basado en '{datos['cancion_buscada']}' de {datos['artista_buscado']}, te sugiero:\n\n"
        
        for rec in datos['recomendaciones']:
            mensaje += f"• *{rec['cancion']}* - {rec['artista']} (Género: {rec['genero']}, Coincidencia: {rec['similitud']*100:.1f}%)\n"
    else:
        mensaje = "❌ Lo siento, no encontré esa canción en mi base de datos de Spotify."
        
    update.message.reply_text(mensaje, parse_mode="Markdown")
