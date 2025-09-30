usuario = "admin"
contrasena = "segura123"
es_usuario_valido = len(usuario) > 0 and len(contrasena)>= 8
print(es_usuario_valido)  # Salida:  True
