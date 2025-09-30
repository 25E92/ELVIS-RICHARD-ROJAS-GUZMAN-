# Usuarios registrados en dos plataformas
usuarios_A = ["Ana", "Luis"]
usuarios_B = ["María", "Pedro"]
# Combinar con extend
usuarios_A.extend(usuarios_B)
print(usuarios_A) # ['Ana', 'Luis', 'María', 'Pedro']
