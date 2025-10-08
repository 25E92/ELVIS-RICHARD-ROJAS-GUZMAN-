import tkinter as tk
from tkinter import messagebox, filedialog
import os

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

# Diccionario con los doctores asignados
doctores_asignados = {
    "Cortes": "Dr. Juan Pérez",
    "Quemaduras": "Dra. Ana Gómez",
    "Fracturas": "Dr. Luis Martínez",
    "Convulsiones": "Dra. Elena Ríos"
}

# Función para mostrar los pasos según la situación seleccionada
def mostrar_info(situacion):
    texto.delete(1.0, tk.END)
    pasos = primeros_auxilios.get(situacion, ["No hay información disponible."])
    doctor = doctores_asignados.get(situacion, "Doctor no asignado")

    texto.insert(tk.END, f"--- {situacion} ---\n")
    texto.insert(tk.END, f"👨‍⚕️ Doctor asignado: {doctor}\n\n")
    for paso in pasos:
        texto.insert(tk.END, paso + "\n")

# Función de búsqueda rápida
def buscar():
    termino = entrada_busqueda.get().strip().capitalize()
    if termino in primeros_auxilios:
        mostrar_info(termino)
    else:
        messagebox.showinfo("No encontrado", f"No se encontró información para '{termino}'.")

# Función para guardar el contenido mostrado en un archivo .txt
def guardar_contenido():
    contenido = texto.get(1.0, tk.END).strip()
    if contenido:
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")])
        if archivo:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(contenido)
            messagebox.showinfo("Guardado", "El contenido se guardó correctamente.")
    else:
        messagebox.showwarning("Vacío", "No hay contenido para guardar.")

# Función para imprimir (simula con vista previa de impresión)
def imprimir():
    contenido = texto.get(1.0, tk.END).strip()
    if contenido:
        with open("temp_impresion.txt", "w", encoding="utf-8") as f:
            f.write(contenido)
        os.startfile("temp_impresion.txt", "print")
        messagebox.showinfo("Imprimiendo", "Se ha enviado el contenido a la impresora.")
    else:
        messagebox.showwarning("Vacío", "No hay contenido para imprimir.")

# Función para salir de la aplicación
def salir():
    if messagebox.askokcancel("Salir", "¿Deseas cerrar la aplicación?"):
        ventana.destroy()

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Asistente de Primeros Auxilios Desarrollado Por ERRG")
ventana.geometry("700x450")
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

# Botones por categoría de primeros auxilios
for situacion in primeros_auxilios.keys():
    btn = tk.Button(marco_menu, text=situacion, width=20, command=lambda s=situacion: mostrar_info(s))
    btn.pack(pady=5)

# --- NUEVOS BOTONES AGREGADOS ABAJO ---
tk.Label(marco_menu, text="").pack()  # Espaciador

btn_guardar = tk.Button(marco_menu, text="💾 Guardar", width=20, bg="lightgreen", command=guardar_contenido)
btn_guardar.pack(pady=2)

btn_imprimir = tk.Button(marco_menu, text="🖨️ Imprimir", width=20, bg="lightyellow", command=imprimir)
btn_imprimir.pack(pady=2)

btn_salir = tk.Button(marco_menu, text="❌ Salir", width=20, bg="salmon", command=salir)
btn_salir.pack(pady=10)

# Zona de texto para mostrar la información
texto = tk.Text(ventana, wrap=tk.WORD, width=50, height=20)
texto.pack(side=tk.RIGHT, padx=10, pady=10)

# Iniciar la aplicación
ventana.mainloop()
import sqlite3
# Conexión a la base de datos
conn = sqlite3.connect("pacientes.db")
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        accidente TEXT NOT NULL
    )
''')
conn.commit()
# Función para registrar a un paciente
def registrar_paciente():
    def guardar_paciente():
        nombre = entry_nombre.get().strip()
        accidente = var_accidente.get()

        if nombre and accidente:
            cursor.execute("INSERT INTO pacientes (nombre, accidente) VALUES (?, ?)", (nombre, accidente))
            conn.commit()
            messagebox.showinfo("Registro exitoso", f"Se registró a {nombre} por {accidente.lower()}.")
            ventana_registro.destroy()
        else:
            messagebox.showwarning("Datos incompletos", "Por favor, completa todos los campos.")

    ventana_registro = tk.Toplevel(ventana)
    ventana_registro.title("Registrar Paciente")
    ventana_registro.geometry("300x200")
    ventana_registro.resizable(False, False)

    tk.Label(ventana_registro, text="Nombre del paciente:").pack(pady=5)
    entry_nombre = tk.Entry(ventana_registro, width=30)
    entry_nombre.pack(pady=5)

    tk.Label(ventana_registro, text="Tipo de accidente:").pack(pady=5)
    var_accidente = tk.StringVar(ventana_registro)
    var_accidente.set("Cortes")  # valor por defecto
    opciones = list(primeros_auxilios.keys())
    menu_accidentes = tk.OptionMenu(ventana_registro, var_accidente, *opciones)
    menu_accidentes.pack(pady=5)

    btn_guardar = tk.Button(ventana_registro, text="Guardar", command=guardar_paciente)
    btn_guardar.pack(pady=10)
    # Función para mostrar pacientes registrados
def ver_pacientes():
    ventana_pacientes = tk.Toplevel(ventana)
    ventana_pacientes.title("Pacientes Registrados")
    ventana_pacientes.geometry("400x300")
    ventana_pacientes.resizable(False, False)

    texto_pacientes = tk.Text(ventana_pacientes, wrap=tk.WORD)
    texto_pacientes.pack(expand=True, fill=tk.BOTH)

    cursor.execute("SELECT nombre, accidente FROM pacientes")
    registros = cursor.fetchall()

    if registros:
        texto_pacientes.insert(tk.END, "Pacientes registrados:\n\n")
        for nombre, accidente in registros:
            texto_pacientes.insert(tk.END, f"👤 {nombre} — 🩺 {accidente}\n")
    else:
        texto_pacientes.insert(tk.END, "No hay pacientes registrados.")
        btn_registrar = tk.Button(marco_menu, text="➕ Registrar Paciente", width=20, bg="lightblue", command=registrar_paciente)
btn_registrar.pack(pady=2)

btn_ver = tk.Button(marco_menu, text="📋 Ver Pacientes", width=20, bg="lightgray", command=ver_pacientes)
btn_ver.pack(pady=2)
def salir():
    if messagebox.askokcancel("Salir", "¿Deseas cerrar la aplicación?"):
        conn.close()
        ventana.destroy()
