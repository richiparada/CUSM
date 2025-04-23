# CUSM - Cisco User & Secret Manager 🛠️

CUSM es una herramienta de automatización desarrollada en Python para administrar usuarios y contraseñas en switches Cisco (modelo 2960 y similares). Su objetivo es simplificar la configuración de múltiples dispositivos a través de conexiones SSH.

---

## 🚀 Características

- 🔐 Crear usuarios administrativos en múltiples switches Cisco.
- 🔄 Eliminar usuarios específicos (como 'admin') de los equipos.
- 🔑 Cambiar la contraseña del modo privilegiado (`enable`).
- 📁 Leer listas de switches y usuarios desde archivos `.txt`.
- 🧪 Registro detallado en archivos de log por ejecución.
- 🔒 Uso de archivo `.env` para cargar credenciales de manera segura.

---

## 🛠️ Requisitos

- Python 3.10 o superior
- Paquetes de Python:

##bash

pip install netmiko python-dotenv

---

## 📦 Estructura del Proyecto

🔧 Uso
1. Cargar lista de switches
Crear un archivo llamado switches.txt con una IP por línea:

10.0.0.1

10.0.0.2

10.0.0.3


2. Crear archivo de usuarios nuevos (usuarios_nuevos.txt)

Cada línea debe tener:

usuario,contraseña

nuevoadmin1,Password123

supervisor,SecurePass456

3. Crear archivo de credenciales .env

Guardar en credenciales.env:

SSH_USER=usuario_ssh

SSH_PASS=contrasena_ssh

ENABLE_PASS=enable_actual

NEW_ENABLE_PASS=nueva_enable

4. Ejecutar scripts

Crear usuarios:

python create_user.py

Modificar enable y eliminar un usuario:

python modificar_admin.py

🗃️ Logs
Todos los resultados se guardan en la carpeta logs/ con nombres como:

modificacon_SW_2025-04-23_14-30-02.log

modificacion_admin_2025-04-23_14-45-17.log

