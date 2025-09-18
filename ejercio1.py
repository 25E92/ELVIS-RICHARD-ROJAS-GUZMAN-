"""Ejemplos de aplicación de conjuntos en Python
Demuestra las principales operaciones y funcionalidades de los conjuntos
"""

"""Ejemplos básicos de creación y operaciones con conjuntos"""
print("=== EJEMPLOS BÁSICOS DE CONJUNTOS ===\n")
    
    # Creación de conjuntos
print("1. Creación de conjuntos:")
conjunto1 = {1, 2, 3, 4, 5}
conjunto2 = {4, 5, 6, 7, 8}
conjunto3 = set([1, 2, 3, 2, 4, 5, 1])  # Los duplicados se eliminan automáticamente
    
print(f"Conjunto 1: {conjunto1}")
print(f"Conjunto 2: {conjunto2}")
print(f"Conjunto 3 (desde lista): {conjunto3}")
print(f"Tamaño del conjunto 1: {len(conjunto1)}")
print()

def operaciones_conjuntos():
    """Operaciones principales entre conjuntos"""
    print("=== OPERACIONES ENTRE CONJUNTOS ===\n")
    
    conjunto1 = {1, 2, 3, 4, 5}
    conjunto2 = {4, 5, 6, 7, 8}
    
    print(f"Conjunto A: {conjunto1}")
    print(f"Conjunto B: {conjunto2}")
    print()
    
    # Unión
    union = conjunto1 | conjunto2
    print(f"Unión (A ∪ B): {union}")
    
    # Intersección
    interseccion = conjunto1 & conjunto2
    print(f"Intersección (A ∩ B): {interseccion}")
    
    # Diferencia
    diferencia_ab = conjunto1 - conjunto2
    diferencia_ba = conjunto2 - conjunto1
    print(f"Diferencia (A - B): {diferencia_ab}")
    print(f"Diferencia (B - A): {diferencia_ba}")
    
    # Diferencia simétrica
    diferencia_simetrica = conjunto1 ^ conjunto2
    print(f"Diferencia simétrica (A △ B): {diferencia_simetrica}")
    print()

def metodos_conjuntos():
    """Métodos útiles de los conjuntos"""
    print("=== MÉTODOS DE CONJUNTOS ===\n")
    
    conjunto = {1, 2, 3, 4, 5}
    print(f"Conjunto original: {conjunto}")
    
    # Agregar elementos
    conjunto.add(6)
    print(f"Después de add(6): {conjunto}")
    
    # Agregar múltiples elementos
    conjunto.update([7, 8, 9])
    print(f"Después de update([7, 8, 9]): {conjunto}")
    
    # Eliminar elementos
    conjunto.remove(9)  # Lanza excepción si no existe
    print(f"Después de remove(9): {conjunto}")
    
    conjunto.discard(10)  # No lanza excepción si no existe
    print(f"Después de discard(10): {conjunto}")
    
    # Pop (elimina y retorna un elemento aleatorio)
    elemento = conjunto.pop()
    print(f"Elemento eliminado con pop(): {elemento}")
    print(f"Conjunto después de pop(): {conjunto}")
    
    # Limpiar conjunto
    conjunto.clear()
    print(f"Después de clear(): {conjunto}")
    print()

def relaciones_conjuntos():
    """Verificación de relaciones entre conjuntos"""
    print("=== RELACIONES ENTRE CONJUNTOS ===\n")
    
    conjunto1 = {1, 2, 3}
    conjunto2 = {1, 2, 3, 4, 5}
    conjunto3 = {4, 5, 6}
    
    print(f"Conjunto A: {conjunto1}")
    print(f"Conjunto B: {conjunto2}")
    print(f"Conjunto C: {conjunto3}")
    print()
    
    # Subconjunto
    print(f"A es subconjunto de B: {conjunto1.issubset(conjunto2)}")
    print(f"A ⊆ B: {conjunto1 <= conjunto2}")
    print(f"A es subconjunto propio de B: {conjunto1 < conjunto2}")
    
    # Superconjunto
    print(f"B es superconjunto de A: {conjunto2.issuperset(conjunto1)}")
    print(f"B ⊇ A: {conjunto2 >= conjunto1}")
    
    # Disjuntos
    print(f"A y C son disjuntos: {conjunto1.isdisjoint(conjunto3)}")
    print()

def aplicacion_practica():
    """Aplicación práctica: análisis de datos"""
    print("=== APLICACIÓN PRÁCTICA: ANÁLISIS DE DATOS ===\n")
    
    # Simulación de datos de usuarios
    usuarios_activos_enero = {"Ana", "Carlos", "María", "Luis", "Sofia"}
    usuarios_activos_febrero = {"Ana", "María", "Pedro", "Sofia", "Diego"}
    usuarios_premium = {"Ana", "Carlos", "Pedro", "Elena"}
    
    print("Datos de usuarios:")
    print(f"Usuarios activos en enero: {usuarios_activos_enero}")
    print(f"Usuarios activos en febrero: {usuarios_activos_febrero}")
    print(f"Usuarios premium: {usuarios_premium}")
    print()
    
    # Análisis
    print("Análisis:")
    
    # Usuarios activos en ambos meses
    usuarios_consistentes = usuarios_activos_enero & usuarios_activos_febrero
    print(f"Usuarios activos en ambos meses: {usuarios_consistentes}")
    
    # Nuevos usuarios en febrero
    nuevos_febrero = usuarios_activos_febrero - usuarios_activos_enero
    print(f"Nuevos usuarios en febrero: {nuevos_febrero}")
    
    # Usuarios que dejaron de ser activos
    usuarios_perdidos = usuarios_activos_enero - usuarios_activos_febrero
    print(f"Usuarios que dejaron de ser activos: {usuarios_perdidos}")
    
    # Usuarios premium activos en febrero
    premium_activos = usuarios_premium & usuarios_activos_febrero
    print(f"Usuarios premium activos en febrero: {premium_activos}")
    
    # Todos los usuarios únicos
    todos_usuarios = usuarios_activos_enero | usuarios_activos_febrero | usuarios_premium
    print(f"Total de usuarios únicos: {len(todos_usuarios)}")
    print()

def conjuntos_inmutables():
    """Ejemplo con conjuntos inmutables (frozenset)"""
    print("=== CONJUNTOS INMUTABLES (FROZENSET) ===\n")
    
    # Creación de frozenset
    conjunto_inmutable = frozenset([1, 2, 3, 4, 5])
    print(f"Frozenset: {conjunto_inmutable}")
    print(f"Tipo: {type(conjunto_inmutable)}")
    
    # Se puede usar como clave en diccionarios
    diccionario = {conjunto_inmutable: "Valor asociado"}
    print(f"Usado como clave en diccionario: {diccionario}")
    
    # Operaciones válidas
    otro_conjunto = frozenset([4, 5, 6, 7, 8])
    union = conjunto_inmutable | otro_conjunto
    print(f"Unión con otro frozenset: {union}")
    print()

def ejemplo_eliminacion_duplicados():
    """Ejemplo práctico: eliminación de duplicados"""
    print("=== ELIMINACIÓN DE DUPLICADOS ===\n")
    
    # Lista con elementos duplicados
    lista_con_duplicados = [1, 2, 2, 3, 4, 4, 5, 5, 5, 6]
    print(f"Lista original: {lista_con_duplicados}")
    
    # Convertir a conjunto para eliminar duplicados
    conjunto_sin_duplicados = set(lista_con_duplicados)
    print(f"Conjunto sin duplicados: {conjunto_sin_duplicados}")
    
    # Convertir de vuelta a lista si es necesario
    lista_sin_duplicados = list(conjunto_sin_duplicados)
    print(f"Lista sin duplicados: {lista_sin_duplicados}")
    print()

def main():
    """Función principal que ejecuta todos los ejemplos"""
    print("PROGRAMACIÓN CON CONJUNTOS EN PYTHON")
    print("=" * 50)
    print()
    
    ejemplos_basicos_conjuntos()
    operaciones_conjuntos()
    metodos_conjuntos()
    relaciones_conjuntos()
    aplicacion_practica()
    conjuntos_inmutables()
    ejemplo_eliminacion_duplicados()
    
    print("¡Fin de los ejemplos de conjuntos!")

if __name__ == "__main__":
    main()