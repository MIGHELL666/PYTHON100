# Valida emails con una expresión regular simple
import re
email = input("Email: ").strip()
regex = r"^[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}$"
print("válido" if re.match(regex, email) else "inválido")
