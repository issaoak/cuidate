import mysql.connector
from mysql.connector import Error  # Importar la clase de excepción específica

def create_database_and_tables():
    try:
        conn = mysql.connector.connect(
            host='db',  # Usa 'db' si es el nombre del servicio en docker-compose.yml
            user='root',
            password='root'
        )
        if conn.is_connected():
            print("Conectado al servidor MySQL")

        cursor = conn.cursor()

        # Crear base de datos
        cursor.execute("CREATE DATABASE IF NOT EXISTS cuidatedivirtiendote;")
        cursor.execute("USE cuidatedivirtiendote;")

        # Crear tabla usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            ID_usuario INT AUTO_INCREMENT PRIMARY KEY,
            Nombre VARCHAR(100) NOT NULL,
            Apellido_paterno VARCHAR(100) NOT NULL,
            Apellido_materno VARCHAR(100) NOT NULL,
            Numero_Telefono VARCHAR(15) NOT NULL,
            Email VARCHAR(100) NOT NULL UNIQUE,
            Contraseña VARCHAR(255) NOT NULL,
            Rol VARCHAR(50) NOT NULL
        );
        """)

        conn.commit()
        print("Base de datos y tablas creadas exitosamente")

    except Error as e:  # Usar la excepción específica
        print("Error al conectar con MySQL:", e)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexión a MySQL cerrada")

if __name__ == "__main__":
    create_database_and_tables()
