def sum(*args):
    valor = 0
    for n in args:
        valor = valor + n
    return valor
print(sum(10,3))
print(sum(1,2,3))
print(sum(3,2,4,1))
print(sum())
