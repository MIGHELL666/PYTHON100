# Genera un nombre de usuario a partir de nombre y apellido
nombre = input("Nombre: ").strip().lower()
apellido = input("Apellido: ").strip().lower()
anio = input("Año de nacimiento (opcional): ").strip()
base = (nombre[0] + apellido).replace(" ", "")
user = base if not anio else base + anio[-2:]
print(user)
