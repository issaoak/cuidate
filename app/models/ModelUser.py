from .entities.User import User

class ModelUser:
    @classmethod
    def login(cls, conn, user):
        try:
            cursor = conn.cursor(dictionary=True)  # Usar cursor como diccionario
            sql = "SELECT ID_usuario, Email, Contrasena, Rol FROM usuarios WHERE Email = %s"
            cursor.execute(sql, (user.Email,))
            row = cursor.fetchone()
            print("Database row:", row)  # Línea de depuración
            if row is not None:
                user = User(row['ID_usuario'], row['Email'], row['Contrasena'], row['Rol'])
                return user
            else:
                return None
        except Exception as e:
            print("Exception in ModelUser.login:", e)  # Línea de depuración
            raise Exception(e)

    @classmethod
    def get_by_id(cls, conn, ID_usuario):
        try:
            cursor = conn.cursor(dictionary=True)  # Usar cursor como diccionario
            sql = "SELECT ID_usuario, Email, Nombre, Rol FROM usuarios WHERE ID_usuario = %s"
            cursor.execute(sql, (ID_usuario,))
            row = cursor.fetchone()
            print("Database row:", row)  # Línea de depuración
            if row is not None:
                user = User(row['ID_usuario'], row['Email'], None, row['Rol'], Nombre=row['Nombre'])
                return user
            else:
                return None
        except Exception as e:
            print("Exception in ModelUser.get_by_id:", e)  # Línea de depuración
            raise Exception(e)
