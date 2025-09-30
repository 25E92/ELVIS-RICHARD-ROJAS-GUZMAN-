import tkinter as tk
from tkinter import filedialog,messagebox

def open_file():
  filepath = filedialog.askopenfilename()
  if filepath:
     with open(filepath,"r")as file: text_area.delete(1.0,tk.END)
  text_area.insert(tk.END,file.read())
root = tk.Tk()
root.title("Editor de Texto Simple")
text_area = tk.Text(root,wrap="word")
text_area.pack(expand=True,fill="both")
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar,tearoff=0)
file_menu.add_command(label="Abrir",command=open_file)
file_menu.add_command(label="Guardar") # Implementar guardar
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(label="Archivo", menu=file_menu)
                    
root.config(menu=menubar)
root.mainloop()
