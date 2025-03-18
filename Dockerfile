# Usa una imagen base de Python
FROM python:3.12-slim

# Instala dependencias necesarias y Chrome
RUN apt-get update && apt-get install -y \
    wget unzip curl \
    chromium \
    chromium-driver

# Establece variables de entorno para Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 5000 (para Flask)
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "server.py"]
