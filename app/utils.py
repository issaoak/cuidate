# utils.py
from werkzeug.security import check_password_hash, generate_password_hash

def check_password_hash_scrypt(pw_hash, password):
    # Tu lógica aquí
    return check_password_hash(pw_hash, password)
