edad = int(input("Dime tu edad: "))
grupo = input("Dime tu grupo [A o B]: ")
if edad >= 18 and grupo == "A" or grupo == "B":
 print("Puedes entrar")
 print("entra al  grupo A asignado")
elif edad < 18 and grupo == "A":
 print("No puedes entrar grupo A, eres menor de edad")
elif edad < 18 and grupo == "B":
 print("Puede entrar, grupo B es para todos")
 print("entra al grupo B asignado")
else:
 print("Elección no válida")
