import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from inventario import abrir_ventana_inventario  # Importar la función del módulo inventario.py

# Crear la ventana principal
root = tk.Tk()
root.title("Punto de Venta")
root.geometry("800x600")

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

# Configurar el grid para que las columnas y filas se expandan
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

# Crear un Frame para contener el logo y el título
header_frame = tk.Frame(root)
header_frame.grid(row=0, column=0, columnspan=3, pady=20, sticky="n")

# Agregar el logo al Frame
if logo_tk:
    lbl_logo = tk.Label(header_frame, image=logo_tk)
    lbl_logo.pack(side="left", padx=10)
    lbl_logo.image = logo_tk

# Agregar el título al Frame
titulo_label = tk.Label(header_frame, text="PUNTO DE VENTA TODOCOMPU 1.0", font=("Arial", 24, "bold"), fg="blue")
titulo_label.pack(side="left", padx=10)

# Estilo de los botones
button_style = {
    "bg": "#87CEEB",
    "fg": "white",
    "font": ("Arial", 14, "bold"),
    "width": 20,
    "height": 5,
    "activebackground": "#6CA6CD",
    "activeforeground": "white",
}

# Botón para Caja
btn_caja = tk.Button(root, text="Caja", command=lambda: abrir_ventana("Caja"), **button_style)
btn_caja.grid(row=1, column=0, padx=10, pady=10)

# Botón para Inventario
btn_inventario = tk.Button(root, text="Inventario", command=lambda: abrir_ventana_inventario(root), **button_style)
btn_inventario.grid(row=1, column=1, padx=10, pady=10)

# Botón para Corte de Caja
btn_corte = tk.Button(root, text="Corte de Caja", command=lambda: abrir_ventana("Corte de Caja"), **button_style)
btn_corte.grid(row=1, column=2, padx=10, pady=10)

# Botón para Salir
btn_salir = tk.Button(root, text="Salir", command=root.destroy, **button_style)
btn_salir.grid(row=2, column=2, padx=10, pady=10, sticky="se")

# Iniciar el bucle principal de la aplicación
root.mainloop()