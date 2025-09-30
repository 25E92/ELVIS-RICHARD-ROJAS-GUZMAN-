def calcular_doble_si_par(numero):
    """
    Calcula el doble de un número solo si es par.

    Args:
        numero (int o float): El número que se desea procesar.

    Returns:
        int o float: El doble del número si es par.
                      Retorna el mensaje "El número no es par." si es impar.
    """
    if numero % 2 == 0:  # Comprueba si el número es par
        return numero * 2
    else:
        return "El número no es par."

# --- Ejemplos de uso ---
print(calcular_doble_si_par(4))   # Salida: 8
print(calcular_doble_si_par(7))   # Salida: El número no es par.
print(calcular_doble_si_par(10))  # Salida: 20
print(calcular_doble_si_par(3))   # Salida: El número no es par.
print(calcular_doble_si_par(0))   # Salida: 0 (0 es un número par)
