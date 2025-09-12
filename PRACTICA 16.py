def tabla_del(numero):
     resultados = []
     for i in range(15):
         resultados.append(numero * i)
     return resultados
res = tabla_del(5)
print(res)
