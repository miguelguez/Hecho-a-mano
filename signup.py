import customtkinter as ctk
import sqlite3
import os
import subprocess

# Función para registrar un nuevo usuario
def register_user():
    firstname = firstname_entry.get()
    lastname = lastname_entry.get()
    phonenumber = phonenumber_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if password != confirm_password:
        error_label.configure(text="Las contraseñas no coinciden", text_color="red")
        return

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (firstname, lastname, phonenumber, email, password)
            VALUES (?, ?, ?, ?, ?)
        """, (firstname, lastname, phonenumber, email, password))
        conn.commit()
        success_label.configure(text="Usuario registrado con éxito", text_color="green")
        # Redirigir a signin.py después del registro exitoso
        app.after(2000, open_signin)  # Esperar 2 segundos antes de redirigir
    except sqlite3.IntegrityError:
        error_label.configure(text="El correo electrónico ya está registrado", text_color="red")
    finally:
        conn.close()

# Función para abrir signin.py
def open_signin():
    if os.path.exists("signin.py"):
        subprocess.Popen(["python", "signin.py"])
        app.destroy()  # Cerrar la ventana de registro
    else:
        print("Error: No se encontró el archivo signin.py")

# Configuración de la aplicación principal
app = ctk.CTk()
app.geometry("300x600")
app.title("Registro de Usuario")
app.iconbitmap("imagenesproject\Logo.ico")

# Configuración de colores y estilos
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Contenedor principal
frame = ctk.CTkFrame(master=app, width=280, height=560, corner_radius=15)
frame.pack(pady=20, padx=10)

# Título
title_label = ctk.CTkLabel(master=frame, text="Registro de Usuario", font=("Arial", 20))
title_label.pack(pady=10)

# Campos del formulario
firstname_entry = ctk.CTkEntry(master=frame, placeholder_text="Nombre")
firstname_entry.pack(pady=5, padx=10, fill="x")

lastname_entry = ctk.CTkEntry(master=frame, placeholder_text="Apellido")
lastname_entry.pack(pady=5, padx=10, fill="x")

phonenumber_entry = ctk.CTkEntry(master=frame, placeholder_text="Número de Teléfono")
phonenumber_entry.pack(pady=5, padx=10, fill="x")

email_entry = ctk.CTkEntry(master=frame, placeholder_text="Correo Electrónico")
email_entry.pack(pady=5, padx=10, fill="x")

password_entry = ctk.CTkEntry(master=frame, placeholder_text="Contraseña", show="*")
password_entry.pack(pady=5, padx=10, fill="x")

confirm_password_entry = ctk.CTkEntry(master=frame, placeholder_text="Confirmar Contraseña", show="*")
confirm_password_entry.pack(pady=5, padx=10, fill="x")

# Botón de registro
register_button = ctk.CTkButton(master=frame, text="Registrar", width=120, height=40, corner_radius=10, command=register_user)
register_button.pack(pady=20)

# Etiquetas para mensajes de éxito o error
error_label = ctk.CTkLabel(master=frame, text="")
error_label.pack()

success_label = ctk.CTkLabel(master=frame, text="")
success_label.pack()

# Botón para redirigir a signin.py si ya tienes una cuenta
signin_label = ctk.CTkLabel(master=frame, text="¿Ya tienes una cuenta?", font=("Arial", 12))
signin_label.pack(pady=5)
signin_button = ctk.CTkButton(master=frame, text="Inicia sesión", width=120, height=40, corner_radius=10, command=open_signin)
signin_button.pack(pady=5)

# Ejecutar la aplicación
app.mainloop()
