# ============================
#   IMPORTACIONES DE LIBRERÍAS
# ============================
# Librerías estándar de Python
import os
import pickle
import sqlite3
import threading
import time
import calendar
from datetime import datetime

# Librerías de terceros para interfaz gráfica
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Librerías de terceros para procesamiento de imágenes y reconocimiento facial
try:
    import cv2
    import numpy as np
    import face_recognition
    from PIL import Image, ImageTk
except ImportError as e:
    print(f"Error al importar librerías de reconocimiento facial: {e}")
    print("Instale las dependencias con: pip install -r requirements.txt")
    # Definir variables dummy para evitar errores
    cv2 = None
    np = None
    face_recognition = None
    Image = None
    ImageTk = None

# ============================
#   VERIFICACIÓN DE DEPENDENCIAS
# ============================
def verificar_dependencias():
    """Verifica que todas las dependencias necesarias estén instaladas"""
    dependencias_faltantes = []
    
    if cv2 is None:
        dependencias_faltantes.append("opencv-python")
    if np is None:
        dependencias_faltantes.append("numpy")
    if face_recognition is None:
        dependencias_faltantes.append("face-recognition")
    if Image is None or ImageTk is None:
        dependencias_faltantes.append("Pillow")
    
    if dependencias_faltantes:
        mensaje = f"Dependencias faltantes: {', '.join(dependencias_faltantes)}\n\n"
        mensaje += "Instale las dependencias con:\n"
        mensaje += "pip install -r requirements.txt"
        
        print(mensaje)
        return False
    
    return True

# ============================
#   CONEXIÓN BASE DE DATOS
# ============================
def conectar_bd():
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    
    # Verificar y crear tabla pacientes
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
    
    # Crear tabla de citas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_paciente TEXT NOT NULL,
            telefono TEXT,
            motivo TEXT NOT NULL,
            doctor TEXT NOT NULL,
            fecha_cita TEXT NOT NULL,
            hora_cita TEXT NOT NULL,
            estado TEXT DEFAULT 'Programada',
            fecha_creacion TEXT NOT NULL
        )
    """)
    
    # Crear tabla de control de asistencia
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asistencia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_personal TEXT NOT NULL,
            cargo TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora_entrada TEXT,
            hora_salida TEXT,
            estado TEXT DEFAULT 'Presente',
            observaciones TEXT
        )
    """)
    
    # Crear tabla de personal registrado
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cargo TEXT NOT NULL,
            codigo TEXT UNIQUE NOT NULL,
            foto_encoding BLOB,
            fecha_registro TEXT NOT NULL,
            activo INTEGER DEFAULT 1
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

def actualizar_paciente_bd(id_paciente, nombre, edad, accidente, doctor, fecha):
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE pacientes SET nombre = ?, edad = ?, accidente = ?, doctor_asignado = ?, fecha_atencion = ? WHERE id = ?",
        (nombre, edad, accidente, doctor, fecha, id_paciente))
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
#   FUNCIONES CITAS
# ============================
def guardar_cita_bd(nombre, telefono, motivo, doctor, fecha, hora):
    """Guarda una nueva cita en la base de datos"""
    try:
        conexion = sqlite3.connect("pacientes.db")
        cursor = conexion.cursor()
        fecha_creacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO citas (nombre_paciente, telefono, motivo, doctor, fecha_cita, hora_cita, estado, fecha_creacion) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, telefono, motivo, doctor, fecha, hora, 'Programada', fecha_creacion))
        
        conexion.commit()
        conexion.close()
        print(f"Cita guardada: {nombre} - {doctor} - {fecha} {hora}")  # Debug
        return True
    except Exception as e:
        print(f"Error al guardar cita: {e}")  # Debug
        return False

def obtener_citas_bd():
    """Obtiene todas las citas de la base de datos"""
    try:
        conexion = sqlite3.connect("pacientes.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM citas ORDER BY fecha_cita, hora_cita")
        datos = cursor.fetchall()
        conexion.close()
        print(f"Citas obtenidas de la BD: {len(datos)} registros")  # Debug
        return datos
    except Exception as e:
        print(f"Error al obtener citas: {e}")  # Debug
        return []

def eliminar_cita_bd(id_cita):
    """Elimina una cita de la base de datos"""
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM citas WHERE id = ?", (id_cita,))
    conexion.commit()
    conexion.close()

def consultar_citas_por_fecha(fecha):
    """Consulta citas por una fecha específica"""
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM citas WHERE fecha_cita = ? ORDER BY hora_cita", (fecha,))
    datos = cursor.fetchall()
    conexion.close()
    return datos

# ============================
#   FUNCIONES CONTROL DE ASISTENCIA
# ============================
def guardar_personal_bd(nombre, cargo, codigo, foto_encoding):
    """Guarda un miembro del personal en la base de datos"""
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    fecha_registro = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO personal (nombre, cargo, codigo, foto_encoding, fecha_registro) 
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, cargo, codigo, foto_encoding, fecha_registro))
    
    conexion.commit()
    conexion.close()

def obtener_personal_bd():
    """Obtiene todos los miembros del personal registrados"""
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM personal WHERE activo = 1")
    datos = cursor.fetchall()
    conexion.close()
    return datos

def registrar_entrada_salida(nombre, cargo, tipo_registro, observaciones=""):
    """Registra entrada o salida del personal"""
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    hora_actual = datetime.now().strftime("%H:%M:%S")
    
    # Verificar si ya existe un registro para hoy
    cursor.execute("SELECT * FROM asistencia WHERE nombre_personal = ? AND fecha = ?", 
                   (nombre, fecha_actual))
    registro_existente = cursor.fetchone()
    
    if registro_existente:
        if tipo_registro == "entrada":
            messagebox.showwarning("Ya registrado", f"{nombre} ya registró entrada hoy.")
        else:  # salida
            cursor.execute("""
                UPDATE asistencia SET hora_salida = ?, observaciones = ? 
                WHERE nombre_personal = ? AND fecha = ?
            """, (hora_actual, observaciones, nombre, fecha_actual))
            messagebox.showinfo("Salida registrada", f"Salida registrada para {nombre} a las {hora_actual}")
    else:
        if tipo_registro == "entrada":
            cursor.execute("""
                INSERT INTO asistencia (nombre_personal, cargo, fecha, hora_entrada, observaciones) 
                VALUES (?, ?, ?, ?, ?)
            """, (nombre, cargo, fecha_actual, hora_actual, observaciones))
            messagebox.showinfo("Entrada registrada", f"Entrada registrada para {nombre} a las {hora_actual}")
        else:
            messagebox.showwarning("Sin entrada", f"{nombre} no tiene entrada registrada para hoy.")
    
    conexion.commit()
    conexion.close()

def obtener_asistencia_bd():
    """Obtiene todos los registros de asistencia"""
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM asistencia ORDER BY fecha DESC, hora_entrada DESC")
    datos = cursor.fetchall()
    conexion.close()
    return datos

def capturar_rostro_para_registro():
    """Captura una foto para el registro de personal"""
    if cv2 is None:
        messagebox.showerror("Error", "OpenCV no está instalado. Instale las dependencias con: pip install -r requirements.txt")
        return None
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        messagebox.showerror("Error", "No se puede acceder a la cámara")
        return None
    
    messagebox.showinfo("Captura", "Mire a la cámara y presione ESPACIO para capturar. Presione ESC para cancelar.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.putText(frame, "Presione ESPACIO para capturar", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Presione ESC para cancelar", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.imshow('Capturar Rostro', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # Espacio
            # Capturar la imagen
            rostro_capturado = frame.copy()
            cv2.destroyAllWindows()
            cap.release()
            return rostro_capturado
        elif key == 27:  # ESC
            cv2.destroyAllWindows()
            cap.release()
            return None
    
    cap.release()
    return None

def procesar_rostro_capturado(imagen):
    """Procesa la imagen capturada para obtener el encoding facial"""
    if cv2 is None or face_recognition is None:
        messagebox.showerror("Error", "Librerías de reconocimiento facial no están instaladas.")
        return None
    
    try:
        # Convertir de BGR a RGB
        rgb_image = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        
        # Detectar rostros
        face_locations = face_recognition.face_locations(rgb_image)
        
        if len(face_locations) == 0:
            messagebox.showerror("Error", "No se detectó ningún rostro en la imagen")
            return None
        elif len(face_locations) > 1:
            messagebox.showwarning("Advertencia", "Se detectaron múltiples rostros. Usando el primero.")
        
        # Obtener el encoding del primer rostro
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        
        if len(face_encodings) > 0:
            # Convertir a bytes para almacenar en la base de datos
            encoding_bytes = pickle.dumps(face_encodings[0])
            return encoding_bytes
        else:
            messagebox.showerror("Error", "No se pudo procesar el rostro")
            return None
            
    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar el rostro: {str(e)}")
        return None

def reconocer_rostro():
    """Reconoce un rostro usando la cámara"""
    if cv2 is None or face_recognition is None or np is None:
        messagebox.showerror("Error", "Librerías de reconocimiento facial no están instaladas.")
        return None
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        messagebox.showerror("Error", "No se puede acceder a la cámara")
        return None
    
    # Obtener todos los encodings del personal registrado
    personal_data = obtener_personal_bd()
    known_encodings = []
    known_names = []
    known_cargos = []
    
    for persona in personal_data:
        if persona[4]:  # Si tiene foto_encoding
            try:
                encoding = pickle.loads(persona[4])
                known_encodings.append(encoding)
                known_names.append(persona[1])  # nombre
                known_cargos.append(persona[2])  # cargo
            except:
                continue
    
    if not known_encodings:
        messagebox.showwarning("Sin personal", "No hay personal registrado con fotos")
        cap.release()
        return None
    
    messagebox.showinfo("Reconocimiento", "Mire a la cámara. Presione ESPACIO para reconocer. ESC para cancelar.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Redimensionar frame para acelerar el procesamiento
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Detectar rostros
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        for face_encoding in face_encodings:
            # Comparar con rostros conocidos
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            
            if True in matches:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    nombre = known_names[best_match_index]
                    cargo = known_cargos[best_match_index]
                    
                    # Dibujar rectángulo alrededor del rostro
                    face_location = face_locations[0]
                    top, right, bottom, left = face_location
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, f"{nombre} - {cargo}", (left, top - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    
                    cv2.imshow('Reconocimiento Facial', frame)
                    cv2.waitKey(2000)  # Mostrar por 2 segundos
                    cv2.destroyAllWindows()
                    cap.release()
                    
                    return (nombre, cargo)
        
        cv2.putText(frame, "Presione ESPACIO para reconocer", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Presione ESC para cancelar", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('Reconocimiento Facial', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # Espacio
            cv2.destroyAllWindows()
            cap.release()
            return None
        elif key == 27:  # ESC
            cv2.destroyAllWindows()
            cap.release()
            return None
    
    cap.release()
    return None

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
#   FUNCIONES FECHA Y HORA
# ============================
def actualizar_fecha_hora():
    """Actualiza la fecha y hora en tiempo real"""
    fecha_actual = datetime.now().strftime("%A, %d de %B de %Y")
    hora_actual = datetime.now().strftime("%H:%M:%S")
    label_fecha.config(text=f"📅 {fecha_actual}")
    label_hora.config(text=f"🕐 {hora_actual}")
    ventana.after(1000, actualizar_fecha_hora)  # Actualizar cada segundo

def obtener_atenciones_por_dia():
    """Obtiene el número de atenciones por día desde la base de datos"""
    conexion = sqlite3.connect("pacientes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT fecha_atencion FROM pacientes")
    fechas = cursor.fetchall()
    conexion.close()
    
    # Contar atenciones por día
    atenciones_por_dia = {}
    for fecha_tupla in fechas:
        fecha_str = fecha_tupla[0]
        try:
            # Parsear la fecha (formato: DD/MM/YYYY HH:MM:SS)
            fecha_obj = datetime.strptime(fecha_str.split()[0], "%d/%m/%Y")
            dia = fecha_obj.day
            mes = fecha_obj.month
            año = fecha_obj.year
            
            clave = (año, mes, dia)
            atenciones_por_dia[clave] = atenciones_por_dia.get(clave, 0) + 1
        except:
            continue
    
    return atenciones_por_dia

def actualizar_calendario():
    """Actualiza el calendario del mes actual con información de atenciones"""
    hoy = datetime.now()
    mes_actual = hoy.month
    año_actual = hoy.year
    
    # Obtener datos de atenciones
    atenciones_por_dia = obtener_atenciones_por_dia()
    
    # Crear el calendario del mes actual
    cal_texto = calendar.month(año_actual, mes_actual)
    
    # Limpiar y mostrar el calendario base
    texto_calendario.delete(1.0, tk.END)
    texto_calendario.insert(tk.END, cal_texto)
    
    # Agregar información de atenciones
    texto_calendario.insert(tk.END, "\n" + "="*50 + "\n")
    texto_calendario.insert(tk.END, "📊 DÍAS CON MÁS ATENCIONES:\n")
    texto_calendario.insert(tk.END, "="*50 + "\n")
    
    # Filtrar atenciones del mes actual
    atenciones_mes_actual = {}
    for (año, mes, dia), count in atenciones_por_dia.items():
        if año == año_actual and mes == mes_actual:
            atenciones_mes_actual[dia] = count
    
    # Mostrar días con atenciones, ordenados por cantidad
    if atenciones_mes_actual:
        dias_ordenados = sorted(atenciones_mes_actual.items(), key=lambda x: x[1], reverse=True)
        
        for dia, cantidad in dias_ordenados:
            if cantidad > 0:
                texto_calendario.insert(tk.END, f"📅 Día {dia:2d}: {cantidad} atenciones")
                if cantidad >= 5:
                    texto_calendario.insert(tk.END, " 🔥 (MUY ALTO)")
                elif cantidad >= 3:
                    texto_calendario.insert(tk.END, " ⚠️ (ALTO)")
                texto_calendario.insert(tk.END, "\n")
    else:
        texto_calendario.insert(tk.END, "📝 No hay atenciones registradas este mes.\n")
    
    # Estadísticas generales
    total_atenciones_mes = sum(atenciones_mes_actual.values())
    if total_atenciones_mes > 0:
        dia_mas_atendido = max(atenciones_mes_actual.items(), key=lambda x: x[1])
        texto_calendario.insert(tk.END, "\n" + "-"*30 + "\n")
        texto_calendario.insert(tk.END, f"📈 Total del mes: {total_atenciones_mes} atenciones\n")
        texto_calendario.insert(tk.END, f"🏆 Día más activo: {dia_mas_atendido[0]} ({dia_mas_atendido[1]} atenciones)\n")
    
    # Actualizar el título del calendario (se actualizará cuando se cree el widget)
    pass

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
    actualizar_calendario()  # Actualizar el calendario con las nuevas estadísticas
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
        actualizar_calendario()  # Actualizar el calendario después de eliminar
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
#   FUNCIONES INTERFAZ CITAS
# ============================
def actualizar_tabla_citas():
    """Actualiza la tabla de citas"""
    try:
        print("Actualizando tabla de citas...")  # Debug
        for fila in tabla_citas.get_children():
            tabla_citas.delete(fila)
        
        citas_data = obtener_citas_bd()
        print(f"Insertando {len(citas_data)} citas en la tabla")  # Debug
        
        for fila in citas_data:
            tabla_citas.insert("", "end", values=fila)
            print(f"Cita insertada: {fila}")  # Debug
        
        print("Tabla de citas actualizada correctamente")  # Debug
    except NameError:
        print("Tabla de citas no existe aún")  # Debug
        # La tabla aún no se ha creado, se actualizará cuando se cree
        pass
    except Exception as e:
        print(f"Error al actualizar tabla de citas: {e}")  # Debug

def reservar_cita():
    """Función principal para reservar una cita"""
    # Crear ventana de reserva de cita
    ventana_cita = tk.Toplevel(ventana)
    ventana_cita.title("📅 Reservar Cita Médica")
    ventana_cita.geometry("500x600")
    ventana_cita.config(bg="#e6f2ff")
    ventana_cita.resizable(False, False)
    ventana_cita.grab_set()  # Hacer la ventana modal
    
    # Centrar la ventana
    ventana_cita.transient(ventana)
    
    # Título
    tk.Label(ventana_cita, text="📅 Reservar Nueva Cita", font=("Arial", 16, "bold"), 
             bg="#e6f2ff", fg="#003366").pack(pady=20)
    
    # Frame principal
    frame_cita = tk.Frame(ventana_cita, bg="#e6f2ff")
    frame_cita.pack(padx=20, pady=10)
    
    # Campos del formulario
    tk.Label(frame_cita, text="Nombre del Paciente:", bg="#e6f2ff", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre_cita = tk.Entry(frame_cita, width=30, font=("Arial", 10))
    entry_nombre_cita.grid(row=0, column=1, pady=5, padx=(10, 0))
    
    tk.Label(frame_cita, text="Teléfono:", bg="#e6f2ff", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
    entry_telefono_cita = tk.Entry(frame_cita, width=30, font=("Arial", 10))
    entry_telefono_cita.grid(row=1, column=1, pady=5, padx=(10, 0))
    
    tk.Label(frame_cita, text="Motivo de Consulta:", bg="#e6f2ff", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=5)
    entry_motivo_cita = tk.Entry(frame_cita, width=30, font=("Arial", 10))
    entry_motivo_cita.grid(row=2, column=1, pady=5, padx=(10, 0))
    
    tk.Label(frame_cita, text="Doctor:", bg="#e6f2ff", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=5)
    combo_doctor_cita = tk.StringVar()
    menu_doctor_cita = tk.OptionMenu(frame_cita, combo_doctor_cita, *doctores_asignados.values())
    menu_doctor_cita.grid(row=3, column=1, sticky="w", pady=5, padx=(10, 0))
    
    tk.Label(frame_cita, text="Fecha de la Cita:", bg="#e6f2ff", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=5)
    entry_fecha_cita = tk.Entry(frame_cita, width=30, font=("Arial", 10))
    entry_fecha_cita.grid(row=4, column=1, pady=5, padx=(10, 0))
    tk.Label(frame_cita, text="(DD/MM/YYYY)", bg="#e6f2ff", font=("Arial", 8)).grid(row=4, column=2, sticky="w", padx=(5, 0))
    
    tk.Label(frame_cita, text="Hora de la Cita:", bg="#e6f2ff", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky="w", pady=5)
    entry_hora_cita = tk.Entry(frame_cita, width=30, font=("Arial", 10))
    entry_hora_cita.grid(row=5, column=1, pady=5, padx=(10, 0))
    tk.Label(frame_cita, text="(HH:MM)", bg="#e6f2ff", font=("Arial", 8)).grid(row=5, column=2, sticky="w", padx=(5, 0))
    
    # Información de ayuda
    frame_info = tk.Frame(ventana_cita, bg="#e6f2ff")
    frame_info.pack(pady=10)
    tk.Label(frame_info, text="💡 Información:", bg="#e6f2ff", font=("Arial", 10, "bold")).pack()
    tk.Label(frame_info, text="• Formato de fecha: DD/MM/YYYY (ej: 15/01/2024)", bg="#e6f2ff", font=("Arial", 9)).pack()
    tk.Label(frame_info, text="• Formato de hora: HH:MM (ej: 14:30)", bg="#e6f2ff", font=("Arial", 9)).pack()
    
    def guardar_cita():
        """Función para guardar la cita"""
        nombre = entry_nombre_cita.get().strip()
        telefono = entry_telefono_cita.get().strip()
        motivo = entry_motivo_cita.get().strip()
        doctor = combo_doctor_cita.get()
        fecha = entry_fecha_cita.get().strip()
        hora = entry_hora_cita.get().strip()
        
        # Validaciones
        if not all([nombre, motivo, doctor, fecha, hora]):
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos obligatorios.")
            return
        
        # Validar formato de fecha
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Usa DD/MM/YYYY")
            return
        
        # Validar formato de hora
        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Formato de hora incorrecto. Usa HH:MM")
            return
        
        # Guardar cita
        if guardar_cita_bd(nombre, telefono, motivo, doctor, fecha, hora):
            actualizar_tabla_citas()
            actualizar_calendario()  # Actualizar estadísticas del calendario
            messagebox.showinfo("Cita reservada", f"✅ Cita reservada exitosamente para {nombre}")
            ventana_cita.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar la cita. Verifique la consola para más detalles.")
    
    # Botones
    frame_botones = tk.Frame(ventana_cita, bg="#e6f2ff")
    frame_botones.pack(pady=20)
    
    tk.Button(frame_botones, text="💾 Reservar Cita", bg="#99ff99", font=("Arial", 10, "bold"), 
              command=guardar_cita).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botones, text="❌ Cancelar", bg="#ff9999", font=("Arial", 10, "bold"), 
              command=ventana_cita.destroy).pack(side=tk.LEFT, padx=10)

def eliminar_cita():
    """Elimina una cita seleccionada"""
    seleccion = tabla_citas.selection()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Por favor, selecciona una cita para eliminar.")
        return
    
    item = tabla_citas.item(seleccion)
    id_cita = item["values"][0]
    nombre = item["values"][1]
    fecha = item["values"][5]
    
    if messagebox.askyesno("Confirmar", f"¿Deseas cancelar la cita de '{nombre}' del {fecha}?"):
        eliminar_cita_bd(id_cita)
        actualizar_tabla_citas()
        actualizar_calendario()  # Actualizar estadísticas
        messagebox.showinfo("Cita cancelada", f"🗑️ Cita de '{nombre}' cancelada correctamente.")

# ============================
#   FUNCIONES INTERFAZ CONTROL DE ASISTENCIA
# ============================
def actualizar_tabla_personal():
    """Actualiza la tabla de personal"""
    try:
        for fila in tabla_personal.get_children():
            tabla_personal.delete(fila)
        for fila in obtener_personal_bd():
            # Mostrar solo ID, Nombre, Cargo, Código, Fecha (sin el encoding)
            datos_mostrar = (fila[0], fila[1], fila[2], fila[3], fila[5])
            tabla_personal.insert("", "end", values=datos_mostrar)
    except NameError:
        pass  # La tabla se creará cuando se abra la ventana de asistencia

def actualizar_tabla_asistencia():
    """Actualiza la tabla de asistencia"""
    try:
        for fila in tabla_asistencia.get_children():
            tabla_asistencia.delete(fila)
        for fila in obtener_asistencia_bd():
            tabla_asistencia.insert("", "end", values=fila)
    except NameError:
        pass  # La tabla se creará cuando se abra la ventana de asistencia

def registrar_personal():
    """Función para registrar nuevo personal"""
    ventana_registro = tk.Toplevel(ventana)
    ventana_registro.title("👥 Registrar Personal")
    ventana_registro.geometry("500x400")
    ventana_registro.config(bg="#f0f8ff")
    ventana_registro.resizable(False, False)
    ventana_registro.grab_set()
    
    # Título
    tk.Label(ventana_registro, text="👥 Registrar Nuevo Personal", 
             font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#2c5aa0").pack(pady=20)
    
    # Frame principal
    frame_registro = tk.Frame(ventana_registro, bg="#f0f8ff")
    frame_registro.pack(padx=20, pady=10)
    
    # Campos del formulario
    tk.Label(frame_registro, text="👤 Nombre completo:", bg="#f0f8ff", 
             font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre_personal = tk.Entry(frame_registro, width=30, font=("Arial", 10))
    entry_nombre_personal.grid(row=0, column=1, pady=5, padx=(10, 0))
    
    tk.Label(frame_registro, text="💼 Cargo:", bg="#f0f8ff", 
             font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=5)
    entry_cargo_personal = tk.Entry(frame_registro, width=30, font=("Arial", 10))
    entry_cargo_personal.grid(row=1, column=1, pady=5, padx=(10, 0))
    
    tk.Label(frame_registro, text="🔢 Código único:", bg="#f0f8ff", 
             font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=5)
    entry_codigo_personal = tk.Entry(frame_registro, width=30, font=("Arial", 10))
    entry_codigo_personal.grid(row=2, column=1, pady=5, padx=(10, 0))
    
    # Información sobre captura de foto
    tk.Label(frame_registro, text="📷 Captura de foto facial:", bg="#f0f8ff", 
             font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=(20, 5))
    
    def capturar_foto():
        nonlocal foto_encoding
        foto = capturar_rostro_para_registro()
        if foto is not None:
            encoding = procesar_rostro_capturado(foto)
            if encoding:
                foto_encoding = encoding
                messagebox.showinfo("Foto capturada", "✅ Foto facial capturada correctamente.")
                return encoding
        return None
    
    # Botón para capturar foto
    btn_capturar = tk.Button(frame_registro, text="📷 Capturar Foto", 
                            bg="#4a90e2", fg="white", font=("Arial", 10, "bold"),
                            command=capturar_foto)
    btn_capturar.grid(row=3, column=1, pady=(20, 5), padx=(10, 0))
    
    foto_encoding = None
    
    def guardar_personal():
        """Función para guardar el personal"""
        nonlocal foto_encoding
        
        nombre = entry_nombre_personal.get().strip()
        cargo = entry_cargo_personal.get().strip()
        codigo = entry_codigo_personal.get().strip()
        
        if not all([nombre, cargo, codigo]):
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return
        
        if foto_encoding is None:
            messagebox.showwarning("Sin foto", "Por favor, captura una foto facial.")
            return
        
        try:
            guardar_personal_bd(nombre, cargo, codigo, foto_encoding)
            actualizar_tabla_personal()
            messagebox.showinfo("Personal registrado", f"✅ Personal '{nombre}' registrado correctamente.")
            ventana_registro.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El código ya existe. Usa un código único.")
    
    # Botones
    frame_botones = tk.Frame(ventana_registro, bg="#f0f8ff")
    frame_botones.pack(pady=20)
    
    tk.Button(frame_botones, text="💾 Guardar Personal", bg="#4caf50", fg="white",
              font=("Arial", 10, "bold"), command=guardar_personal).pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botones, text="❌ Cancelar", bg="#f44336", fg="white",
              font=("Arial", 10, "bold"), command=ventana_registro.destroy).pack(side=tk.LEFT, padx=10)

def control_asistencia():
    """Función principal para el control de asistencia"""
    ventana_asistencia = tk.Toplevel(ventana)
    ventana_asistencia.title("🕐 Control de Asistencia")
    ventana_asistencia.geometry("1000x700")
    ventana_asistencia.config(bg="#f0f8ff")
    ventana_asistencia.resizable(False, False)
    ventana_asistencia.grab_set()
    
    # Título
    tk.Label(ventana_asistencia, text="🕐 Control de Asistencia del Personal", 
             font=("Arial", 18, "bold"), bg="#f0f8ff", fg="#2c5aa0").pack(pady=20)
    
    # Frame principal
    frame_principal_asistencia = tk.Frame(ventana_asistencia, bg="#f0f8ff")
    frame_principal_asistencia.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    # Panel izquierdo - Control de entrada/salida
    frame_control = tk.LabelFrame(frame_principal_asistencia, text="🎯 Control de Entrada/Salida", 
                                 bg="#f0f8ff", font=("Arial", 12, "bold"), fg="#2c5aa0")
    frame_control.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
    
    # Botones de control
    tk.Button(frame_control, text="📷 Registrar Entrada", bg="#4caf50", fg="white",
              font=("Arial", 12, "bold"), command=registrar_entrada_facial,
              width=20, height=2).pack(pady=10, padx=10)
    
    tk.Button(frame_control, text="📷 Registrar Salida", bg="#f44336", fg="white",
              font=("Arial", 12, "bold"), command=registrar_salida_facial,
              width=20, height=2).pack(pady=10, padx=10)
    
    tk.Button(frame_control, text="👥 Registrar Personal", bg="#2196f3", fg="white",
              font=("Arial", 12, "bold"), command=registrar_personal,
              width=20, height=2).pack(pady=10, padx=10)
    
    # Panel derecho - Tablas
    frame_tablas = tk.Frame(frame_principal_asistencia, bg="#f0f8ff")
    frame_tablas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # Tabla de asistencia
    marco_tabla_asistencia = tk.LabelFrame(frame_tablas, text="📊 Registro de Asistencia", 
                                          bg="#f0f8ff", font=("Arial", 11, "bold"), fg="#2c5aa0")
    marco_tabla_asistencia.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    columnas_asistencia = ("ID", "Personal", "Cargo", "Fecha", "Entrada", "Salida", "Estado", "Observaciones")
    tabla_asistencia = ttk.Treeview(marco_tabla_asistencia, columns=columnas_asistencia, show="headings", height=8)
    for col in columnas_asistencia:
        tabla_asistencia.heading(col, text=col)
        tabla_asistencia.column(col, width=100, anchor="center")
    tabla_asistencia.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Tabla de personal
    marco_tabla_personal = tk.LabelFrame(frame_tablas, text="👥 Personal Registrado", 
                                        bg="#f0f8ff", font=("Arial", 11, "bold"), fg="#2c5aa0")
    marco_tabla_personal.pack(fill=tk.X)
    
    columnas_personal = ("ID", "Nombre", "Cargo", "Código", "Fecha Registro")
    tabla_personal = ttk.Treeview(marco_tabla_personal, columns=columnas_personal, show="headings", height=4)
    for col in columnas_personal:
        tabla_personal.heading(col, text=col)
        tabla_personal.column(col, width=120, anchor="center")
    tabla_personal.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # Actualizar tablas
    actualizar_tabla_asistencia()
    actualizar_tabla_personal()

def registrar_entrada_facial():
    """Registra entrada usando reconocimiento facial"""
    resultado = reconocer_rostro()
    if resultado:
        nombre, cargo = resultado
        registrar_entrada_salida(nombre, cargo, "entrada")
        actualizar_tabla_asistencia()

def registrar_salida_facial():
    """Registra salida usando reconocimiento facial"""
    resultado = reconocer_rostro()
    if resultado:
        nombre, cargo = resultado
        registrar_entrada_salida(nombre, cargo, "salida")
        actualizar_tabla_asistencia()

def probar_base_datos_citas():
    """Función de prueba para verificar la base de datos de citas"""
    try:
        # Probar conexión
        conexion = sqlite3.connect("pacientes.db")
        cursor = conexion.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='citas'")
        tabla_existe = cursor.fetchone()
        
        if tabla_existe:
            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM citas")
            count = cursor.fetchone()[0]
            
            # Obtener estructura de la tabla
            cursor.execute("PRAGMA table_info(citas)")
            columnas = cursor.fetchall()
            
            conexion.close()
            
            mensaje = f"✅ Base de datos funcionando correctamente\n\n"
            mensaje += f"📊 Tabla 'citas' encontrada\n"
            mensaje += f"📈 Registros en la tabla: {count}\n\n"
            mensaje += f"🏗️ Estructura de la tabla:\n"
            for col in columnas:
                mensaje += f"   • {col[1]} ({col[2]})\n"
            
            messagebox.showinfo("Prueba de Base de Datos", mensaje)
            
            # Actualizar la tabla
            actualizar_tabla_citas()
            
        else:
            conexion.close()
            messagebox.showerror("Error", "❌ La tabla 'citas' no existe en la base de datos")
            
    except Exception as e:
        messagebox.showerror("Error", f"❌ Error al probar la base de datos:\n{str(e)}")

# ============================
#   INTERFAZ GRÁFICA ORDENADA
# ============================
# Verificar dependencias antes de inicializar la aplicación
if not verificar_dependencias():
    print("\n⚠️  ADVERTENCIA: Algunas dependencias no están instaladas.")
    print("El sistema funcionará sin reconocimiento facial.")
    print("Para habilitar todas las funciones, instale las dependencias.\n")

ventana = tk.Tk()
from tkinter import PhotoImage
ventana.title("MEDICAL CENTER - ELVIS ROJAS")
ventana.geometry("1200x900")  # Ventana más amplia para mejor distribución
ventana.config(bg="#f0f8ff")  # Fondo más suave
ventana.resizable(False, False)

conectar_bd()

# ============================
#   ENCABEZADO PRINCIPAL
# ============================
# Barra superior con título principal
frame_encabezado = tk.Frame(ventana, bg="#2c5aa0", height=60)
frame_encabezado.pack(fill=tk.X, pady=0)
frame_encabezado.pack_propagate(False)

titulo_principal = tk.Label(frame_encabezado, 
                           text="🩺 MEDICAL CENTER - ELVIS ROJAS", 
                           font=("Arial", 18, "bold"), 
                           bg="#2c5aa0", fg="white")
titulo_principal.pack(expand=True)

# Barra de búsqueda de información médica
frame_busqueda = tk.Frame(ventana, bg="#f0f8ff", height=50)
frame_busqueda.pack(fill=tk.X, pady=(10, 5))
frame_busqueda.pack_propagate(False)

tk.Label(frame_busqueda, text="🔍 Buscar Información Médica:", 
         font=("Arial", 10, "bold"), bg="#f0f8ff").pack(side=tk.LEFT, padx=20)
entrada_busqueda = tk.Entry(frame_busqueda, width=25, font=("Arial", 10))
entrada_busqueda.pack(side=tk.LEFT, padx=5)
tk.Button(frame_busqueda, text="🔍 Buscar", command=buscar, 
          bg="#4a90e2", fg="white", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=5)

# ============================
#   CONTENIDO PRINCIPAL
# ============================
frame_principal = tk.Frame(ventana, bg="#f0f8ff")
frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Panel izquierdo - Menú de primeros auxilios
frame_izquierdo = tk.Frame(frame_principal, bg="#f0f8ff", width=220)
frame_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
frame_izquierdo.pack_propagate(False)

# Título del menú
tk.Label(frame_izquierdo, text="🚑 Primeros Auxilios", 
         font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#2c5aa0").pack(pady=(0, 10))

# Botones de primeros auxilios
for situacion in primeros_auxilios.keys():
    btn = tk.Button(frame_izquierdo, text=situacion, width=18, 
                   bg="#e6f3ff", fg="#2c5aa0", font=("Arial", 9, "bold"),
                   command=lambda s=situacion: mostrar_info(s), relief="raised", bd=2)
    btn.pack(pady=3)

# Separador
tk.Frame(frame_izquierdo, bg="#2c5aa0", height=2).pack(fill=tk.X, pady=15)

# Botones de utilidad
tk.Button(frame_izquierdo, text="💾 Guardar", width=18, 
          bg="#4caf50", fg="white", font=("Arial", 9, "bold"),
          command=guardar_contenido, relief="raised", bd=2).pack(pady=3)
tk.Button(frame_izquierdo, text="🖨️ Imprimir", width=18, 
          bg="#ff9800", fg="white", font=("Arial", 9, "bold"),
          command=imprimir, relief="raised", bd=2).pack(pady=3)

# Separador para control de asistencia
tk.Frame(frame_izquierdo, bg="#2c5aa0", height=2).pack(fill=tk.X, pady=10)

# Título del control de asistencia
tk.Label(frame_izquierdo, text="🕐 Control de Asistencia", 
         font=("Arial", 10, "bold"), bg="#f0f8ff", fg="#2c5aa0").pack(pady=(0, 5))

# Botón de control de asistencia
tk.Button(frame_izquierdo, text="🕐 Asistencia", width=18, 
          bg="#9c27b0", fg="white", font=("Arial", 9, "bold"),
          command=control_asistencia, relief="raised", bd=2).pack(pady=3)

# Separador final
tk.Frame(frame_izquierdo, bg="#2c5aa0", height=2).pack(fill=tk.X, pady=10)

tk.Button(frame_izquierdo, text="❌ Salir", width=18, 
          bg="#f44336", fg="white", font=("Arial", 9, "bold"),
          command=salir, relief="raised", bd=2).pack(pady=10)

# Panel central - Gestión de pacientes y citas
frame_central = tk.Frame(frame_principal, bg="#f0f8ff")
frame_central.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

# Panel derecho - Información médica
frame_derecho = tk.Frame(frame_principal, bg="#f0f8ff", width=300)
frame_derecho.pack(side=tk.RIGHT, fill=tk.Y)
frame_derecho.pack_propagate(False)

# Título del panel de información
tk.Label(frame_derecho, text="📋 Información Médica", 
         font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#2c5aa0").pack(pady=(0, 10))

# Cuadro de texto información
texto = tk.Text(frame_derecho, wrap=tk.WORD, width=35, height=25, 
               bg="white", fg="#003366", font=("Arial", 9), relief="sunken", bd=2)
texto.pack(fill=tk.BOTH, expand=True)

# ============================
#   GESTIÓN DE PACIENTES
# ============================
# Marco para tabla de pacientes
marco_tabla = tk.LabelFrame(frame_central, text="👥 Pacientes Registrados", 
                           bg="#f0f8ff", font=("Arial", 11, "bold"), fg="#2c5aa0")
marco_tabla.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

# Tabla de pacientes
columnas = ("ID", "Nombre", "Edad", "Accidente", "Doctor", "Fecha Atención")
tabla_pacientes = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=6)
for col in columnas:
    tabla_pacientes.heading(col, text=col)
    tabla_pacientes.column(col, width=120, anchor="center")
tabla_pacientes.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# ============================
#   GESTIÓN DE CITAS
# ============================
# Marco para tabla de citas
marco_tabla_citas = tk.LabelFrame(frame_central, text="📅 Citas Programadas", 
                                 bg="#f0f8ff", font=("Arial", 11, "bold"), fg="#2c5aa0")
marco_tabla_citas.pack(fill=tk.X, pady=(0, 10))

# Tabla de citas
columnas_citas = ("ID", "Paciente", "Teléfono", "Motivo", "Doctor", "Fecha", "Hora", "Estado")
tabla_citas = ttk.Treeview(marco_tabla_citas, columns=columnas_citas, show="headings", height=4)
for col in columnas_citas:
    tabla_citas.heading(col, text=col)
    tabla_citas.column(col, width=90, anchor="center")
tabla_citas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Botones para gestión de citas
frame_botones_citas = tk.Frame(marco_tabla_citas, bg="#f0f8ff")
frame_botones_citas.pack(fill=tk.X, padx=5, pady=(0, 5))

tk.Button(frame_botones_citas, text="🗑️ Cancelar Cita", bg="#f44336", fg="white",
          font=("Arial", 9, "bold"), command=eliminar_cita).pack(side=tk.RIGHT, padx=(5, 0))
tk.Button(frame_botones_citas, text="🔄 Actualizar", bg="#2196f3", fg="white",
          font=("Arial", 9, "bold"), command=actualizar_tabla_citas).pack(side=tk.RIGHT, padx=(5, 0))
tk.Button(frame_botones_citas, text="🧪 Prueba BD", bg="#ff9800", fg="white",
          font=("Arial", 9, "bold"), command=probar_base_datos_citas).pack(side=tk.RIGHT, padx=(5, 0))

# Actualizar la tabla de citas después de crearla
actualizar_tabla_citas()

# ============================
#   FORMULARIO DE REGISTRO
# ============================
# Marco para registro de pacientes
marco_paciente = tk.LabelFrame(frame_central, text="📝 Registro de Pacientes", 
                              bg="#f0f8ff", font=("Arial", 11, "bold"), fg="#2c5aa0")
marco_paciente.pack(fill=tk.X, pady=(0, 10))

# Frame para campos del formulario
frame_campos = tk.Frame(marco_paciente, bg="#f0f8ff")
frame_campos.pack(fill=tk.X, padx=10, pady=10)

# Fila 1 - Nombre y Accidente
tk.Label(frame_campos, text="👤 Nombre:", bg="#f0f8ff", 
         font=("Arial", 9, "bold")).grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
entry_nombre = tk.Entry(frame_campos, width=20, font=("Arial", 9))
entry_nombre.grid(row=0, column=1, padx=(0, 20), pady=5)

tk.Label(frame_campos, text="🚨 Accidente:", bg="#f0f8ff", 
         font=("Arial", 9, "bold")).grid(row=0, column=2, padx=(0, 5), pady=5, sticky="w")
combo_accidente = tk.StringVar()
entry_accidente = tk.OptionMenu(frame_campos, combo_accidente, *primeros_auxilios.keys())
entry_accidente.config(width=15, font=("Arial", 9))
entry_accidente.grid(row=0, column=3, padx=(0, 20), pady=5)

# Fila 2 - Edad y Doctor
tk.Label(frame_campos, text="🎂 Edad:", bg="#f0f8ff", 
         font=("Arial", 9, "bold")).grid(row=1, column=0, padx=(0, 5), pady=5, sticky="w")
entry_edad = tk.Entry(frame_campos, width=20, font=("Arial", 9))
entry_edad.grid(row=1, column=1, padx=(0, 20), pady=5)

tk.Label(frame_campos, text="👨‍⚕️ Doctor:", bg="#f0f8ff", 
         font=("Arial", 9, "bold")).grid(row=1, column=2, padx=(0, 5), pady=5, sticky="w")
entry_doctor = tk.Entry(frame_campos, width=20, state="readonly", font=("Arial", 9))
entry_doctor.grid(row=1, column=3, padx=(0, 20), pady=5)

# Frame para botones principales
frame_botones_principales = tk.Frame(marco_paciente, bg="#f0f8ff")
frame_botones_principales.pack(fill=tk.X, padx=10, pady=(0, 10))

tk.Button(frame_botones_principales, text="💾 Guardar Paciente", bg="#4caf50", fg="white",
          font=("Arial", 9, "bold"), command=guardar_paciente).pack(side=tk.LEFT, padx=(0, 10))
tk.Button(frame_botones_principales, text="✏️ Editar Paciente", bg="#ff9800", fg="white",
          font=("Arial", 9, "bold"), command=editar_paciente).pack(side=tk.LEFT, padx=(0, 10))
tk.Button(frame_botones_principales, text="🗑️ Borrar Paciente", bg="#f44336", fg="white",
          font=("Arial", 9, "bold"), command=borrar_paciente).pack(side=tk.LEFT, padx=(0, 10))
tk.Button(frame_botones_principales, text="📅 Reservar Cita", bg="#2196f3", fg="white",
          font=("Arial", 9, "bold"), command=reservar_cita).pack(side=tk.LEFT, padx=(0, 10))

# Frame para búsqueda de pacientes
frame_busqueda_pacientes = tk.Frame(marco_paciente, bg="#f0f8ff")
frame_busqueda_pacientes.pack(fill=tk.X, padx=10, pady=(0, 10))

tk.Label(frame_busqueda_pacientes, text="🔍 Buscar paciente:", bg="#f0f8ff", 
         font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=(0, 5))
entry_buscar_paciente = tk.Entry(frame_busqueda_pacientes, width=20, font=("Arial", 9))
entry_buscar_paciente.pack(side=tk.LEFT, padx=(0, 10))
tk.Button(frame_busqueda_pacientes, text="🔍 Consultar", bg="#ff9800", fg="white",
          font=("Arial", 9, "bold"), command=buscar_paciente_tabla).pack(side=tk.LEFT, padx=(0, 10))
tk.Button(frame_busqueda_pacientes, text="🔄 Mostrar Todos", bg="#9c27b0", fg="white",
          font=("Arial", 9, "bold"), command=actualizar_tabla).pack(side=tk.LEFT, padx=(0, 10))

# ============================
#   PIE DE PÁGINA - FECHA, HORA Y CALENDARIO
# ============================
# Separador visual
separador = tk.Frame(ventana, bg="#2c5aa0", height=3)
separador.pack(fill=tk.X, pady=(10, 0))

# Frame principal para fecha, hora y calendario
frame_pie = tk.Frame(ventana, bg="#f0f8ff")
frame_pie.pack(fill=tk.X, padx=10, pady=10)

# Marco para fecha y hora
marco_fecha_hora = tk.Frame(frame_pie, bg="#e8f4fd", relief="ridge", bd=2)
marco_fecha_hora.pack(fill=tk.X, pady=(0, 10))

# Labels para fecha y hora
label_fecha = tk.Label(marco_fecha_hora, text="📅 Fecha", font=("Arial", 11, "bold"), 
                      bg="#e8f4fd", fg="#2c5aa0")
label_fecha.pack(side=tk.LEFT, padx=20, pady=8)

label_hora = tk.Label(marco_fecha_hora, text="🕐 Hora", font=("Arial", 11, "bold"), 
                     bg="#e8f4fd", fg="#2c5aa0")
label_hora.pack(side=tk.RIGHT, padx=20, pady=8)

# Marco para el calendario
marco_calendario = tk.LabelFrame(frame_pie, text="📆 Calendario Médico y Estadísticas", 
                                bg="#f0f8ff", font=("Arial", 11, "bold"), fg="#2c5aa0", 
                                relief="ridge", bd=2)
marco_calendario.pack(fill=tk.X)

# Widget de texto para el calendario
texto_calendario = tk.Text(marco_calendario, wrap=tk.WORD, width=100, height=8, 
                          bg="white", fg="#003366", font=("Courier", 9), relief="sunken", bd=1)
texto_calendario.pack(fill=tk.X, padx=10, pady=(10, 5))

# Botón para actualizar estadísticas del calendario
btn_actualizar_calendario = tk.Button(marco_calendario, text="🔄 Actualizar Estadísticas", 
                                     bg="#4a90e2", fg="white", font=("Arial", 9, "bold"),
                                     command=actualizar_calendario)
btn_actualizar_calendario.pack(pady=(0, 10))

# ============================
#   EJECUCIÓN
# ============================
actualizar_tabla()
actualizar_tabla_citas()  # Actualizar tabla de citas
actualizar_fecha_hora()  # Iniciar la actualización de fecha y hora
actualizar_calendario()  # Mostrar el calendario

# Mensaje de bienvenida
messagebox.showinfo("Bienvenido", 
                   "🩺 MEDICAL CENTER - ELVIS ROJAS\n\n"
                   "Sistema completo de gestión médica con:\n"
                   "• Primeros auxilios\n"
                   "• Gestión de pacientes\n"
                   "• Reserva de citas\n"
                   "• Control de asistencia con reconocimiento facial\n\n"
                   "¡Bienvenido al sistema!")

# Variable global para edición de pacientes
paciente_seleccionado = None

def editar_paciente():
    """Carga los datos del paciente seleccionado en el formulario para edición"""
    global paciente_seleccionado
    seleccion = tabla_pacientes.selection()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Por favor, selecciona un paciente para editar.")
        return
    
    # Obtener datos del paciente seleccionado
    paciente_seleccionado = tabla_pacientes.item(seleccion)['values'][0]  # ID del paciente
    
    # Cargar datos en el formulario
    datos = tabla_pacientes.item(seleccion)['values']
    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, datos[1])  # Nombre
    
    entry_edad.delete(0, tk.END)
    entry_edad.insert(0, datos[2])  # Edad
    
    combo_accidente.set(datos[3])  # Accidente
    
    entry_doctor.config(state="normal")
    entry_doctor.delete(0, tk.END)
    entry_doctor.insert(0, datos[4])  # Doctor
    entry_doctor.config(state="readonly")
    
    # Cambiar el texto del botón de guardar para indicar que estamos en modo edición
    for widget in frame_botones_principales.winfo_children():
        if isinstance(widget, tk.Button) and "Guardar" in widget["text"]:
            widget.config(text="💾 Actualizar Paciente", command=actualizar_paciente)
            return

def actualizar_paciente():
    """Actualiza los datos del paciente en edición"""
    global paciente_seleccionado
    
    if paciente_seleccionado is None:
        messagebox.showwarning("Error", "No hay paciente seleccionado para actualizar.")
        return
    
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
    actualizar_paciente_bd(paciente_seleccionado, nombre, edad, accidente, doctor, fecha_actual)
    
    # Restablecer el botón de guardar
    for widget in frame_botones_principales.winfo_children():
        if isinstance(widget, tk.Button) and "Actualizar" in widget["text"]:
            widget.config(text="💾 Guardar Paciente", command=guardar_paciente)
    
    # Limpiar campos y restablecer variables
    entry_nombre.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    combo_accidente.set("")
    entry_doctor.config(state="normal")
    entry_doctor.delete(0, tk.END)
    entry_doctor.config(state="readonly")
    
    paciente_seleccionado = None
    
    actualizar_tabla()
    actualizar_calendario()
    messagebox.showinfo("Paciente actualizado", f"✅ Paciente '{nombre}' actualizado correctamente.")
