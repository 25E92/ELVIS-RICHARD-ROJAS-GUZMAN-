# Cálculo de interés compuesto
capital_inicial = 10000.00
tasa_interes = 0.05 # 5 % anual
periodos = 3
monto_final = capital_inicial * (1 + tasa_interes) ** periodos
print(f"Monto final: ${monto_final:.3f}")
