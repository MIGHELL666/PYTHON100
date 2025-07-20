"""
Proyecto 23: Reemplazar palabras en un archivo
"""

def reemplazar_en_archivo(nombre_archivo, palabra_original, palabra_nueva, crear_backup=True):
    try:
        # Leer el archivo original
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        
        # Crear backup si se solicita
        if crear_backup:
            nombre_backup = f"{nombre_archivo}.backup"
            with open(nombre_backup, 'w', encoding='utf-8') as backup:
                backup.write(contenido)
            print(f"Backup creado: {nombre_backup}")
        
        # Contar ocurrencias antes del reemplazo
        ocurrencias = contenido.count(palabra_original)
        
        # Realizar el reemplazo
        contenido_nuevo = contenido.replace(palabra_original, palabra_nueva)
        
        # Escribir el archivo modificado
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido_nuevo)
        
        return ocurrencias
        
    except FileNotFoundError:
        return None

def crear_archivo_prueba():
    """Crea un archivo de prueba"""
    contenido = """Python es un lenguaje de programación.
Python es fácil de aprender.
Con Python puedes crear muchas aplicaciones.
Python es muy popular en ciencia de datos."""
    
    with open('texto_prueba.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)
    
    print("Archivo 'texto_prueba.txt' creado para pruebas")

def main():
    print("=== REEMPLAZAR PALABRAS EN ARCHIVO ===")
    
    nombre_archivo = input("Nombre del archivo (o 'prueba' para crear uno): ")
    
    if nombre_archivo.lower() == 'prueba':
        crear_archivo_prueba()
        nombre_archivo = 'texto_prueba.txt'
    
    # Mostrar contenido actual
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido_actual = archivo.read()
        print(f"\nContenido actual del archivo:")
        print(f"'{contenido_actual}'")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
        return
    
    palabra_original = input("\nPalabra a reemplazar: ")
    palabra_nueva = input("Nueva palabra: ")
    
    backup = input("¿Crear backup? (s/n): ").lower() == 's'
    
    ocurrencias = reemplazar_en_archivo(nombre_archivo, palabra_original, palabra_nueva, backup)
    
    if ocurrencias is not None:
        print(f"\nReemplazo completado:")
        print(f"Se reemplazaron {ocurrencias} ocurrencias de '{palabra_original}' por '{palabra_nueva}'")
        
        # Mostrar contenido nuevo
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido_nuevo = archivo.read()
        print(f"\nContenido nuevo:")
        print(f"'{contenido_nuevo}'")
    else:
        print("Error al procesar el archivo")

if __name__ == "__main__":
    main()
