# Solicitar al usuario el primer número
num1_str = input("Ingresa el primer número: ")

# Solicitar al usuario el segundo número
num2_str = input("Ingresa el segundo número: ")

# Convertir las entradas de cadena a números (enteros o flotantes)
# Usamos float() para permitir números con decimales. Si solo quieres enteros, usa int().
num1 = float(num1_str)
num2 = float(num2_str)

# Realizar la suma
suma = num1 + num2

# Mostrar el resultado
print(f"La suma de {num1} y {num2} es: {suma}")
