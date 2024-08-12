from flask_login import UserMixin
from utils import check_password_hash_scrypt

class User(UserMixin):
    def __init__(self, ID_usuario, Email, Contraseña, Rol='user', Apellido_paterno="", Apellido_materno="", Numero_Telefono="", Nombre=""):
        self.ID_usuario = ID_usuario
        self.Email = Email
        self.Contraseña = Contraseña
        self.Rol = Rol
        self.Apellido_paterno = Apellido_paterno
        self.Apellido_materno = Apellido_materno
        self.Numero_Telefono = Numero_Telefono
        self.Nombre = Nombre

    def get_id(self):
        return str(self.ID_usuario)
    
    @classmethod
    def is_authenticated(cls, hashed_password, password):
        return check_password_hash_scrypt(hashed_password, password)
