import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
from datetime import datetime

# ============================
#   CONEXIÓN BASE DE DATOS
# ============================
def conectar_bd():
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pacientes'")
    existe = cursor.fetchone()

    if existe:
        cursor.execute("PRAGMA table_info(pacientes)")
        columnas = [col[1] for col in cursor.fetchall()]
        columnas_necesarias = {"id", "nombre", "edad", "accidente", "doctor_asignado", "fecha_atencion"}
        if not columnas_necesarias.issubset(columnas):
            cursor.execute("DROP TABLE pacientes")
            conexion.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER,
            accidente TEXT NOT NULL,
            doctor_asignado TEXT NOT NULL,
            fecha_atencion TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

def guardar_paciente_bd(nombre, edad, accidente, doctor, fecha):
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO pacientes (nombre, edad, accidente, doctor_asignado, fecha_atencion) VALUES (?, ?, ?, ?, ?)",
        (nombre, edad, accidente, doctor, fecha))
    conexion.commit()
    conexion.close()

def obtener_pacientes_bd():
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pacientes")
    datos = cursor.fetchall()
    conexion.close()
    return datos

def eliminar_paciente_bd(id_paciente):
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
    conexion.commit()
    conexion.close()

def consultar_paciente(nombre):
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM pacientes WHERE nombre LIKE ?", ('%' + nombre + '%',))
    datos = cursor.fetchall()
    conexion.close()
    return datos

# ============================
#   DATOS DE APOYO
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
#   FUNCIONES PACIENTES
# ============================
def actualizar_tabla():
    for fila in tabla_pacientes.get_children():
        tabla_pacientes.delete(fila)
    for fila in obtener_pacientes_bd():
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

    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    guardar_paciente_bd(nombre, edad, accidente, doctor, fecha_actual)
    actualizar_tabla()
    messagebox.showinfo("Paciente registrado", f"✅ Paciente '{nombre}' registrado correctamente.")
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    combo_accidente.set("")
    entry_doctor.config(state="normal")
    entry_doctor.delete(0, tk.END)
    entry_doctor.config(state="readonly")

def borrar_paciente():
    seleccion = tabla_pacientes.selection()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Por favor, selecciona un paciente para borrar.")
        return

    item = tabla_pacientes.item(seleccion)
    id_paciente = item["values"][0]
    nombre = item["values"][1]
    if messagebox.askyesno("Confirmar", f"¿Deseas borrar al paciente '{nombre}'?"):
        eliminar_paciente_bd(id_paciente)
        actualizar_tabla()
        messagebox.showinfo("Eliminado", f"🗑️ Paciente '{nombre}' eliminado correctamente.")

def buscar_paciente_tabla():
    nombre = entry_buscar_paciente.get().strip()
    if not nombre:
        messagebox.showwarning("Campo vacío", "Por favor, ingresa un nombre para consultar.")
        return

    resultados = consultar_paciente(nombre)
    for fila in tabla_pacientes.get_children():
        tabla_pacientes.delete(fila)

    if resultados:
        for fila in resultados:
            tabla_pacientes.insert("", "end", values=fila)
    else:
        messagebox.showinfo("Sin resultados", f"No se encontraron pacientes con el nombre '{nombre}'.")

# ============================
#   INTERFAZ GRÁFICA
# ============================
ventana = tk.Tk()
from tkinter import PhotoImage
ventana.title("MEDICAL CENTER - ELVIS ROJAS")
ventana.geometry("1150x600")
ventana.config(bg="#e6f2ff")
ventana.resizable(False, False)

conectar_bd()

titulo = tk.Label(ventana, text="🩺 Asistente Digital de Primeros Auxilios", font=("Helvetica", 16, "bold"), bg="#4da6ff", fg="white")
titulo.pack(fill=tk.X)

# Marco búsqueda de información
marco_busqueda = tk.Frame(ventana, bg="#e6f2ff")
marco_busqueda.pack(pady=5)
entrada_busqueda = tk.Entry(marco_busqueda, width=30)
entrada_busqueda.pack(side=tk.LEFT, padx=5)
tk.Button(marco_busqueda, text="Buscar", command=buscar, bg="#99ccff").pack(side=tk.LEFT)

# Menú lateral
marco_menu = tk.Frame(ventana, bg="#e6f2ff")
marco_menu.pack(side=tk.LEFT, padx=10, pady=10)
for situacion in primeros_auxilios.keys():
    tk.Button(marco_menu, text=situacion, width=20, bg="#b3e0ff", command=lambda s=situacion: mostrar_info(s)).pack(pady=4)
tk.Label(marco_menu, text="", bg="#e6f2ff").pack()
tk.Button(marco_menu, text="💾 Guardar", width=20, bg="lightgreen", command=guardar_contenido).pack(pady=2)
tk.Button(marco_menu, text="🖨️ Imprimir", width=20, bg="lightyellow", command=imprimir).pack(pady=2)
tk.Button(marco_menu, text="❌ Salir", width=20, bg="salmon", command=salir).pack(pady=8)

# Cuadro de texto información
texto = tk.Text(ventana, wrap=tk.WORD, width=45, height=20, bg="white", fg="#003366")
texto.pack(side=tk.RIGHT, padx=10, pady=10)

# Tabla pacientes
marco_tabla = tk.LabelFrame(ventana, text="Pacientes Registrados", bg="#e6f2ff", font=("Arial", 10, "bold"))
marco_tabla.place(x=260, y=70, width=860, height=250)
columnas = ("ID", "Nombre", "Edad", "Accidente", "Doctor", "Fecha Atención")
tabla_pacientes = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=10)
for col in columnas:
    tabla_pacientes.heading(col, text=col)
    tabla_pacientes.column(col, width=130, anchor="center")
tabla_pacientes.pack(fill=tk.BOTH, expand=True)

# Marco registro
marco_paciente = tk.LabelFrame(ventana, text="Registro de Pacientes", bg="#e6f2ff", font=("Arial", 10, "bold"))
marco_paciente.place(x=260, y=330, width=860, height=160)

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

# Botones principales
tk.Button(marco_paciente, text="Guardar Paciente", bg="#99ff99", command=guardar_paciente).grid(row=0, column=4, rowspan=2, padx=10)
tk.Button(marco_paciente, text="🗑️ Borrar Paciente", bg="#ff9999", command=borrar_paciente).grid(row=0, column=5, rowspan=2, padx=10)

# 🔍 Campo de búsqueda de pacientes
tk.Label(marco_paciente, text="Buscar paciente:", bg="#e6f2ff").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_buscar_paciente = tk.Entry(marco_paciente, width=25)
entry_buscar_paciente.grid(row=2, column=1, padx=5, pady=5)
tk.Button(marco_paciente, text="🔍 Consultar", bg="#99ccff", command=buscar_paciente_tabla).grid(row=2, column=2, padx=5, pady=5)
tk.Button(marco_paciente, text="🔄 Mostrar Todos", bg="#ccffcc", command=actualizar_tabla).grid(row=2, column=3, padx=5, pady=5)

# ============================
#   EJECUCIÓN
# ============================
actualizar_tabla()
ventana.mainloop()
