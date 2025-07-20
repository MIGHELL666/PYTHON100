"""
Proyecto 11: Invertir una cadena
"""

def invertir_cadena(texto):
    return texto[::-1]

def invertir_cadena_manual(texto):
    resultado = ""
    for i in range(len(texto) - 1, -1, -1):
        resultado += texto[i]
    return resultado

def main():
    texto = input("Ingresa una cadena de texto: ")
    
    # Método 1: Usando slicing
    invertida1 = invertir_cadena(texto)
    print(f"Texto original: {texto}")
    print(f"Texto invertido (método 1): {invertida1}")
    
    # Método 2: Manual
    invertida2 = invertir_cadena_manual(texto)
    print(f"Texto invertido (método 2): {invertida2}")

if __name__ == "__main__":
    main()
