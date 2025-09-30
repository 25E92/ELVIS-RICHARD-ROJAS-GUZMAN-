import tkinter as tk
from tkinter import filedialog, messagebox

# ---------------- FUNCIONES ----------------
def new_file():
    text_area.delete(1.0, tk.END)

def open_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if filepath:
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, file.read())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

def save_file():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if filepath:
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(text_area.get(1.0, tk.END))
            messagebox.showinfo("Éxito", "Archivo guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

def cut_text():
    text_area.event_generate("<<Cut>>")

def copy_text():
    text_area.event_generate("<<Copy>>")

def paste_text():
    text_area.event_generate("<<Paste>>")

# ---------------- VENTANA PRINCIPAL ----------------
root = tk.Tk()
root.title("Editor de Texto Avanzado")
root.geometry("600x400")

# ---------------- ÁREA DE TEXTO + SCROLL ----------------
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

text_area = tk.Text(frame, wrap="word", undo=True, yscrollcommand=scrollbar.set)
text_area.pack(expand=True, fill="both")

scrollbar.config(command=text_area.yview)

# ---------------- MENÚ ----------------
menubar = tk.Menu(root)

# Menú Archivo
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Nuevo", command=new_file)
file_menu.add_command(label="Abrir", command=open_file)
file_menu.add_command(label="Guardar", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(label="Archivo", menu=file_menu)

# Menú Edición
edit_menu = tk.Menu(menubar, tearoff=0)
edit_menu.add_command(label="Cortar", command=cut_text)
edit_menu.add_command(label="Copiar", command=copy_text)
edit_menu.add_command(label="Pegar", command=paste_text)
menubar.add_cascade(label="Edición", menu=edit_menu)

# Asignar barra de menú
root.config(menu=menubar)

# ---------------- INICIAR ----------------
root.mainloop()
