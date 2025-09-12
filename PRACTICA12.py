def xx(**kwargs):
    for calle, (numero, barrio) in kwargs.items():
        print(calle, numero, barrio)

print('Primero')

xx(
    lima=(1, "bellavista"),
    puno=(2, "laykakota"),
    cusco=(3, "orkapata"),
    losandes=(4, "miraflores"),
    ilave=(5, "elsol"),
    floral=(6, "altoalianza")
)

