"""
Proyecto 22: Contar caracteres de un archivo .txt
"""

def contar_caracteres_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            
        # Conteos
        total_caracteres = len(contenido)
        caracteres_sin_espacios = len(contenido.replace(' ', '').replace('\n', '').replace('\t', ''))
        espacios = contenido.count(' ')
        saltos_linea = contenido.count('\n')
        lineas = len(contenido.split('\n'))
        
        return {
            'total_caracteres': total_caracteres,
            'caracteres_sin_espacios': caracteres_sin_espacios,
            'espacios': espacios,
            'saltos_linea': saltos_linea,
            'lineas': lineas,
            'contenido': contenido
        }
    except FileNotFoundError:
        return None

def crear_archivo_ejemplo():
    """Crea un archivo de ejemplo para probar"""
    contenido_ejemplo = """Este es un archivo de ejemplo.
Contiene varias líneas de texto.
Podemos contar caracteres, espacios y líneas.
¡Perfecto para probar nuestro contador!"""
    
    with open('ejemplo.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(contenido_ejemplo)
    
    print("Archivo 'ejemplo.txt' creado para pruebas")

def main():
    print("=== CONTADOR DE CARACTERES EN ARCHIVO ===")
    
    nombre_archivo = input("Ingresa el nombre del archivo (o 'ejemplo' para crear uno): ")
    
    if nombre_archivo.lower() == 'ejemplo':
        crear_archivo_ejemplo()
        nombre_archivo = 'ejemplo.txt'
    
    resultado = contar_caracteres_archivo(nombre_archivo)
    
    if resultado is None:
        print(f"Error: No se pudo encontrar el archivo '{nombre_archivo}'")
        return
    
    print(f"\nEstadísticas del archivo '{nombre_archivo}':")
    print(f"Total de caracteres: {resultado['total_caracteres']}")
    print(f"Caracteres sin espacios: {resultado['caracteres_sin_espacios']}")
    print(f"Espacios: {resultado['espacios']}")
    print(f"Saltos de línea: {resultado['saltos_linea']}")
    print(f"Número de líneas: {resultado['lineas']}")
    
    print(f"\nPrimeros 100 caracteres del archivo:")
    print(f"'{resultado['contenido'][:100]}{'...' if len(resultado['contenido']) > 100 else ''}'")

if __name__ == "__main__":
    main()
