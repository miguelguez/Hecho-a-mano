import customtkinter as ctk
from PIL import Image, ImageTk
import os
import subprocess
import sqlite3
import sys

# Datos de los productos
products = [
    {
        "name": "Porta vela",
        "description": "porta vela en forma de donita de hecho a mano",
        "price": 150,
        "image": "imagenesproject/Funky Donut Tea Light Holder, Jewelry Tray, Ring Dish, Trinket Dish, Ash Tray, Vanity Ring Holder, Eclectic Room Decor, Funky Decor, Pop Art.jpeg",
        "file": "portavelas.py"
    },
    {
        "name": "Porta fotos",
        "description": "porta fotos en forma de cactus de hecho a mano",
        "price": 100,
        "image": "imagenesproject/Cacti shaped concrete photo or name card holders, wedding name card holder, Ideal for holding Wedding name cards_ Several colours.jpeg",
        "file": "portafotos.py"
    },
    {
        "name": "Macetas",
        "description": "Maceta de arcilla de hecho a mano.",
        "price": 250,
        "image": "imagenesproject/Plants pots decor.jpg",
        "file": "macetas.py"
    },
    {
        "name": "Separador de libro",
        "description": "Hermoso separador de libro personalisable de hecho a mano.",
        "price": 50,
        "image": "imagenesproject/descarga.jpg",
        "file": "separador_de_libro.py"
    },
    {
        "name": "Llaveros del zodiaco",
        "description": "Llaveros con diseño del zodiaco de hecho a mano.",
        "price": 100,
        "image": "imagenesproject/༝༚༝༚.jpeg",
        "file": "llavero_del_zodiaco.py"
    },
    {
        "name": "Joyero",
        "description": "Joyero con increible diseño hecho a mano.",
        "price": 150,
        "image": "imagenesproject/joyero.jpeg",
        "file": "Joyero.py"
    }
]

# Función para filtrar los productos
def filter_products():
    search_term = search_entry.get().lower()
    for widget in product_frame.winfo_children():
        widget.destroy()
    for product in products:
        if search_term in product["name"].lower() or search_term in product["description"].lower():
            add_product_to_frame(product)

def open_cart():
    if os.path.exists("cart.py"):
        subprocess.Popen(["python", "cart.py", user_email])
    else:
        print("Error: No se encontró el archivo cart.py")

def open_about_us():
    if os.path.exists("aboutus.py"):
        subprocess.Popen(["python", "aboutus.py"])
    else:
        print("Error: No se encontró el archivo aboutus.py")

# Función para añadir un producto al frame
def add_product_to_frame(product):
    product_container = ctk.CTkFrame(master=product_frame, corner_radius=15)
    product_container.pack(pady=10, padx=10, fill="x")
    
    image_path = product["image"]
    if os.path.exists(image_path):
        image = Image.open(image_path)
        image = image.resize((50, 50), Image.Resampling.LANCZOS)
        image_tk = ImageTk.PhotoImage(image)
        product_image_label = ctk.CTkLabel(master=product_container, image=image_tk, text="")
        product_image_label.image = image_tk  # keep a reference
        product_image_label.pack(side="left", padx=10)

    product_info_frame = ctk.CTkFrame(master=product_container, corner_radius=15)
    product_info_frame.pack(side="left", fill="x", expand=True)
    
    product_name_label = ctk.CTkLabel(master=product_info_frame, text=product["name"], font=("Arial", 14, "bold"))
    product_name_label.pack(anchor="w")
    
    product_description_label = ctk.CTkLabel(master=product_info_frame, text=product["description"], font=("Arial", 12))
    product_description_label.pack(anchor="w")
    
    product_price_label = ctk.CTkLabel(master=product_info_frame, text=f"${product['price']} DOP", font=("Arial", 12))
    product_price_label.pack(anchor="w")

    def add_to_cart(user_email, product_name, quantity, price):
        conn = sqlite3.connect("cart.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                user_email TEXT,
                product_name TEXT,
                quantity INTEGER,
                price REAL
            )
        """)
        cursor.execute("""
            INSERT INTO cart (user_email, product_name, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (user_email, product_name, quantity, price))
        conn.commit()
        conn.close()
        print(f"{product_name} añadido al carrito de {user_email}")

    def add_to_cart_handler():
        add_to_cart(user_email, product["name"], 1, product["price"])

    add_to_cart_button = ctk.CTkButton(master=product_info_frame, text="Añadir al carrito", width=120, command=add_to_cart_handler)
    add_to_cart_button.pack(side="right", padx=10)

def main(user_email):
    global app
    # Configuración de la aplicación principal
    app = ctk.CTk()
    app.geometry("480x600")
    app.title("Hecho a Mano")
    app.iconbitmap("imagenesproject/Logo.ico")

    # Contenedor del encabezado
    header_frame = ctk.CTkFrame(master=app, corner_radius=0)
    header_frame.pack(pady=10, padx=10, fill="x")

    # Logo de la tienda
    logo_path = "imagenesproject/Logo.ico"
    if os.path.exists(logo_path):
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((40, 40), Image.Resampling.LANCZOS)
        logo_image_tk = ImageTk.PhotoImage(logo_image)
        logo_label = ctk.CTkLabel(master=header_frame, image=logo_image_tk, text="")
        logo_label.image = logo_image_tk
        logo_label.pack(side="left", padx=10)
        logo_label.bind("<Button-1>", lambda e: open_about_us())  # Enlazar la función open_about_us al clic en el logo

    # Nombre de usuario
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT firstname, lastname FROM users WHERE email=?", (user_email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_name = f"{user[0]} {user[1]}"
    else:
        user_name = "[name]"

    user_label = ctk.CTkLabel(master=header_frame, text=user_name, font=("Arial", 14))
    user_label.pack(side="left", padx=10)

    # Carrito de compras (icono de carrito sin número)
    cart_label = ctk.CTkLabel(master=header_frame, text="🛒", font=("Arial", 20))
    cart_label.pack(side="right", padx=10)
    cart_label.bind("<Button-1>", lambda e: open_cart())  # Enlazar la función open_cart

    # Barra de búsqueda
    global search_entry
    search_entry = ctk.CTkEntry(master=app, placeholder_text="Buscar productos...")
    search_entry.pack(pady=10, padx=10, fill="x")
    search_button = ctk.CTkButton(master=app, text="Buscar", command=filter_products)
    search_button.pack(pady=5, padx=10, fill="x")

    # Contenedor de productos con scrollbar
    product_container = ctk.CTkFrame(master=app, corner_radius=15)
    product_container.pack(pady=10, padx=10, fill="both", expand=True)

    canvas = ctk.CTkCanvas(master=product_container)
    scrollbar = ctk.CTkScrollbar(master=product_container, orientation="vertical", command=canvas.yview)
    scrollable_frame = ctk.CTkFrame(master=canvas, corner_radius=15)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    global product_frame
    product_frame = ctk.CTkFrame(master=scrollable_frame, corner_radius=15)
    product_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Añadir productos al frame
    for product in products:
        add_product_to_frame(product)

    # Ejecutar la aplicación
    app.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_email = sys.argv[1]
    else:
        user_email = None
    main(user_email)
