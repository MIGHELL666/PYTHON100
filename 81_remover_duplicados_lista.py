# Elimina duplicados preservando orden
v = input("Elementos separados por espacios: ").split()
sin_dups = []
for x in v:
    if x not in sin_dups:
        sin_dups.append(x)
print(" ".join(sin_dups))
