def tabla_del(numero):
     resultados = []
     for i in range(11):
         resultados.append(numero * i)
     return resultados
res = tabla_del(3)
print(res)
