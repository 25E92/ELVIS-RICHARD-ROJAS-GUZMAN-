import tkinter as tk
from tkinter import messagebox

def saludar():
    nombre = entrada.get()
    if nombre:
        messagebox.showinfo("Saludo", f"¡Hola, {nombre}!")
    else:
        messagebox.showwarning("Advertencia", "Por favor, introduce tu nombre.")

# Crear la ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Mi Primera GUI")
ventana.geometry("300x200")  # Aumentamos la altura para que entren todos los elementos

# Crear y configurar widgets
etiqueta = tk.Label(ventana, text="Introduce tu nombre:")
entrada = tk.Entry(ventana, width=25)
boton_saludar = tk.Button(ventana, text="Saludar", command=saludar)
boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)

# Organizar los widgets en la ventana
etiqueta.pack(pady=10)
entrada.pack(pady=5)
boton_saludar.pack(pady=5)
boton_salir.pack(pady=5)
boton_guardar.pack(pady=5)

# Iniciar el bucle principal de eventos
ventana.mainloop()
