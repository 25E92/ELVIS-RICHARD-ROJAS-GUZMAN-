import tkinter as tk
import math

# =========================
# FUNCIONES
# =========================
def calculate():
    try:
        expression = entry.get().replace("^", "**")  # Permitir ^ como potencia
        result_value = eval(expression, {"__builtins__": None}, math.__dict__)
        result.set(result_value)
        
        # Guardar en historial
        history_list.insert(tk.END, f"{expression} = {result_value}")
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result_value))  # almacenar último resultado
    except Exception:
        result.set("Error")

def clear_entry():
    entry.delete(0, tk.END)

def insert_text(text):
    entry.insert(tk.END, text)

def use_history(event):
    selected = history_list.get(history_list.curselection())
    expression = selected.split("=")[0].strip()
    entry.delete(0, tk.END)
    entry.insert(tk.END, expression)

# =========================
# INTERFAZ PRINCIPAL
# =========================
root = tk.Tk()
root.title("Calculadora Científica")

# Entrada
entry = tk.Entry(root, width=35, borderwidth=5, font=("Arial", 14))
entry.grid(row=0, column=0, columnspan=6, padx=5, pady=5)

result = tk.StringVar()
tk.Label(root, textvariable=result, font=("Arial", 12), fg="blue").grid(row=1, column=0, columnspan=6)

# =========================
# BOTONES BÁSICOS
# =========================
buttons = [
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("/", 2, 3), ("(", 2, 4), (")", 2, 5),
    ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("*", 3, 3), ("^", 3, 4), ("sqrt", 3, 5),
    ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("-", 4, 3), ("log", 4, 4), ("ln", 4, 5),
    ("0", 5, 0), (".", 5, 1), ("+", 5, 2), ("=", 5, 3), ("pi", 5, 4), ("e", 5, 5),
]

for (text, row, col) in buttons:
    if text == "=":
        tk.Button(root, text=text, command=calculate, width=6, height=2).grid(row=row, column=col, padx=2, pady=2)
    elif text == "sqrt":
        tk.Button(root, text=text, command=lambda: insert_text("math.sqrt("), width=6, height=2).grid(row=row, column=col, padx=2, pady=2)
    elif text == "log":
        tk.Button(root, text=text, command=lambda: insert_text("math.log10("), width=6, height=2).grid(row=row, column=col, padx=2, pady=2)
    elif text == "ln":
        tk.Button(root, text=text, command=lambda: insert_text("math.log("), width=6, height=2).grid(row=row, column=col, padx=2, pady=2)
    elif text == "pi":
        tk.Button(root, text=text, command=lambda: insert_text("math.pi"), width=6, height=2).grid(row=row, column=col, padx=2, pady=2)
    elif text == "e":
        tk.Button(root, text=text, command=lambda: insert_text("math.e"), width=6, height=2).grid(row=row, column=col, padx=2, pady=2)
    else:
        tk.Button(root, text=text, command=lambda t=text: insert_text(t), width=6, height=2).grid(row=row, column=col, padx=2, pady=2)

# =========================
# FUNCIONES TRIGONOMÉTRICAS
# =========================
trig_funcs = [("sin", "math.sin("), ("cos", "math.cos("), ("tan", "math.tan("),
              ("asin", "math.asin("), ("acos", "math.acos("), ("atan", "math.atan(")]

for i, (name, func) in enumerate(trig_funcs):
    tk.Button(root, text=name, command=lambda f=func: insert_text(f), width=6, height=2).grid(row=6, column=i, padx=2, pady=2)

# =========================
# BOTONES EXTRA
# =========================
tk.Button(root, text="C", command=clear_entry, width=14, height=2, bg="red", fg="white").grid(row=7, column=0, columnspan=2, padx=2, pady=2)

# =========================
# HISTORIAL
# =========================
tk.Label(root, text="Historial:", font=("Arial", 12, "bold")).grid(row=8, column=0, columnspan=6)
history_list = tk.Listbox(root, height=8, width=50)
history_list.grid(row=9, column=0, columnspan=6, padx=5, pady=5)
history_list.bind("<<ListboxSelect>>", use_history)

root.mainloop()
