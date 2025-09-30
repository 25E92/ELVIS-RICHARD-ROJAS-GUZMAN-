# Pedir al usuario el numerador
numerador_str = input("Ingresa el numerador: ")

# Pedir al usuario el denominador
denominador_str = input("Ingresa el denominador: ")

# Convertir las entradas a números de punto flotante para permitir decimales
numerador = float(numerador_str)
denominador = float(denominador_str)

# Verificar si el denominador es cero para evitar un error de división por cero
if denominador == 0:
    print("Error: No se puede dividir por cero.")
else:
    # Realizar la división
    resultado = numerador / denominador

    # Comprobar si el resultado es mayor que 10
    if resultado > 10:
        print(f"El resultado de la división es {resultado}, el cual es mayor que 10.")
    else:
        print(f"El resultado de la división es {resultado}, el cual no es mayor que 10.")
