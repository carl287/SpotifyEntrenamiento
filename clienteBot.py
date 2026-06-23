import telebot
import requests

# 1. PEGA AQUÍ EL TOKEN QUE TE DIO BOTFATHER
TOKEN = "8587357217:AAHdmcJ4_4Jvg3CPnk_Sx7t6ZwqQTpYOdho"

bot = telebot.TeleBot(TOKEN)

# URL de tu API local que está corriendo en el puerto 8000
API_URL = "http://127.0.0.1:8000/recomendar"

# Mensaje de bienvenida cuando el usuario inicia el bot
@bot.message_handler(commands=['start', 'help'])
def enviar_bienvenida(message):
    bot.reply_to(
        message, 
        "¡Hola! Soy tu asistente de Spotify 🎵.\n\n"
        "Escríbeme el comando `/recomendar` seguido del nombre de una canción y te buscaré las mejores recomendaciones.\n\n"
        "Ejemplo:\n`/recomendar Comedy`"
    )

# Escuchar el comando /recomendar
@bot.message_handler(commands=['recomendar'])
def recomendar_cancion(message):
    # Extraemos el nombre de la canción quitando el comando "/recomendar "
    cancion_usuario = message.text.replace("/recomendar", "").strip()
    
    if not cancion_usuario:
        bot.reply_to(message, "❌ Por favor, escribe el nombre de una canción después del comando.\nEjemplo: `/recomendar Hold On`")
        return

    # Enviamos un mensaje de "escribiendo..." para que el usuario sepa que el bot está procesando
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Preparamos los datos para tu servidor API local
    payload = {"nombre_cancion": cancion_usuario, "top_n": 5}
    
    try:
        # Hacemos la consulta a tu API FastAPI local
        respuesta = requests.post(API_URL, json=payload)
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            mensaje = f"🎵 Basado en *{datos['cancion_buscada']}* (de {datos['artista_buscado']}), te sugiero estas canciones similares:\n\n"
            
            for i, rec in enumerate(datos['recomendaciones'], 1):
                mensaje += f"{i}. *{rec['cancion']}*\n"
                mensaje += f"   👤 Artista: {rec['artista']}\n"
                mensaje += f"   🏷️ Género: {rec['genero']}\n"
                mensaje += f"   🤝 Coincidencia: {rec['similitud']*100:.1f}%\n\n"
        else:
            mensaje = "❌ Lo siento, no encontré esa canción en mi base de datos de Spotify."
            
    except requests.exceptions.ConnectionError:
        mensaje = "⚠️ Error: No me pude conectar con el servidor API local. ¿Está encendido?"

    # Respondemos al usuario en Telegram
    bot.reply_to(message, mensaje, parse_mode="Markdown")

# Iniciar el bot (se queda escuchando mensajes continuamente)
print("¡El Chatbot de Telegram está encendido y escuchando!")
bot.infinity_polling()