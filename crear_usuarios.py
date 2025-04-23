from netmiko import ConnectHandler
from dotenv import load_dotenv
import os
from datetime import datetime

# Cargar credenciales desde credenciales.env
load_dotenv(dotenv_path="credenciales.env")
usuario_ssh = os.getenv("SSH_USER")
contrasena_ssh = os.getenv("SSH_PASS")
contrasena_enable = os.getenv("ENABLE_PASS")

# Funciones para cargar datos
def cargar_ips_desde_txt(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        return [linea.strip() for linea in f if linea.strip()]

def cargar_usuarios_desde_txt(ruta_archivo):
    usuarios = []
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            partes = linea.strip().split(',')
            if len(partes) == 2:
                usuarios.append((partes[0].strip(), partes[1].strip()))
    return usuarios

# Crear carpeta logs/ si no existe
os.makedirs("logs", exist_ok=True)

# Crear nombre de archivo único con fecha y hora
timestamp_log = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"logs/modificacion_SW_{timestamp_log}.log"

def escribir_log(mensaje):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{timestamp} {mensaje}\n")

# Cargar datos
ips = cargar_ips_desde_txt("switches.txt")
usuarios_nuevos = cargar_usuarios_desde_txt("usuarios_nuevos.txt")

# Ejecutar comandos en cada switch
for ip in ips:
    print(f"\n🔄 Conectando a {ip}...")

    switch = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': usuario_ssh,
        'password': contrasena_ssh,
        'secret': contrasena_enable,
    }

    try:
        conexion = ConnectHandler(**switch)
        conexion.enable()

        comandos = []
        for usuario, contraseña in usuarios_nuevos:
            comandos.append(f'username {usuario} privilege 15 secret {contraseña}')
        comandos.append('do write memory')

        resultado = conexion.send_config_set(comandos)
        conexion.disconnect()

        mensaje = f"✅ {ip} - Usuarios configurados correctamente."
        print(mensaje)
        escribir_log(mensaje)

    except Exception as e:
        mensaje = f"❌ {ip} - Error: {e}"
        print(mensaje)
        escribir_log(mensaje)