# Cuenta caracteres (con y sin espacios)
t = input("Texto: ")
print("con_espacios:", len(t))
print("sin_espacios:", len(t.replace(' ', '')))
