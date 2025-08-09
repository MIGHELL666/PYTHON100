# Dibuja tablero de ajedrez (ASCII) de NxN
n = int(input("Tamaño del tablero (ej. 8): "))
for i in range(n):
    fila = []
    for j in range(n):
        fila.append("#" if (i + j) % 2 == 0 else ".")
    print("".join(fila))
