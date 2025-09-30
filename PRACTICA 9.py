# Sistema de pedidos
pedidos = []
# Clientes hacen pedidos
pedidos.append("pizza")
pedidos.append("hamburguesa")
pedidos.append("pizza")
pedidos.append("ensalada")
# Revisar cuántas pizzas hay
print("Pizzas pedidas:", pedidos.count("pizza"))
# Eliminar un pedido cancelado
pedidos.remove("ensalada")
# Copiar la lista actual de pedidos
pedidos_backup = pedidos.copy()
# Ordenar los pedidos alfabéticamente
pedidos.sort()
print("Pedidos ordenados:", pedidos)
# Limpiar lista de pedidos al final del día
pedidos.clear()
print("Pedidos del día:", pedidos)
print("Respaldo:", pedidos_backup)
