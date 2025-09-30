import tkinter as tk
import math

def calculate():
 try:
    result.set(eval(entry.get()))
 except Exception:
   result.set("Error")
   
root = tk.Tk()
root.title("Calculadora Científica")
entry = tk.Entry(root, width=40,borderwidth=5)
entry.grid(row=0, column=0,columnspan=4)
result = tk.StringVar()
tk.Label(root,textvariable=result).grid(row=1,
column=0, columnspan=4)

# Ejemplo de botones(simplificado)
tk.Button(root, text="7",
command=lambda:
entry.insert(tk.END,"7")).grid(row=2, column=0)
tk.Button(root, text="+",command=lambda:
entry.insert(tk.END,"+")).grid(row=2, column=3)
tk.Button(root, text="=",command=calculate).grid(row=5, column=3)
tk.Button(root, text="sin",
command=lambda:
entry.insert(tk.END,
"math.sin(")).grid(row=5,
column=0)
root.mainloop()
