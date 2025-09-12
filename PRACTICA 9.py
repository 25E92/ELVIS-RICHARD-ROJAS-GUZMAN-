def read_list_args(*args):
    for count, arg in enumerate(args):
        print( '%d - %s' % (count, arg))
read_list_args('Elvis', 'Arroba.com')
read_list_args('Elvis', 25, 'Rojas', [4, 5, 6], 'Arroba.com')
read_list_args(33,"Elvis",10.10,(5,2,0), 'cetpropuno.edu.pe',0,25,6)
read_list_args(25,"Elvis Rojas",25.50,(5,2,0), 'mariano.melgar.edu.pe',0,25,6)
