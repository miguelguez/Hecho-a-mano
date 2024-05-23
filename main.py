import customtkinter as ctk
from PIL import Image, ImageTk
import os
import subprocess
import sqlite3


import sqlite3

def create_cart_database():
    conn = sqlite3.connect("cart.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_cart_database()

# Función para ejecutar el archivo signup.py
def open_signup():
    if os.path.exists("signup.py"):
        subprocess.Popen(["python", "signup.py"])
    else:
        print("Error: No se encontró el archivo signup.py")

# Función para ejecutar el archivo signin.py
def open_signin():
    if os.path.exists("signin.py"):
        subprocess.Popen(["python", "signin.py"])
    else:
        print("Error: No se encontró el archivo signin.py")

# Función para crear la base de datos si no existe
def create_database():
    db_path = "users.db"
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                phonenumber TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("Base de datos creada correctamente.")
    else:
        print("La base de datos ya existe.")

# Crear la base de datos al iniciar la aplicación
create_database()

# Configuración de la aplicación principal
app = ctk.CTk()
app.geometry("300x600")
app.title("Hecho a mano")
app.iconbitmap("imagenesproject/Logo.ico")

# Configuración de colores y estilos
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Contenedor principal
frame = ctk.CTkFrame(master=app, width=280, height=560, corner_radius=15)
frame.pack(pady=20, padx=10)

# Ruta de la imagen
image_path = r"imagenesproject\༝༚༝༚.jpeg"

if not os.path.exists(image_path):
    print(f"Error: No se encontró el archivo en la ruta especificada: {image_path}")
    # Muestra un mensaje de error en la interfaz si la imagen no se encuentra
    image_label = ctk.CTkLabel(master=frame, text="Imagen no encontrada", font=("Arial", 14), text_color="red")
    image_label.pack(pady=10)
else:
    # Cargar y mostrar la imagen si se encuentra en la ruta especificada
    image = Image.open(image_path)
    image = image.resize((240, 240), Image.Resampling.LANCZOS)
    image_tk = ImageTk.PhotoImage(image)

    image_label = ctk.CTkLabel(master=frame, image=image_tk, text="")
    image_label.pack(pady=10)

# Título
title_label = ctk.CTkLabel(master=frame, text="Joyero con tapa", font=("Arial", 20))
title_label.pack(pady=10)

# Descripción
description_label = ctk.CTkLabel(master=frame, text="Este es uno de los muchos productos que encontrarás a un muy buen precio y con la mejor calidad.",
                                 font=("Arial", 14), wraplength=250)
description_label.pack(pady=10, padx=10)

# Botones
button_frame = ctk.CTkFrame(master=frame, width=260, height=50, corner_radius=15)
button_frame.pack(pady=20)

login_button = ctk.CTkButton(master=button_frame, text="Inicia sesión", width=120, height=40, corner_radius=10, fg_color="#f8bbd0", command=open_signin)
login_button.pack(side="left", padx=10)

register_button = ctk.CTkButton(master=button_frame, text="Register", width=120, height=40, corner_radius=10, fg_color="#424242", command=open_signup)
register_button.pack(side="right", padx=10)

# Ejecutar la aplicación
app.mainloop()
