# Mezcla dos listas intercalando elementos
a = input("Lista A (espacios): ").split()
b = input("Lista B (espacios): ").split()
res = []
for i in range(max(len(a), len(b))):
    if i < len(a): res.append(a[i])
    if i < len(b): res.append(b[i])
print(" ".join(res))
