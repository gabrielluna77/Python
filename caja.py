import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Función para conectar a la base de datos
def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="punto_venta"
        )
        return conexion
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
        return None

# Función para guardar la cantidad en la tabla "cajas"
def guardar_cantidad(num_caja, cantidad):
    conexion = conectar_db()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "INSERT INTO cajas (num_caja, cant_abre, fecha) VALUES (%s, %s, CURDATE())"
            cursor.execute(query, (num_caja, cantidad))
            conexion.commit()
            messagebox.showinfo("Éxito", "Cantidad guardada correctamente.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo guardar la cantidad: {e}")
        finally:
            cursor.close()
            conexion.close()

# Función para abrir la ventana de la caja
def abrir_ventana_caja(num_caja):
    ventana_caja = tk.Toplevel()
    ventana_caja.title("Caja de Cobro")
    ventana_caja.state('zoomed')  # Poner esto para maximizar , Maximizar la ventana
    ventana_caja.lift() # Elevar la ventana al frente
    ventana_caja.focus_force() # Forzar el foco en la ventana
    
    # Título de la ventana
    titulo_label = tk.Label(ventana_caja, text="Caja de Cobro", font=("Arial", 18, "bold"), fg="blue")
    titulo_label.pack(pady=10)

    # Botón para cerrar la caja
    btn_cerrar = tk.Button(ventana_caja, text="Cerrar", command=ventana_caja.destroy, bg="red", fg="white", font=("Arial", 12, "bold"))
    btn_cerrar.pack(pady=10)

    # Botón para calcular el cambio
    btn_calcular_cambio = tk.Button(ventana_caja, text="Calcular Cambio", command=lambda: calcular_cambio(), bg="green", fg="white", font=("Arial", 12, "bold"))
    btn_calcular_cambio.pack(pady=10)

    # Botón para cobrar
    btn_cobrar = tk.Button(ventana_caja, text="Cobrar", command=lambda: cobrar(), bg="blue", fg="white", font=("Arial", 12, "bold"))
    btn_cobrar.pack(pady=10)

    # Botón para imprimir ticket
    btn_imprimir = tk.Button(ventana_caja, text="Imprimir Ticket", command=lambda: imprimir_ticket(), bg="orange", fg="white", font=("Arial", 12, "bold"))
    btn_imprimir.pack(pady=10)

    # Función para calcular el cambio
    def calcular_cambio():
        messagebox.showinfo("Calcular Cambio", "Funcionalidad de calcular cambio en desarrollo.")

    # Función para cobrar
    def cobrar():
        messagebox.showinfo("Cobrar", "Funcionalidad de cobro en desarrollo.")

    # Función para imprimir el ticket
    def imprimir_ticket():
        messagebox.showinfo("Imprimir Ticket", "Funcionalidad de impresión de ticket en desarrollo.")

# Función para abrir la ventana de apertura de caja
def abrir_ventana_apertura_caja(root):
    ventana_apertura = tk.Toplevel(root)
    ventana_apertura.title("Abrir Caja")
    ventana_apertura.geometry("300x350")
    ventana_apertura.lift() # Elevar la ventana al frente
    ventana_apertura.focus_force() # Forzar el foco en la ventana
    lbl_num_caja = tk.Label(ventana_apertura, text="Número de Caja:", font=("Arial", 12))
    lbl_num_caja.pack(pady=5)

    entry_num_caja = tk.Entry(ventana_apertura, font=("Arial", 12))
    entry_num_caja.pack(pady=5)

    lbl_cantidad = tk.Label(ventana_apertura, text="Cantidad de Apertura:", font=("Arial", 12))
    lbl_cantidad.pack(pady=5)

    entry_cantidad = tk.Entry(ventana_apertura, font=("Arial", 12))
    entry_cantidad.pack(pady=5)

    btn_guardar = tk.Button(ventana_apertura, text="Guardar", command=lambda: guardar_y_abrir_caja(entry_num_caja.get(), entry_cantidad.get()), bg="blue", fg="white", font=("Arial", 12, "bold"))
    btn_guardar.pack(pady=10)

    # Función para guardar y abrir la caja
    def guardar_y_abrir_caja(num_caja, cantidad):
        if num_caja and cantidad:
            guardar_cantidad(num_caja, cantidad)
            ventana_apertura.destroy()
            abrir_ventana_caja(num_caja)
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")