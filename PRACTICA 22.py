nombre = input("Ingresa tu nombre: ")
nombre_completo = ""
for i in nombre:
    nombre_completo += i
    print(f"Pásame la {i}")
print(f"El resultado de la 'suma' es: ¡{nombre_completo.upper()}!")
