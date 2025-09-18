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