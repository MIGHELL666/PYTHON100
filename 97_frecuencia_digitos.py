# Cuenta la frecuencia de cada dígito en un número
n = input("Número grande: ").strip()
for d in "0123456789":
    print(d, n.count(d))
