#Mensaje de bienvenida
print("¡Hola! Aqui podras realizar sumas")
#Leemos un primer número
numero1 = input("Por favor ingrese el primer valor: ")
#Leemos un segundo número
numero2 = input("Por favor ingrese el segundo valor: ")
#Leemos un tercer número
numero3 = input("Por favor ingrese el tercer valor: ")
# En este punto tanto numero1, numero2 y numero3 son string
# Debes entonces convertirlos a números
#numero1 será entero así que usamos int()
numero1 = int(numero1)
#numero2 será un real, así que usamos float()
numero2 = float(numero2)
#numero3 será un real, así que usamos int()
numero3 =int(numero3)
# Mostramos el resultado de la suma
print(numero1, "+", numero2, "+",numero3 "=", numero1 + numero2 + numero3)
