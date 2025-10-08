import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os

# ============================
#   BASE DE DATOS
# ============================
def conectar_bd():
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER,
            accidente TEXT NOT NULL,
            doctor_asignado TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def guardar_paciente_bd(nombre, edad, accidente, doctor):
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO pacientes (nombre, edad, accidente, doctor_asignado) VALUES (?, ?, ?, ?)",
                   (nombre, edad, accidente, doctor))
    conexion.commit()
    conexion.close()

def obtener_pacientes_bd():
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pacientes")
    datos = cursor.fetchall()
    conexion.close()
    return datos

# ============================
#   DATOS PRINCIPALES
# ============================
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

doctores_asignados = {
    "Cortes": "Dr. Juan Pérez",
    "Quemaduras": "Dra. Ana Gómez",
    "Fracturas": "Dr. Luis Martínez",
    "Convulsiones": "Dra. Elena Ríos"
}

# ============================
#   FUNCIONES PRINCIPALES
# ============================
def mostrar_info(situacion):
    texto.delete(1.0, tk.END)
    pasos = primeros_auxilios.get(situacion, ["No hay información disponible."])
    doctor = doctores_asignados.get(situacion, "Doctor no asignado")

    texto.insert(tk.END, f"--- {situacion} ---\n")
    texto.insert(tk.END, f"👨‍⚕️ Doctor asignado: {doctor}\n\n")
    for paso in pasos:
        texto.insert(tk.END, paso + "\n")

    combo_accidente.set(situacion)
    entry_doctor.config(state="normal")
    entry_doctor.delete(0, tk.END)
    entry_doctor.insert(0, doctor)
    entry_doctor.config(state="readonly")

def buscar():
    termino = entrada_busqueda.get().strip().capitalize()
    if termino in primeros_auxilios:
        mostrar_info(termino)
    else:
        messagebox.showinfo("No encontrado", f"No se encontró información para '{termino}'.")

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

def imprimir():
    contenido = texto.get(1.0, tk.END).strip()
    if contenido:
        with open("temp_impresion.txt", "w", encoding="utf-8") as f:
            f.write(contenido)
        os.startfile("temp_impresion.txt", "print")
        messagebox.showinfo("Imprimiendo", "Se ha enviado el contenido a la impresora.")
    else:
        messagebox.showwarning("Vacío", "No hay contenido para imprimir.")

def salir():
    if messagebox.askokcancel("Salir", "¿Deseas cerrar la aplicación?"):
        ventana.destroy()

# ============================
#   NUEVAS FUNCIONES
# ============================
def actualizar_tabla():
    """Actualiza la tabla con todos los pacientes registrados"""
    for fila in tabla_pacientes.get_children():
        tabla_pacientes.delete(fila)
    pacientes = obtener_pacientes_bd()
    for fila in pacientes:
        tabla_pacientes.insert("", "end", values=fila)

def guardar_paciente():
    nombre = entry_nombre.get().strip()
    edad = entry_edad.get().strip()
    accidente = combo_accidente.get()
    doctor = entry_doctor.get()

    if not nombre or not edad or not accidente:
        messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos del paciente.")
        return

    try:
        edad = int(edad)
    except ValueError:
        messagebox.showerror("Error", "La edad debe ser un número.")
        return

    guardar_paciente_bd(nombre, edad, accidente, doctor)

    # Actualiza tabla inmediatamente después de guardar
    actualizar_tabla()

    # Mensaje de confirmación
    messagebox.showinfo("Paciente registrado", f"✅ Paciente '{nombre}' registrado correctamente.")

    # Limpia los campos
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    combo_accidente.set("")
    entry_doctor.config(state="normal")
    entry_doctor.delete(0, tk.END)
    entry_doctor.config(state="readonly")

# ============================
#   INTERFAZ GRÁFICA
# ============================
ventana = tk.Tk()
ventana.title("Asistente de Primeros Auxilios - ERRG")
ventana.geometry("1000x600")
ventana.config(bg="#e6f2ff")
ventana.resizable(False, False)

conectar_bd()

# --- Título principal ---
titulo = tk.Label(ventana, text="🩺 Asistente Digital de Primeros Auxilios", font=("Helvetica", 16, "bold"), bg="#4da6ff", fg="white")
titulo.pack(fill=tk.X)

# --- Búsqueda ---
marco_busqueda = tk.Frame(ventana, bg="#e6f2ff")
marco_busqueda.pack(pady=5)
entrada_busqueda = tk.Entry(marco_busqueda, width=30)
entrada_busqueda.pack(side=tk.LEFT, padx=5)
tk.Button(marco_busqueda, text="Buscar", command=buscar, bg="#99ccff").pack(side=tk.LEFT)

# --- Menú lateral ---
marco_menu = tk.Frame(ventana, bg="#e6f2ff")
marco_menu.pack(side=tk.LEFT, padx=10, pady=10)

for situacion in primeros_auxilios.keys():
    tk.Button(marco_menu, text=situacion, width=20, bg="#b3e0ff", command=lambda s=situacion: mostrar_info(s)).pack(pady=4)

tk.Label(marco_menu, text="", bg="#e6f2ff").pack()
tk.Button(marco_menu, text="💾 Guardar", width=20, bg="lightgreen", command=guardar_contenido).pack(pady=2)
tk.Button(marco_menu, text="🖨️ Imprimir", width=20, bg="lightyellow", command=imprimir).pack(pady=2)
tk.Button(marco_menu, text="❌ Salir", width=20, bg="salmon", command=salir).pack(pady=8)

# --- Área de texto ---
texto = tk.Text(ventana, wrap=tk.WORD, width=45, height=20, bg="white", fg="#003366")
texto.pack(side=tk.RIGHT, padx=10, pady=10)

# --- Formulario de paciente ---
marco_paciente = tk.LabelFrame(ventana, text="Registro de Pacientes", bg="#e6f2ff", font=("Arial", 10, "bold"))
marco_paciente.place(x=260, y=330, width=720, height=120)

tk.Label(marco_paciente, text="Nombre:", bg="#e6f2ff").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_nombre = tk.Entry(marco_paciente, width=25)
entry_nombre.grid(row=0, column=1)

tk.Label(marco_paciente, text="Edad:", bg="#e6f2ff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_edad = tk.Entry(marco_paciente, width=25)
entry_edad.grid(row=1, column=1)

tk.Label(marco_paciente, text="Accidente:", bg="#e6f2ff").grid(row=0, column=2, padx=5, pady=5, sticky="e")
combo_accidente = tk.StringVar()
entry_accidente = tk.OptionMenu(marco_paciente, combo_accidente, *primeros_auxilios.keys())
entry_accidente.grid(row=0, column=3, padx=5, pady=5)

tk.Label(marco_paciente, text="Doctor:", bg="#e6f2ff").grid(row=1, column=2, padx=5, pady=5, sticky="e")
entry_doctor = tk.Entry(marco_paciente, width=25, state="readonly")
entry_doctor.grid(row=1, column=3)

tk.Button(marco_paciente, text="Guardar Paciente", bg="#99ff99", command=guardar_paciente).grid(row=0, column=4, rowspan=2, padx=15)

# --- Tabla de pacientes ---
marco_tabla = tk.LabelFrame(ventana, text="Pacientes Registrados", bg="#e6f2ff", font=("Arial", 10, "bold"))
marco_tabla.place(x=260, y=70, width=720, height=250)

columnas = ("ID", "Nombre", "Edad", "Accidente", "Doctor")
tabla_pacientes = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=10)

for col in columnas:
    tabla_pacientes.heading(col, text=col)
    tabla_pacientes.column(col, width=130, anchor="center")

tabla_pacientes.pack(fill=tk.BOTH, expand=True)

# --- Cargar datos al inicio ---
actualizar_tabla()

ventana.mainloop()