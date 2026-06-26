FROM python:3.12-slim

# Instalar dependencias del sistema necesarias para psutil
RUN apt-get update && apt-get install -y gcc python3-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar e instalar librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto de Streamlit
EXPOSE 8501

# Comando para correr Streamlit por defecto
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]