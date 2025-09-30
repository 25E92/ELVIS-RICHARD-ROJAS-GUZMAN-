edad = int(input("¿Cuabtos años tiene? "))
jubilado = -65 + edad

if edad <= 65:
    print("Usted sigue laborando")
else:
    print(f"Usted ya se jubilo hace {jubilado} años")
