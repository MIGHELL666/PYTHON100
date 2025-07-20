"""
Proyecto 21: Contar palabras en una frase
"""

def contar_palabras(frase):
    # Método simple
    palabras = frase.split()
    return len(palabras)

def contar_palabras_detallado(frase):
    # Análisis más detallado
    palabras = frase.split()
    
    # Limpiar signos de puntuación básicos
    palabras_limpias = []
    for palabra in palabras:
        palabra_limpia = palabra.strip('.,!?;:"()[]{}')
        if palabra_limpia:  # Solo agregar si no está vacía
            palabras_limpias.append(palabra_limpia.lower())
    
    # Contar frecuencias
    frecuencias = {}
    for palabra in palabras_limpias:
        frecuencias[palabra] = frecuencias.get(palabra, 0) + 1
    
    return len(palabras_limpias), frecuencias

def main():
    frase = input("Ingresa una frase: ")
    
    # Conteo simple
    total_palabras = contar_palabras(frase)
    print(f"Frase: '{frase}'")
    print(f"Total de palabras: {total_palabras}")
    
    # Análisis detallado
    total_limpias, frecuencias = contar_palabras_detallado(frase)
    print(f"Palabras únicas: {len(frecuencias)}")
    
    print("\nFrecuencia de palabras:")
    for palabra, freq in sorted(frecuencias.items()):
        print(f"  '{palabra}': {freq}")
    
    # Estadísticas adicionales
    if frecuencias:
        palabra_mas_comun = max(frecuencias, key=frecuencias.get)
        print(f"\nPalabra más común: '{palabra_mas_comun}' ({frecuencias[palabra_mas_comun]} veces)")

if __name__ == "__main__":
    main()
