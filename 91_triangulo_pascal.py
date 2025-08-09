# Imprime el Triángulo de Pascal con n filas
n = int(input("Filas: "))
fila = [1]
for _ in range(n):
    print(" ".join(map(str, fila)))
    fila = [1] + [fila[i] + fila[i+1] for i in range(len(fila)-1)] + [1]
