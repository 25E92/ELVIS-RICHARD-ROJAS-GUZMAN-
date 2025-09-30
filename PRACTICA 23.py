# Solicitar al usuario el salario mensual
salario_mensual = float(input("Ingresa tu salario mensual: "))

# Definir la duración en meses y el porcentaje de descuento
meses_trabajados = 6
descuento_porcentaje = 0.10  # 10% de descuento

# Calcular el pago total sin el descuento
pago_total_sin_descuento = salario_mensual * meses_trabajados

# Calcular el monto del descuento
monto_descuento = pago_total_sin_descuento * descuento_porcentaje

# Calcular el pago total con el descuento
pago_total_con_descuento = pago_total_sin_descuento - monto_descuento

# Mostrar los resultados
print("\n--- Resumen de cálculo ---")
print(f"Salario mensual: ${salario_mensual:.2f}")
print(f"Meses trabajados: {meses_trabajados}")
print(f"Pago total (sin descuento): ${pago_total_sin_descuento:.2f}")
print(f"Descuento aplicado (10%): ${monto_descuento:.2f}")
print(f"Pago total (con descuento): ${pago_total_con_descuento:.2f}")
