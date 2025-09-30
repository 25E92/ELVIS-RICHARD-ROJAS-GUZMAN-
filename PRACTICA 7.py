def es_primo(numero):
    """
    Determina si un número es primo.

    Un número primo es un número natural mayor que 1 que no tiene divisores positivos
    más que 1 y él mismo.

    Args:
        numero (int): El número que se desea verificar.

    Returns:
        bool: True si el número es primo, False en caso contrario.
    """
    # Los números menores o iguales a 1 no son primos
    if numero <= 1:
        return False
    # El 2 es el único número par que es primo
    if numero == 2:
        return True
    # Los números pares mayores que 2 no son primos
    if numero % 2 == 0:
        return False
    
    # Para números impares mayores que 2, solo necesitamos verificar divisores impares
    # desde 3 hasta la raíz cuadrada del número.
    # Usamos int(numero**0.5) + 1 para incluir la raíz cuadrada si es un entero.
    # El rango va de 3, saltando de 2 en 2 (solo números impares)
    for i in range(3, int(numero**0.5) + 1, 2):
        if numero % i == 0:
            return False # Si encontramos un divisor, no es primo
            
    return True # Si no encontramos ningún divisor, es primo

# --- Ejemplos de uso ---
print(f"¿Es 7 primo? {es_primo(7)}")      # Salida esperada: True
print(f"¿Es 10 primo? {es_primo(10)}")    # Salida esperada: False
print(f"¿Es 2 primo? {es_primo(2)}")      # Salida esperada: True
print(f"¿Es 1 primo? {es_primo(1)}")      # Salida esperada: False
print(f"¿Es 0 primo? {es_primo(0)}")      # Salida esperada: False
print(f"¿Es 13 primo? {es_primo(13)}")    # Salida esperada: True
print(f"¿Es 17 primo? {es_primo(17)}")    # Salida esperada: True
print(f"¿Es 9 primo? {es_primo(9)}")      # Salida esperada: False (3 * 3)
print(f"¿Es 25 primo? {es_primo(25)}")    # Salida esperada: False (5 * 5)
print(f"¿Es 29 primo? {es_primo(29)}")    # Salida esperada: True
