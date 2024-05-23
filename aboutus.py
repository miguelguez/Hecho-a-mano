import customtkinter as ctk
from PIL import Image, ImageTk
import os
import subprocess

# Función para redirigir a homepage.py
def open_homepage():
    if os.path.exists("homepage.py"):
        subprocess.Popen(["python", "homepage.py"])
    else:
        print("Error: No se encontró el archivo homepage.py")

# Configuración de la aplicación principal
app = ctk.CTk()
app.geometry("300x600")
app.title("Detalles de hecho a mano")

# Configuración de colores y estilos
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Contenedor principal
frame = ctk.CTkFrame(master=app, width=280, height=560, corner_radius=15)
frame.pack(pady=20, padx=10)

# Flecha de retorno
back_button = ctk.CTkLabel(master=frame, text="←", font=("Arial", 20))
back_button.pack(pady=10, padx=10, anchor="w")
back_button.bind("<Button-1>", lambda e: open_homepage())

# Título
title_label = ctk.CTkLabel(master=frame, text="Detalles de hecho a mano", font=("Arial", 20))
title_label.pack(pady=10)

# Ruta de la imagen
image_path = "imagenesproject\Logo.jpg"  # Asegúrate de colocar la ruta correcta de la imagen

if not os.path.exists(image_path):
    print(f"Error: No se encontró el archivo en la ruta especificada: {image_path}")
    # Muestra un mensaje de error en la interfaz si la imagen no se encuentra
    image_label = ctk.CTkLabel(master=frame, text="Imagen no encontrada", font=("Arial", 14), text_color="red")
    image_label.pack(pady=10)
else:
    # Cargar y mostrar la imagen si se encuentra en la ruta especificada
    image = Image.open(image_path)
    image = image.resize((200, 200), Image.Resampling.LANCZOS)
    image_tk = ImageTk.PhotoImage(image)

    image_label = ctk.CTkLabel(master=frame, image=image_tk, text="")
    image_label.pack(pady=10)

# Descripción
description_text = """
¡Hola a todos!

En "Hecho a Mano" nos dedicamos a crear adornos para el hogar y joyas únicas y especiales. Somos un equipo de amigos apasionados por el arte y la artesanía, y nos encanta trabajar con arcilla para dar vida a nuestras ideas.

¡No te pierdas nuestras últimas creaciones y detrás de escena! Síguenos en nuestra cuenta de Instagram @Hecho a mano, para obtener inspiración y ver todas las novedades. Además, ahora puedes encontrar todos nuestros productos en nuestra tienda virtual y explorar aún más sobre nosotros en nuestra página web.

En nuestro pequeño taller artesanal, diseñamos y elaboramos una variedad de adornos para embellecer tu hogar, desde vasijas y jarrones hasta
"""

description_label = ctk.CTkLabel(master=frame, text=description_text, font=("Arial", 14), wraplength=250, justify="left")
description_label.pack(pady=10, padx=10)

# Ejecutar la aplicación
app.mainloop()
