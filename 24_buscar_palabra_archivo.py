"""
Proyecto 24: Buscar una palabra en un archivo
"""

def buscar_palabra_en_archivo(nombre_archivo, palabra_buscar, case_sensitive=False):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        resultados = []
        palabra_buscar_proc = palabra_buscar if case_sensitive else palabra_buscar.lower()
        
        for num_linea, linea in enumerate(lineas, 1):
            linea_proc = linea if case_sensitive else linea.lower()
            
            if palabra_buscar_proc in linea_proc:
                # Encontrar todas las posiciones en la línea
                posiciones = []
                start = 0
                while True:
                    pos = linea_proc.find(palabra_buscar_proc, start)
                    if pos == -1:
                        break
                    posiciones.append(pos)
                    start = pos + 1
                
                resultados.append({
                    'linea': num_linea,
                    'contenido': linea.strip(),
                    'posiciones': posiciones,
                    'ocurrencias': len(posiciones)
                })
        
        return resultados
        
    except FileNotFoundError:
        return None

def crear_archivo_busqueda():
    """Crea un archivo para pruebas de búsqueda"""
    contenido = """La programación es el arte de resolver problemas.
Python es un lenguaje de programación muy popular.
Los programadores usan Python para muchas tareas.
La programación requiere práctica y paciencia.
Python facilita la programación orientada a objetos."""
    
    with open('busqueda_prueba.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)
    
    print("Archivo 'busqueda_prueba.txt' creado")

def main():
    print("=== BUSCAR PALABRA EN ARCHIVO ===")
    
    nombre_archivo = input("Nombre del archivo (o 'prueba' para crear uno): ")
    
    if nombre_archivo.lower() == 'prueba':
        crear_archivo_busqueda()
        nombre_archivo = 'busqueda_prueba.txt'
    
    palabra = input("Palabra a buscar: ")
    case_sensitive = input("¿Búsqueda sensible a mayúsculas? (s/n): ").lower() == 's'
    
    resultados = buscar_palabra_en_archivo(nombre_archivo, palabra, case_sensitive)
    
    if resultados is None:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
        return
    
    if not resultados:
        print(f"No se encontró la palabra '{palabra}' en el archivo")
        return
    
    total_ocurrencias = sum(r['ocurrencias'] for r in resultados)
    print(f"\nSe encontró '{palabra}' {total_ocurrencias} vez(es) en {len(resultados)} línea(s):")
    
    for resultado in resultados:
        print(f"\nLínea {resultado['linea']} ({resultado['ocurrencias']} ocurrencia(s)):")
        print(f"  {resultado['contenido']}")
        print(f"  Posiciones: {resultado['posiciones']}")

if __name__ == "__main__":
    main()
