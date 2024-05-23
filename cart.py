import customtkinter as ctk
import sqlite3
import sys

def main(user_email):
    # Configuración de la aplicación principal
    app = ctk.CTk()
    app.geometry("400x600")
    app.title("Carrito de Compras")

    # Contenedor principal
    frame = ctk.CTkFrame(master=app, corner_radius=15)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Título
    title_label = ctk.CTkLabel(master=frame, text="Carrito de Compras", font=("Arial", 20))
    title_label.pack(pady=10)

    # Mostrar productos en el carrito
    conn = sqlite3.connect("cart.db")
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, quantity, price FROM cart WHERE user_email=?", (user_email,))
    cart_items = cursor.fetchall()
    conn.close()

    for item in cart_items:
        item_label = ctk.CTkLabel(master=frame, text=f"{item[0]} - Cantidad: {item[1]} - Precio: {item[2]} DOP")
        item_label.pack(pady=5)

    # Botón de finalizar pedido
    def finalizar_pedido():
        print(f"Pedido finalizado por {user_email}")
        conn = sqlite3.connect("cart.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE user_email=?", (user_email,))
        conn.commit()
        conn.close()
        print(f"Todos los productos del carrito de {user_email} han sido eliminados.")
        # Aquí puedes agregar la lógica para procesar el pedido
        app.destroy()  # Cerrar la ventana después de finalizar el pedido

    finish_button = ctk.CTkButton(master=frame, text="Finalizar Pedido", command=finalizar_pedido)
    finish_button.pack(pady=20)

    # Ejecutar la aplicación
    app.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_email = sys.argv[1]
    else:
        user_email = None
    main(user_email)
