# Convierte km/h a m/s y viceversa
modo = input("k->m o m->k: ").strip().lower()
v = float(input("Valor: "))
if modo == "k->m":
    print(v/3.6)
elif modo == "m->k":
    print(v*3.6)
else:
    print("Modo no reconocido")
