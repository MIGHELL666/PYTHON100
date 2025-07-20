"""
Proyecto 12: Contar vocales en una frase
"""

def contar_vocales(texto):
    vocales = "aeiouAEIOU"
    contador = 0
    vocales_encontradas = {}
    
    for char in texto:
        if char in vocales:
            contador += 1
            vocal = char.lower()
            vocales_encontradas[vocal] = vocales_encontradas.get(vocal, 0) + 1
    
    return contador, vocales_encontradas

def main():
    frase = input("Ingresa una frase: ")
    total_vocales, detalle_vocales = contar_vocales(frase)
    
    print(f"Frase: '{frase}'")
    print(f"Total de vocales: {total_vocales}")
    print("Detalle por vocal:")
    for vocal, cantidad in sorted(detalle_vocales.items()):
        print(f"  {vocal}: {cantidad}")

if __name__ == "__main__":
    main()
