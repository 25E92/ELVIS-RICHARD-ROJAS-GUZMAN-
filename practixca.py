words = ("CETPRO", "ELVIS")

# Itera sobre cada palabra en la tupla
for word in words:
    # `enumerate()` recorre la palabra y devuelve su índice y el caracter
    for index, char in enumerate(word):
        # Imprime el índice y el carácter, uno al lado del otro
        print(index, char)
