# Distribución de productos en cajas
total_productos = 82
capacidad_caja = 28
cajas_completas = total_productos // capacidad_caja
productos_sobrantes = total_productos % capacidad_caja
print(f"Cajas completas: {cajas_completas}, Productos sobrantes: {productos_sobrantes}")
