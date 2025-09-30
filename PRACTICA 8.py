import math

def solve_quadratic_equation(a, b, c):
    """Resuelve una ecuación cuadrática de la forma ax^2 + bx + c = 0.

    Args:
        a: El coeficiente de x^2.
        b: El coeficiente de x.
        c: El término constante.

    Returns:
        Una tupla con las soluciones (x1, x2).
        Devuelve None si la ecuación no tiene soluciones reales.
    """
    # Calcula el discriminante
    delta = (b**2) - 4*(a*c)

    # Verifica si la ecuación tiene soluciones reales
    if delta >= 0:
        # Calcula las dos soluciones
        x1 = (-b - math.sqrt(delta)) / (2*a)
        x2 = (-b + math.sqrt(delta)) / (2*a)
        return (x1, x2)
    else:
        # La ecuación no tiene soluciones reales
        return None

# Ejemplo de uso
a = 1
b = -5
c = 6

soluciones = solve_quadratic_equation(a, b, c)

if soluciones:
    x1, x2 = soluciones
    print(f"Las soluciones son: x1 = {x1}, x2 = {x2}")
else:
    print("La ecuación no tiene soluciones reales.")
