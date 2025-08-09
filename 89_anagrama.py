# Verifica si dos palabras/frases son anagramas (ignora espacios y mayúsculas)
a = "".join(input("Texto 1: ").lower().split())
b = "".join(input("Texto 2: ").lower().split())
print("anagrama" if sorted(a)==sorted(b) else "no_anagrama")
