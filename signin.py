import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import sqlite3
import os

def open_signup():
    if os.path.exists("signup.py"):
        subprocess.Popen(["python", "signup.py"])
    else:
        print("Error: No se encontró el archivo signup.py")

def open_homepage(user_email):
    if os.path.exists("homepage.py"):
        subprocess.Popen(["python", "homepage.py", user_email])
        app.destroy()  # Cerrar la ventana de inicio de sesión
    else:
        print("Error: No se encontró el archivo homepage.py")

# Función para manejar el clic en "¿Olvidó la contraseña?"
def forgot_password():
    login_frame.pack_forget()
    reset_password_frame.pack(pady=10, padx=10, fill="both", expand=True)

def go_back():
    reset_password_frame.pack_forget()
    login_frame.pack(pady=10, padx=10, fill="both", expand=True)

def login_user():
    email = email_entry.get()
    password = password_entry.get()
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        login_status_label.configure(text="Inicio de sesión exitoso", text_color="green")
        open_homepage(email)  # Pasar el email del usuario a la función open_homepage
    else:
        login_status_label.configure(text="Email o contraseña incorrectos", text_color="red")

def send_reset_link():
    email = reset_email_entry.get()
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        reset_status_label.configure(text="Enlace de restablecimiento enviado", text_color="green")
        # Aquí puedes agregar la lógica para enviar el correo de restablecimiento
    else:
        reset_status_label.configure(text="Email no encontrado", text_color="red")

# Configuración de la aplicación principal
app = ctk.CTk()
app.geometry("300x640")
app.title("Hecho a mano")

# Configuración de colores y estilos
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Fondo del encabezado
header_frame = ctk.CTkFrame(master=app, width=280, height=80, corner_radius=0, fg_color="#FFB6C1")
header_frame.pack(pady=0, padx=0, fill="x")

# Título principal
header_label = ctk.CTkLabel(master=header_frame, text="Hecho a mano", font=("Arial", 24))
header_label.pack(pady=30)

# Contenedor de inicio de sesión
login_frame = ctk.CTkFrame(master=app, width=280, height=500, corner_radius=15)

# Imagen del logo
logo_image_path = "imagenesproject/Logo.jpg"  # Ruta de la imagen del logo
if os.path.exists(logo_image_path):
    logo_image = Image.open(logo_image_path)
    logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
    logo_image_tk = ImageTk.PhotoImage(logo_image)
    logo_label = ctk.CTkLabel(master=login_frame, image=logo_image_tk, text="")
    logo_label.pack(pady=10)
else:
    logo_label = ctk.CTkLabel(master=login_frame, text="Logo no encontrado", font=("Arial", 14), text_color="red")
    logo_label.pack(pady=10)

# Título de inicio de sesión
login_label = ctk.CTkLabel(master=login_frame, text="Iniciar sesión", font=("Arial", 20))
login_label.pack(pady=10)

# Subtítulo
subtitle_label = ctk.CTkLabel(master=login_frame, text="Utilice la siguiente cuenta para iniciar sesión.", font=("Arial", 12))
subtitle_label.pack(pady=5)

# Campos de texto
email_entry = ctk.CTkEntry(master=login_frame, placeholder_text="Email", width=250, height=40, corner_radius=10)
email_entry.pack(pady=5)

password_entry = ctk.CTkEntry(master=login_frame, placeholder_text="Contraseña", show="*", width=250, height=40, corner_radius=10)
password_entry.pack(pady=5)

# Botón de inicio de sesión
login_button = ctk.CTkButton(master=login_frame, text="Inicia sesión", width=250, height=40, corner_radius=10, fg_color="#FFB6C1", command=login_user)
login_button.pack(pady=20)

# Enlace de "¿Olvidó la contraseña?"
forgot_password_label = ctk.CTkLabel(master=login_frame, text="¿Olvidó la contraseña?", font=("Arial", 12), text_color="#a9a9a9")
forgot_password_label.pack(pady=5)
forgot_password_label.bind("<Button-1>", lambda e: forgot_password())

# Texto de inicio con otra opción
alternative_label = ctk.CTkLabel(master=login_frame, text="Or sign up with", font=("Arial", 12))
alternative_label.pack(pady=10)

# Contenedor para el botón social
social_frame = ctk.CTkFrame(master=login_frame, width=250, height=60, corner_radius=15, fg_color="#FFB6C1")
social_frame.pack(pady=10)

# Botón de correo dentro del contenedor
email_button = ctk.CTkButton(master=social_frame, text="Correo", width=50, height=40, corner_radius=10, fg_color="#D8BFD8", command=open_signup)
email_button.pack(pady=10)

# Etiqueta de estado del inicio de sesión
login_status_label = ctk.CTkLabel(master=login_frame, text="")
login_status_label.pack(pady=10)

# Contenedor de recuperación de contraseña
reset_password_frame = ctk.CTkFrame(master=app, width=280, height=500, corner_radius=15)

# Botón de volver atrás
back_button = ctk.CTkLabel(master=reset_password_frame, text="←", font=("Arial", 20))
back_button.pack(pady=10, padx=10, anchor="w")
back_button.bind("<Button-1>", lambda e: go_back())

# Título de recuperación de contraseña
reset_password_label = ctk.CTkLabel(master=reset_password_frame, text="¿Olvidó su contraseña?", font=("Arial", 20))
reset_password_label.pack(pady=10)

# Subtítulo de recuperación de contraseña
reset_password_subtitle_label = ctk.CTkLabel(master=reset_password_frame, text="Complete su correo electrónico a continuación para recibir un enlace para restablecer la contraseña.", font=("Arial", 12))
reset_password_subtitle_label.pack(pady=5, padx=10)

# Campo de texto para el correo electrónico
reset_email_entry = ctk.CTkEntry(master=reset_password_frame, placeholder_text="Email", width=250, height=40, corner_radius=10)
reset_email_entry.pack(pady=5)

# Botón para enviar el enlace de restablecimiento
send_reset_link_button = ctk.CTkButton(master=reset_password_frame, text="Send Reset Link", width=250, height=40, corner_radius=10, fg_color="#FFB6C1", command=send_reset_link)
send_reset_link_button.pack(pady=20)

# Etiqueta de estado de la recuperación de contraseña
reset_status_label = ctk.CTkLabel(master=reset_password_frame, text="")
reset_status_label.pack(pady=10)

# Mostrar el contenedor de inicio de sesión por defecto
login_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Ejecutar la aplicación
app.mainloop()
