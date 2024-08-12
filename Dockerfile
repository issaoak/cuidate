# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instala netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

# Copia el archivo requirements.txt y luego instala las dependencias
COPY app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el script wait-for-mysql.sh y asegúrate de que tenga permisos de ejecución
COPY app/wait-for-mysql.sh /app/
RUN chmod +x /app/wait-for-mysql.sh

# Copia el resto de los archivos al contenedor
COPY app /app

# Expone el puerto en el que correrá la aplicación
EXPOSE 6000

# Comando para correr la aplicación
CMD ["/app/wait-for-mysql.sh", "db", "python", "app.py"]
