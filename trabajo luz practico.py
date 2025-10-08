 pip  install cryptography
import os
import json
import getpass
import hashlib
import base64
import secrets
from cryptography.fernet import Fernet

# -------------------------------
# CONFIGURACIÓN Y UTILIDADES
# -------------------------------

DATA_FILE = 'passwords.json'
KEY_FILE = 'secret.key'

# Generar o cargar la clave secreta (clave maestra para cifrado)
def load_or_create_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    return key

# -------------------------------
# AUTENTICACIÓN BÁSICA
# -------------------------------

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return base64.b64encode(salt + pwd_hash).decode()

def verify_password(stored_hash, input_password):
    decoded = base64.b64decode(stored_hash.encode())
    salt = decoded[:16]
    stored_pwd_hash = decoded[16:]
    new_pwd_hash = hashlib.pbkdf2_hmac('sha256', input_password.encode(), salt, 100000)
    return stored_pwd_hash == new_pwd_hash

# -------------------------------
# GENERACIÓN DE CONTRASEÑAS SEGURAS
# -------------------------------

def generate_secure_password(length=16):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+'
    return ''.join(secrets.choice(characters) for _ in range(length))

# -------------------------------
# GESTOR DE CONTRASEÑAS
# -------------------------------

class PasswordManager:
    def __init__(self, key):
        self.fernet = Fernet(key)
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return {}
        with open(DATA_FILE, 'r') as file:
            return json.load(file)

    def save_data(self):
        with open(DATA_FILE, 'w') as file:
            json.dump(self.data, file)

    def add_password(self, service, username, password):
        encrypted = self.fernet.encrypt(password.encode()).decode()
        self.data[service] = {"username": username, "password": encrypted}
        self.save_data()
        print(f"[+] Contraseña para {service} guardada correctamente.")

    def get_password(self, service):
        if service in self.data:
            record = self.data[service]
            decrypted = self.fernet.decrypt(record['password'].encode()).decode()
            print(f"Servicio: {service}")
            print(f"Usuario: {record['username']}")
            print(f"Contraseña: {decrypted}")
        else:
            print("[!] Servicio no encontrado.")

# -------------------------------
# MENÚ PRINCIPAL
# -------------------------------

def main():
    print("==== Gestor de Contraseñas ====")

    key = load_or_create_key()
    manager = PasswordManager(key)

    # Autenticación de usuario
    if not os.path.exists('master.hash'):
        print("[!] No se encontró usuario maestro. Crear uno nuevo.")
        master_pwd = getpass.getpass("Crea una contraseña maestra: ")
        master_hash = hash_password(master_pwd)
        with open('master.hash', 'w') as f:
            f.write(master_hash)
        print("[+] Contraseña maestra creada.")
    else:
        master_pwd = getpass.getpass("Introduce la contraseña maestra: ")
        with open('master.hash', 'r') as f:
            stored_hash = f.read()
        if not verify_password(stored_hash, master_pwd):
            print("[!] Contraseña incorrecta. Acceso denegado.")
            return

    # Menú de opciones
    while True:
        print("\nOpciones:")
        print("1. Añadir contraseña")
        print("2. Mostrar contraseña")
        print("3. Generar contraseña segura")
        print("4. Salir")

        choice = input("Elige una opción: ")

        if choice == '1':
            service = input("Servicio: ")
            username = input("Usuario: ")
            password = getpass.getpass("Contraseña: ")
            manager.add_password(service, username, password)

        elif choice == '2':
            service = input("Servicio a buscar: ")
            manager.get_password(service)

        elif choice == '3':
            length = int(input("Longitud deseada: "))
            print("Contraseña generada:", generate_secure_password(length))

        elif choice == '4':
            print("Saliendo del gestor...")
            break

        else:
            print("Opción inválida.")

if __name__ == '__main__':
    main()
