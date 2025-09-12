def read_dict_args(**kwargs):
    for key, value in kwargs.items():
        print('%s - %s' % (key, value))
print('Primero')
read_dict_args(name1='Richard', name2='Rojas', web='Arroba.com')
print('Segundo')
read_dict_args(Team='Alianza Lima', player='Paolo Guerrero', demarcation='FOOTBALLER', number=10)
print('Tercero')
read_dict_args(Uno=1, Dos=2, Tres=3,Cuatro=4)
print('Cuarto')
read_dict_args(nambre='Richard',apellido='Rojas', edad=33,dni="70238453",
correo="elvisrrojas@gmail.com")
