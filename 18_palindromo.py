"""
Proyecto 18: Determinar si una palabra es palíndromo
"""

def es_palindromo(texto):
    # Limpiar el texto: quitar espacios y convertir a minúsculas
    texto_limpio = ''.join(texto.lower().split())
    # Comparar con su reverso
    return texto_limpio == texto_limpio[::-1]

def es_palindromo_manual(texto):
    texto_limpio = ''.join(texto.lower().split())
    longitud = len(texto_limpio)
    
    for i in range(longitud // 2):
        if texto_limpio[i] != texto_limpio[longitud - 1 - i]:
            return False
    return True

def main():
    texto = input("Ingresa una palabra o frase: ")
    
    if es_palindromo(texto):
        print(f"'{texto}' ES un palíndromo")
    else:
        print(f"'{texto}' NO es un palíndromo")
    
    # Ejemplos de palíndromos
    ejemplos = ["oso", "anita lava la tina", "A man a plan a canal Panama", "12321"]
    print("\nEjemplos de palíndromos:")
    for ejemplo in ejemplos:
        resultado = "SÍ" if es_palindromo(ejemplo) else "NO"
        print(f"'{ejemplo}' -> {resultado}")

if __name__ == "__main__":
    main()
