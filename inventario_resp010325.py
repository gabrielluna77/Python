import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
from database import conectar, ejecutar_consulta

def abrir_ventana_inventario(root):
    ventana_inventario = tk.Toplevel(root)
    ventana_inventario.title("Inventario")
    ventana_inventario.geometry("800x600")

    # Obtener la ruta del directorio del script
    directorio_actual = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta del logo
    logo_path = os.path.join(directorio_actual, "logo", "logo.jpg")

    # Cargar el logo
    if os.path.exists(logo_path):
        try:
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)
            logo_tk = ImageTk.PhotoImage(logo_image)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el logo: {e}")
            logo_tk = None
    else:
        messagebox.showerror("Error", "No se encontró el archivo del logo.")
        logo_tk = None

    # Frame para el logo y el título
    header_frame = tk.Frame(ventana_inventario)
    header_frame.pack(pady=20)

    # Agregar el logo al Frame
    if logo_tk:
        lbl_logo = tk.Label(header_frame, image=logo_tk)
        lbl_logo.pack(side="left", padx=10)
        lbl_logo.image = logo_tk

    # Agregar el título al Frame
    titulo_label = tk.Label(header_frame, text="INVENTARIO", font=("Arial", 24, "bold"), fg="blue")
    titulo_label.pack(side="left", padx=10)

    # Frame para los botones
    botones_frame = tk.Frame(ventana_inventario)
    botones_frame.pack(pady=20)

    # Estilo de los botones
    button_style = {
        "bg": "#87CEEB",
        "fg": "white",
        "font": ("Arial", 14, "bold"),
        "width": 20,
        "height": 2,
        "activebackground": "#6CA6CD",
        "activeforeground": "white",
    }

    # Botón para agregar producto
    btn_agregar = tk.Button(botones_frame, text="Agregar Producto", command=lambda: agregar_producto(ventana_inventario), **button_style)
    btn_agregar.grid(row=0, column=0, padx=10, pady=10)

    # Botón para modificar producto
    btn_modificar = tk.Button(botones_frame, text="Modificar Producto", command=lambda: modificar_producto(ventana_inventario), **button_style)
    btn_modificar.grid(row=0, column=1, padx=10, pady=10)

    # Botón para eliminar producto
    btn_eliminar = tk.Button(botones_frame, text="Eliminar Producto", command=lambda: eliminar_producto(ventana_inventario), **button_style)
    btn_eliminar.grid(row=0, column=2, padx=10, pady=10)

    # Botón para regresar a la ventana principal
    btn_regresar = tk.Button(botones_frame, text="Regresar", command=ventana_inventario.destroy, **button_style)
    btn_regresar.grid(row=1, column=1, padx=10, pady=10)

# Función para abrir la ventana de agregar producto
def agregar_producto(ventana):
    ventana_agregar = tk.Toplevel(ventana)
    ventana_agregar.title("Agregar Producto")
    ventana_agregar.geometry("600x400")

    # Campos del formulario
    tk.Label(ventana_agregar, text="Clave:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
    clave_entry = tk.Entry(ventana_agregar, font=("Arial", 14))
    clave_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(ventana_agregar, text="Descripción:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
    descrip_entry = tk.Entry(ventana_agregar, font=("Arial", 14))
    descrip_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(ventana_agregar, text="Cantidad:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10)
    cantidad_entry = tk.Entry(ventana_agregar, font=("Arial", 14))
    cantidad_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(ventana_agregar, text="Precio:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=10)
    precio_entry = tk.Entry(ventana_agregar, font=("Arial", 14))
    precio_entry.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(ventana_agregar, text="Observaciones:", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=10)
    obser_entry = tk.Entry(ventana_agregar, font=("Arial", 14))
    obser_entry.grid(row=4, column=1, padx=10, pady=10)

    # Función para verificar si la clave ya existe
    def verificar_clave(event=None):
        clave = clave_entry.get()
        if not clave:
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            query = "SELECT * FROM productos WHERE clave = %s"
            cursor.execute(query, (clave,))
            resultado = cursor.fetchone()
            cursor.close()
            conexion.close()

            if resultado:
                messagebox.showinfo("Clave existente", "La clave ya existe.")
                clave_entry.focus_set()  # Regresar el foco al campo de la clave
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo verificar la clave: {err}")

    # Vincular el evento KeyRelease al campo de la clave
    clave_entry.bind("<KeyRelease>", verificar_clave)

    # Función para guardar el producto en la base de datos
    def guardar_producto():
        clave = clave_entry.get()
        descrip = descrip_entry.get()
        cantidad = cantidad_entry.get()
        precio = precio_entry.get()
        obser = obser_entry.get()

        # Validar campos obligatorios
        if not clave or not descrip or not cantidad or not precio:
            messagebox.showerror("Error", "Todos los campos son obligatorios excepto Observaciones.")
            return

        try:
            # Verificar si la clave ya existe antes de guardar
            conexion = conectar()
            cursor = conexion.cursor()
            query = "SELECT * FROM productos WHERE clave = %s"
            cursor.execute(query, (clave,))
            resultado = cursor.fetchone()
            if resultado:
                messagebox.showerror("Error", "La clave ya está registrada.")
                return

            # Insertar el producto en la base de datos
            query = "INSERT INTO productos (clave, descrip, cantidad, precio, obser) VALUES (%s, %s, %s, %s, %s)"
            valores = (clave, descrip, cantidad, precio, obser)
            ejecutar_consulta(query, valores)

            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            ventana_agregar.destroy()  # Cerrar la ventana de agregar producto
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo agregar el producto: {err}")

    # Botón para guardar el producto
    btn_guardar = tk.Button(ventana_agregar, text="Guardar", command=guardar_producto, font=("Arial", 14), bg="#87CEEB", fg="white")
    btn_guardar.grid(row=5, column=0, columnspan=2, pady=20)

# Funciones para modificar y eliminar productos (pendientes de implementar)
def modificar_producto(ventana):
    messagebox.showinfo("Info", "Función de modificar producto aún no implementada.")

def eliminar_producto(ventana):
    messagebox.showinfo("Info", "Función de eliminar producto aún no implementada.")