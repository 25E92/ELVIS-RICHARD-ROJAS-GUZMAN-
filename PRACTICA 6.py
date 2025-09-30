def calcular_enesimo_termino_pg(a1, r, n):
    """
    Calcula el n-ésimo término de una progresión geométrica.

    Args:
        a1 (float): El primer término de la progresión.
        r (float): La razón común de la progresión.
        n (int): La posición del término que se desea calcular (n > 0).

    Returns:
        float: El n-ésimo término de la progresión geométrica.
    """
    if n <= 0:
        return "La posición del término (n) debe ser un entero positivo."
    
    # an = a1 * r^(n-1)
    enesimo_termino = a1 * (r ** (n - 1))
    return enesimo_termino

# --- Ejemplos de uso ---

# Ejemplo 1: Una progresión simple (2, 4, 8, 16, ...)
# a1 = 2 (primer término)
# r = 2 (razón común)
# n = 4 (queremos el 4to término)
primer_termino_1 = 2
razon_comun_1 = 2
posicion_n_1 = 4
resultado_1 = calcular_enesimo_termino_pg(primer_termino_1, razon_comun_1, posicion_n_1)
print(f"El {posicion_n_1}-ésimo término de la PG (a1={primer_termino_1}, r={razon_comun_1}) es: {resultado_1}") # Salida esperada: 16

# Ejemplo 2: Otra progresión (3, 9, 27, ...)
# a1 = 3
# r = 3
# n = 3 (queremos el 3er término)
primer_termino_2 = 3
razon_comun_2 = 3
posicion_n_2 = 3
resultado_2 = calcular_enesimo_termino_pg(primer_termino_2, razon_comun_2, posicion_n_2)
print(f"El {posicion_n_2}-ésimo término de la PG (a1={primer_termino_2}, r={razon_comun_2}) es: {resultado_2}") # Salida esperada: 27

# Ejemplo 3: Con razón común negativa (5, -10, 20, -40, ...)
primer_termino_3 = 5
razon_comun_3 = -2
posicion_n_3 = 5
resultado_3 = calcular_enesimo_termino_pg(primer_termino_3, razon_comun_3, posicion_n_3)
print(f"El {posicion_n_3}-ésimo término de la PG (a1={primer_termino_3}, r={razon_comun_3}) es: {resultado_3}") # Salida esperada: 80

# Ejemplo 4: Con n inválido
primer_termino_4 = 1
razon_comun_4 = 2
posicion_n_4 = 0
resultado_4 = calcular_enesimo_termino_pg(primer_termino_4, razon_comun_4, posicion_n_4)
print(f"El {posicion_n_4}-ésimo término de la PG (a1={primer_termino_4}, r={razon_comun_4}) es: {resultado_4}")
