import tkinter as tk
from tkinter import messagebox

def saludar():
    nombre = entrada.get()
    if nombre:
        messagebox.showinfo("Saludo", f"¡Hola, {nombre}!")
    else:
        messagebox.showwarning("Advertencia", "Por favor, introduce tu nombre.")

def guardar():
    nombre = entrada.get()
    if nombre:
        try:
            with open("nombres.txt", "a") as archivo:
                archivo.write(nombre + "\n")
            messagebox.showinfo("Guardado", f"Nombre '{nombre}' guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el nombre: {e}")
    else:
        messagebox.showwarning("Advertencia", "Por favor, introduce un nombre antes de guardar.")

# Crear la ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Mi Primera GUI")
ventana.geometry("300x250")  # Altura aumentada para acomodar el nuevo botón

# Crear y configurar widgets
etiqueta = tk.Label(ventana, text="Introduce tu nombre:")
entrada = tk.Entry(ventana, width=25)
boton_saludar = tk.Button(ventana, text="Saludar", command=saludar)
boton_guardar = tk.Button(ventana, text="Guardar", command=guardar)
boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)

# Organizar los widgets en la ventana
etiqueta.pack(pady=10)
entrada.pack(pady=5)
boton_saludar.pack(pady=5)
boton_guardar.pack(pady=5)
boton_salir.pack(pady=5)

# Iniciar el bucle principal de eventos
ventana.mainloop()
