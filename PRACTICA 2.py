# Pedir al usuario la longitud de la base
base_str = input("Ingresa la longitud de la base del rectángulo: ")

# Pedir al usuario la altura del rectángulo
altura_str = input("Ingresa la altura del rectángulo: ")

# Convertir las entradas (que son texto) a números.
# Usamos float() para permitir valores decimales.
base = float(base_str)
altura = float(altura_str)

# Calcular el área usando la fórmula: base * altura
area = base * altura

# Mostrar el resultado al usuario
print(f"El área del rectángulo con base {base} y altura {altura} es: {area}")
