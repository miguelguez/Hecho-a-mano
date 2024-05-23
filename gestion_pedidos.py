import customtkinter as ctk
import sqlite3
import sys
from collections import defaultdict

# Función para validar las credenciales de Maria
def validate_maria(email, password):
    return email == "Maria30@gmail.com" and password == "Maria30"

# Función para cargar los pedidos desde la base de datos
def load_orders():
    conn = sqlite3.connect("cart.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_email, product_name, SUM(quantity), price FROM cart GROUP BY user_email, product_name")
    orders = cursor.fetchall()
    conn.close()
    return orders

# Función para finalizar un pedido
def finalize_order(user_email, product_name):
    conn = sqlite3.connect("cart.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE user_email=? AND product_name=?", (user_email, product_name))
    conn.commit()
    conn.close()
    refresh_orders()

# Función para refrescar la lista de pedidos
def refresh_orders():
    for widget in orders_frame.winfo_children():
        widget.destroy()
    show_orders()

# Función para mostrar los pedidos
def show_orders():
    orders = load_orders()
    orders_by_user = defaultdict(list)
    
    for order in orders:
        orders_by_user[order[0]].append(order)

    for user_email, user_orders in orders_by_user.items():
        user_frame = ctk.CTkFrame(master=orders_frame, corner_radius=15)
        user_frame.pack(pady=10, padx=10, fill="x")

        user_email_label = ctk.CTkLabel(master=user_frame, text=f"Email: {user_email}", font=("Arial", 12, "bold"))
        user_email_label.pack(anchor="w", padx=10, pady=5)

        for order in user_orders:
            product_frame = ctk.CTkFrame(master=user_frame, corner_radius=15)
            product_frame.pack(pady=5, padx=10, fill="x")

            product_name_label = ctk.CTkLabel(master=product_frame, text=f"Producto: {order[1]}", font=("Arial", 12))
            product_name_label.pack(anchor="w", padx=10)

            quantity_label = ctk.CTkLabel(master=product_frame, text=f"Cantidad: {order[2]}", font=("Arial", 12))
            quantity_label.pack(anchor="w", padx=10)

            price_label = ctk.CTkLabel(master=product_frame, text=f"Precio Total: {order[2] * order[3]} DOP", font=("Arial", 12))
            price_label.pack(anchor="w", padx=10)

            finalize_button = ctk.CTkButton(master=product_frame, text="Finalizar Pedido", command=lambda ue=user_email, pn=order[1]: finalize_order(ue, pn))
            finalize_button.pack(anchor="e", padx=10)

# Función para iniciar sesión
def login():
    email = email_entry.get()
    password = password_entry.get()
    if validate_maria(email, password):
        login_frame.pack_forget()
        main_frame.pack(pady=20, padx=10, fill="both", expand=True)
        show_orders()
    else:
        login_status_label.configure(text="Acceso denegado. Solo Maria30 puede acceder.", text_color="red")

# Configuración de la aplicación principal
app = ctk.CTk()
app.geometry("600x600")
app.title("Gestión de Pedidos")

# Frame de inicio de sesión
login_frame = ctk.CTkFrame(master=app, width=580, height=580, corner_radius=15)
login_frame.pack(pady=20, padx=10, fill="both", expand=True)

login_label = ctk.CTkLabel(master=login_frame, text="Inicio de Sesión", font=("Arial", 20))
login_label.pack(pady=20)

email_entry = ctk.CTkEntry(master=login_frame, placeholder_text="Correo Electrónico", width=250)
email_entry.pack(pady=10)

password_entry = ctk.CTkEntry(master=login_frame, placeholder_text="Contraseña", show="*", width=250)
password_entry.pack(pady=10)

login_button = ctk.CTkButton(master=login_frame, text="Iniciar Sesión", command=login)
login_button.pack(pady=20)

login_status_label = ctk.CTkLabel(master=login_frame, text="")
login_status_label.pack(pady=10)

# Frame principal para la gestión de pedidos
main_frame = ctk.CTkFrame(master=app, width=580, height=580, corner_radius=15)

# Título
title_label = ctk.CTkLabel(master=main_frame, text="Gestión de Pedidos", font=("Arial", 20))
title_label.pack(pady=10)

# Contenedor de pedidos con scrollbar
orders_container = ctk.CTkFrame(master=main_frame, corner_radius=15)
orders_container.pack(pady=10, padx=10, fill="both", expand=True)

canvas = ctk.CTkCanvas(master=orders_container)
scrollbar = ctk.CTkScrollbar(master=orders_container, orientation="vertical", command=canvas.yview)
orders_frame = ctk.CTkFrame(master=canvas, corner_radius=15)

orders_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=orders_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Ejecutar la aplicación
app.mainloop()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        email = sys.argv[1]
        password = sys.argv[2]
        if validate_maria(email, password):
            app.mainloop()
        else:
            print("Acceso denegado. Solo Maria30 puede acceder.")
    else:
        print("Uso: python gestion_pedidos.py <email> <password>")
