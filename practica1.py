import tkinter as tk
from tkinter import messagebox

# Diccionario con la información de primeros auxilios
primeros_auxilios = {
    "Cortes": [
        "1. Lava tus manos antes de tocar la herida.",
        "2. Detén el sangrado con una gasa limpia.",
        "3. Lava la herida con agua y jabón.",
        "4. Cubre la herida con una venda.",
        "5. Busca atención médica si es profunda."
    ],
    "Quemaduras": [
        "1. Enfría la quemadura con agua fría por 10 minutos.",
        "2. No revientes las ampollas.",
        "3. Cubre con un apósito limpio y seco.",
        "4. Si es grave, acude al hospital."
    ],
    "Fracturas": [
        "1. No muevas la zona afectada.",
        "2. Inmoviliza con una férula si es posible.",
        "3. Aplica hielo envuelto en un paño.",
        "4. Busca atención médica de inmediato."
    ],
    "Convulsiones": [
        "1. No sujetes a la persona.",
        "2. Retira objetos cercanos peligrosos.",
        "3. Coloca algo blando bajo su cabeza.",
        "4. Gira su cuerpo de lado una vez termine.",
        "5. Llama a emergencias si dura más de 5 minutos."
    ]
}

# Función para mostrar los pasos según la situación seleccionada
def mostrar_info(situacion):
    texto.delete(1.0, tk.END)
    pasos = primeros_auxilios.get(situacion, ["No hay información disponible."])
    texto.insert(tk.END, f"--- {situacion} ---\n\n")
    for paso in pasos:
        texto.insert(tk.END, paso + "\n")

# Función de búsqueda rápida
def buscar():
    termino = entrada_busqueda.get().strip().capitalize()
    if termino in primeros_auxilios:
        mostrar_info(termino)
    else:
        messagebox.showinfo("No encontrado", f"No se encontró información para '{termino}'.")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Asistente de Primeros Auxilios Desarrollado Por ERRG")
ventana.geometry("600x400")
ventana.resizable(False, False)

# Interfaz de usuario
titulo = tk.Label(ventana, text="Asistente Digital de Primeros Auxilios", font=("Helvetica", 16), bg="lightblue")
titulo.pack(fill=tk.X)

# Marco superior con búsqueda
marco_busqueda = tk.Frame(ventana)
marco_busqueda.pack(pady=5)

entrada_busqueda = tk.Entry(marco_busqueda, width=30)
entrada_busqueda.pack(side=tk.LEFT, padx=5)
btn_buscar = tk.Button(marco_busqueda, text="Buscar", command=buscar)
btn_buscar.pack(side=tk.LEFT)

# Marco izquierdo para menú
marco_menu = tk.Frame(ventana)
marco_menu.pack(side=tk.LEFT, padx=10, pady=10)

# Botones por categoría
for situacion in primeros_auxilios.keys():
    btn = tk.Button(marco_menu, text=situacion, width=15, command=lambda s=situacion: mostrar_info(s))
    btn.pack(pady=5)

# Zona de texto para mostrar información
texto = tk.Text(ventana, wrap=tk.WORD, width=50, height=20)
texto.pack(side=tk.RIGHT, padx=10, pady=10)

# Iniciar la aplicación
ventana.mainloop()
