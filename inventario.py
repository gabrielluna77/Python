import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
from database import conectar, ejecutar_consulta


def abrir_ventana_inventario(root):
    """
    Abre la ventana principal del inventario.
    """
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


def agregar_producto(ventana):
    """
    Abre la ventana para agregar un nuevo producto.
    """
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
                messagebox.showinfo("Clave existente", "La clave ya existe.", parent=ventana_agregar)
                clave_entry.focus_set()  # Regresar el foco al campo de la clave
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo verificar la clave: {err}", parent=ventana_agregar)

    # Vincular el evento KeyRelease al campo de la clave
    clave_entry.bind("<KeyRelease>", verificar_clave)

    # Función para limpiar los campos del formulario
    def limpiar_campos():
        clave_entry.delete(0, tk.END)
        descrip_entry.delete(0, tk.END)
        cantidad_entry.delete(0, tk.END)
        precio_entry.delete(0, tk.END)
        obser_entry.delete(0, tk.END)
        clave_entry.focus_set()  # Colocar el foco en el campo de la clave

    # Función para guardar el producto en la base de datos
    def guardar_producto():
        clave = clave_entry.get()
        descrip = descrip_entry.get()
        cantidad = cantidad_entry.get()
        precio = precio_entry.get()
        obser = obser_entry.get()

        # Validar campos obligatorios
        if not clave or not descrip or not cantidad or not precio:
            messagebox.showerror("Error", "Todos los campos son obligatorios excepto Observaciones.", parent=ventana_agregar)
            return

        try:
            # Verificar si la clave ya existe antes de guardar
            conexion = conectar()
            cursor = conexion.cursor()
            query = "SELECT * FROM productos WHERE clave = %s"
            cursor.execute(query, (clave,))
            resultado = cursor.fetchone()
            if resultado:
                messagebox.showerror("Error", "La clave ya está registrada.", parent=ventana_agregar)
                return

            # Insertar el producto en la base de datos
            query = "INSERT INTO productos (clave, descrip, cantidad, precio, obser) VALUES (%s, %s, %s, %s, %s)"
            valores = (clave, descrip, cantidad, precio, obser)
            ejecutar_consulta(query, valores)

            messagebox.showinfo("Éxito", "Producto agregado correctamente.", parent=ventana_agregar)
            limpiar_campos()  # Limpiar los campos después de guardar
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo agregar el producto: {err}", parent=ventana_agregar)

    # Botón para guardar el producto
    btn_guardar = tk.Button(ventana_agregar, text="Guardar", command=guardar_producto, font=("Arial", 14), bg="#87CEEB", fg="white")
    btn_guardar.grid(row=5, column=0, columnspan=2, pady=20)

    # Botón para regresar a la ventana de inventario
    btn_regresar = tk.Button(ventana_agregar, text="Regresar", command=ventana_agregar.destroy, font=("Arial", 14), bg="#87CEEB", fg="white")
    btn_regresar.grid(row=5, column=2, pady=20, padx=10)


def modificar_producto(ventana):
    """
    Abre la ventana para modificar un producto existente.
    """
    ventana_modificar = tk.Toplevel(ventana)
    ventana_modificar.title("Modificar Producto")
    ventana_modificar.geometry("600x400")

    # Frame para buscar producto
    buscar_frame = tk.Frame(ventana_modificar)
    buscar_frame.pack(pady=20)

    # Campo para ingresar la clave o descripción
    tk.Label(buscar_frame, text="Clave o Descripción:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
    buscar_entry = tk.Entry(buscar_frame, font=("Arial", 14))
    buscar_entry.grid(row=0, column=1, padx=10, pady=10)

    # Función para buscar el producto
    def buscar_producto():
        criterio = buscar_entry.get()
        if not criterio:
            messagebox.showwarning("Advertencia", "Ingrese una clave o descripción para buscar.", parent=ventana_modificar)
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM productos WHERE clave = %s OR descrip LIKE %s"
            cursor.execute(query, (criterio, f"%{criterio}%"))
            producto = cursor.fetchone()
            cursor.close()
            conexion.close()

            if producto:
                mostrar_detalles_producto(producto)
            else:
                messagebox.showinfo("No encontrado", "No se encontró ningún producto con ese criterio.", parent=ventana_modificar)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo buscar el producto: {err}", parent=ventana_modificar)

    # Botón para buscar producto
    btn_buscar = tk.Button(buscar_frame, text="Buscar", command=buscar_producto, font=("Arial", 14), bg="#87CEEB", fg="white")
    btn_buscar.grid(row=0, column=2, padx=10, pady=10)

    # Frame para mostrar y modificar detalles del producto
    detalles_frame = tk.Frame(ventana_modificar)
    detalles_frame.pack(pady=20)

    # Campos del formulario
    tk.Label(detalles_frame, text="Clave:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
    clave_entry = tk.Entry(detalles_frame, font=("Arial", 14))
    clave_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(detalles_frame, text="Descripción:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
    descrip_entry = tk.Entry(detalles_frame, font=("Arial", 14))
    descrip_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(detalles_frame, text="Cantidad:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10)
    cantidad_entry = tk.Entry(detalles_frame, font=("Arial", 14))
    cantidad_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(detalles_frame, text="Precio:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=10)
    precio_entry = tk.Entry(detalles_frame, font=("Arial", 14))
    precio_entry.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(detalles_frame, text="Observaciones:", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=10)
    obser_entry = tk.Entry(detalles_frame, font=("Arial", 14))
    obser_entry.grid(row=4, column=1, padx=10, pady=10)

    # Función para mostrar los detalles del producto encontrado
    def mostrar_detalles_producto(producto):
        clave_entry.delete(0, tk.END)
        descrip_entry.delete(0, tk.END)
        cantidad_entry.delete(0, tk.END)
        precio_entry.delete(0, tk.END)
        obser_entry.delete(0, tk.END)

        clave_entry.insert(0, producto["clave"])
        descrip_entry.insert(0, producto["descrip"])
        cantidad_entry.insert(0, producto["cantidad"])
        precio_entry.insert(0, producto["precio"])
        obser_entry.insert(0, producto["obser"])

    # Función para limpiar los campos del formulario
    def limpiar_campos():
        buscar_entry.delete(0, tk.END)  # Limpiar el campo de búsqueda
        clave_entry.delete(0, tk.END)
        descrip_entry.delete(0, tk.END)
        cantidad_entry.delete(0, tk.END)
        precio_entry.delete(0, tk.END)
        obser_entry.delete(0, tk.END)
        buscar_entry.focus_set()  # Colocar el foco en el campo de búsqueda

    # Función para guardar los cambios del producto
    def guardar_cambios():
        clave = clave_entry.get()
        descrip = descrip_entry.get()
        cantidad = cantidad_entry.get()
        precio = precio_entry.get()
        obser = obser_entry.get()

        # Validar campos obligatorios
        if not clave or not descrip or not cantidad or not precio:
            messagebox.showerror("Error", "Todos los campos son obligatorios excepto Observaciones.", parent=ventana_modificar)
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            query = "UPDATE productos SET descrip = %s, cantidad = %s, precio = %s, obser = %s WHERE clave = %s"
            valores = (descrip, cantidad, precio, obser, clave)
            ejecutar_consulta(query, valores)

            messagebox.showinfo("Éxito", "Producto modificado correctamente.", parent=ventana_modificar)
            limpiar_campos()  # Limpiar los campos después de guardar
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo modificar el producto: {err}", parent=ventana_modificar)

    # Botón para guardar cambios
    btn_guardar = tk.Button(detalles_frame, text="Guardar Cambios", command=guardar_cambios, font=("Arial", 14), bg="#87CEEB", fg="white")
    btn_guardar.grid(row=5, column=0, columnspan=2, pady=20)

    # Botón para regresar
    btn_regresar = tk.Button(ventana_modificar, text="Regresar", command=ventana_modificar.destroy, font=("Arial", 14), bg="#87CEEB", fg="white")
    btn_regresar.pack(pady=10)


def eliminar_producto(ventana):
    """
    Abre la ventana para eliminar un producto existente.
    """
    ventana_eliminar = tk.Toplevel(ventana)
    ventana_eliminar.title("Eliminar Producto")
    ventana_eliminar.geometry("600x400")

    # Frame para buscar producto
    buscar_frame = tk.Frame(ventana_eliminar)
    buscar_frame.pack(pady=20)

    # Campo para ingresar la clave o descripción
    tk.Label(buscar_frame, text="Clave o Descripción:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
    buscar_entry = tk.Entry(buscar_frame, font=("Arial", 14))
    buscar_entry.grid(row=0, column=1, padx=10, pady=10)

    # Función para buscar el producto
    def buscar_producto():
        criterio = buscar_entry.get()
        if not criterio:
            messagebox.showwarning("Advertencia", "Ingrese una clave o descripción para buscar.", parent=ventana_eliminar)
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM productos WHERE clave = %s OR descrip LIKE %s"
            cursor.execute(query, (criterio, f"%{criterio}%"))
            producto = cursor.fetchone()
            cursor.close()
            conexion.close()

            if producto:
                mostrar_detalles_producto(producto)
            else:
                messagebox.showinfo("No encontrado", "No se encontró ningún producto con ese criterio.", parent=ventana_eliminar)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo buscar el producto: {err}", parent=ventana_eliminar)

    # Botón para buscar producto
    btn_buscar = tk.Button(buscar_frame, text="Buscar", command=buscar_producto, font=("Arial", 14), bg="#87CEEB", fg="white")
    btn_buscar.grid(row=0, column=2, padx=10, pady=10)

    # Frame para mostrar detalles del producto
    detalles_frame = tk.Frame(ventana_eliminar)
    detalles_frame.pack(pady=20)

    # Campos del formulario (solo lectura)
    tk.Label(detalles_frame, text="Clave:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10)
    clave_entry = tk.Entry(detalles_frame, font=("Arial", 14), state="readonly")
    clave_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(detalles_frame, text="Descripción:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10)
    descrip_entry = tk.Entry(detalles_frame, font=("Arial", 14), state="readonly")
    descrip_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(detalles_frame, text="Cantidad:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10)
    cantidad_entry = tk.Entry(detalles_frame, font=("Arial", 14), state="readonly")
    cantidad_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(detalles_frame, text="Precio:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=10)
    precio_entry = tk.Entry(detalles_frame, font=("Arial", 14), state="readonly")
    precio_entry.grid(row=3, column=1, padx=10, pady=10)

    tk.Label(detalles_frame, text="Observaciones:", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=10)
    obser_entry = tk.Entry(detalles_frame, font=("Arial", 14), state="readonly")
    obser_entry.grid(row=4, column=1, padx=10, pady=10)

    # Función para mostrar los detalles del producto encontrado
    def mostrar_detalles_producto(producto):
        clave_entry.config(state="normal")
        descrip_entry.config(state="normal")
        cantidad_entry.config(state="normal")
        precio_entry.config(state="normal")
        obser_entry.config(state="normal")

        clave_entry.delete(0, tk.END)
        descrip_entry.delete(0, tk.END)
        cantidad_entry.delete(0, tk.END)
        precio_entry.delete(0, tk.END)
        obser_entry.delete(0, tk.END)

        clave_entry.insert(0, producto["clave"])
        descrip_entry.insert(0, producto["descrip"])
        cantidad_entry.insert(0, producto["cantidad"])
        precio_entry.insert(0, producto["precio"])
        obser_entry.insert(0, producto["obser"])

        clave_entry.config(state="readonly")
        descrip_entry.config(state="readonly")
        cantidad_entry.config(state="readonly")
        precio_entry.config(state="readonly")
        obser_entry.config(state="readonly")

    # Función para eliminar el producto
    def eliminar():
        clave = clave_entry.get()
        if not clave:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ningún producto para eliminar.", parent=ventana_eliminar)
            return

        # Confirmar eliminación
        confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este producto?", parent=ventana_eliminar)
        if not confirmacion:
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            query = "DELETE FROM productos WHERE clave = %s"
            cursor.execute(query, (clave,))
            conexion.commit()
            cursor.close()
            conexion.close()

            messagebox.showinfo("Éxito", "Producto eliminado correctamente.", parent=ventana_eliminar)
            limpiar_campos()  # Limpiar los campos después de eliminar
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {err}", parent=ventana_eliminar)

    # Función para limpiar los campos del formulario
    def limpiar_campos():
        buscar_entry.delete(0, tk.END)
        clave_entry.config(state="normal")
        descrip_entry.config(state="normal")
        cantidad_entry.config(state="normal")
        precio_entry.config(state="normal")
        obser_entry.config(state="normal")

        clave_entry.delete(0, tk.END)
        descrip_entry.delete(0, tk.END)
        cantidad_entry.delete(0, tk.END)
        precio_entry.delete(0, tk.END)
        obser_entry.delete(0, tk.END)

        clave_entry.config(state="readonly")
        descrip_entry.config(state="readonly")
        cantidad_entry.config(state="readonly")
        precio_entry.config(state="readonly")
        obser_entry.config(state="readonly")

        buscar_entry.focus_set()  # Colocar el foco en el campo de búsqueda

    # Botón para eliminar el producto
    btn_eliminar = tk.Button(detalles_frame, text="Eliminar", command=eliminar, font=("Arial", 14), bg="#FF6347", fg="white")
    btn_eliminar.grid(row=5, column=0, columnspan=2, pady=20)

    # Botón para regresar
    btn_regresar = tk.Button(ventana_eliminar, text="Regresar", command=ventana_eliminar.destroy, font=("Arial", 14), bg="#87CEEB", fg="white")
    btn_regresar.pack(pady=10)
