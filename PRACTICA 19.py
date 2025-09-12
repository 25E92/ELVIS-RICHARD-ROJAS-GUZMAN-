def elvis():
  num=int(input("que producto compraste 1)Zapatillas 2)Buzos 3)Camisetas 4)otros; "))
  total=int(input("cuanto costo S/.? : "))
  if num==1:
    im=20
  elif num==2:
    im=20
  elif num==3:
    im=30
  else:
    im=70
  impu=(total*im/200)
  print('impuesto de ese producto es S/.: ',impu)
#  print(impu)
  return impu
elvis()
print("Programa terminado")
