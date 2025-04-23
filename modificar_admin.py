from netmiko import ConnectHandler
from dotenv import load_dotenv
import os
from datetime import datetime

# Cargar credenciales desde archivo .env
load_dotenv(dotenv_path="credenciales.env")
usuario_ssh = os.getenv("SSH_USER")
contrasena_ssh = os.getenv("SSH_PASS")
contrasena_enable = os.getenv("ENABLE_PASS")
nueva_enable_pass = os.getenv("NEW_ENABLE_PASS")

# Usuario que se eliminará (puedes cambiar "admin" por otro si lo deseas)
usuario_a_eliminar = "admin"

# Crear carpeta logs si no existe
os.makedirs("logs", exist_ok=True)

# Crear nombre de archivo log con timestamp
timestamp_log = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"logs/modificacion_admin_{timestamp_log}.log"

def escribir_log(mensaje):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{timestamp} {mensaje}\n")

# Leer IPs de switches
def cargar_ips_desde_txt(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        return [linea.strip() for linea in f if linea.strip()]

ips = cargar_ips_desde_txt("switches.txt")

# Ejecutar tareas en cada switch
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

        comandos = [
            f'no username {usuario_a_eliminar}',
            f'enable secret {nueva_enable_pass}',
            'do write memory'
        ]

        resultado = conexion.send_config_set(comandos)
        conexion.disconnect()

        mensaje = f"✅ {ip} - Usuario '{usuario_a_eliminar}' eliminado y contraseña de enable actualizada."
        print(mensaje)
        escribir_log(mensaje)

    except Exception as e:
        mensaje = f"❌ {ip} - Error: {e}"
        print(mensaje)
        escribir_log(mensaje)
