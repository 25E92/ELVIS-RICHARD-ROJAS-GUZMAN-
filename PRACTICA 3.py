# Pedir al usuario la temperatura en Celsius
celsius_str = input("Ingresa la temperatura en grados Celsius: ")

# Convertir la entrada de texto a un número (puede tener decimales)
celsius = float(celsius_str)

# Aplicar la fórmula de conversión: F = C * 9/5 + 32
fahrenheit = (celsius * 9/5) + 32

# Mostrar el resultado
print(f"{celsius}°C equivalen a {fahrenheit}°F")
