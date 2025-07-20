"""
Proyecto 27: Leer archivo línea por línea
"""

def leer_archivo_linea_por_linea(nombre_archivo, mostrar_numeros=True, pausar=False):
    """Lee un archivo línea por línea con opciones de visualización"""
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            print(f"=== LEYENDO: {nombre_archivo} ===\n")
            
            for num_linea, linea in enumerate(archivo, 1):
                if mostrar_numeros:
                    print(f"{num_linea:3d}: {linea.rstrip()}")
                else:
                    print(linea.rstrip())
                
                if pausar and num_linea % 5 == 0:
                    input(f"\n[Presiona Enter para continuar... (línea {num_linea})]")
            
            return num_linea
            
    except FileNotFoundError:
        return None

def analizar_archivo(nombre_archivo):
    """Analiza estadísticas del archivo"""
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        total_lineas = len(lineas)
        lineas_vacias = sum(1 for linea in lineas if linea.strip() == '')
        lineas_con_contenido = total_lineas - lineas_vacias
        
        if lineas:
            linea_mas_larga = max(lineas, key=len)
            linea_mas_corta = min((l for l in lineas if l.strip()), key=len, default="")
        else:
            linea_mas_larga = linea_mas_corta = ""
        
        return {
            'total_lineas': total_lineas,
            'lineas_vacias': lineas_vacias,
            'lineas_con_contenido': lineas_con_contenido,
            'linea_mas_larga': linea_mas_larga.strip(),
            'linea_mas_corta': linea_mas_corta.strip(),
            'longitud_maxima': len(linea_mas_larga),
            'longitud_minima': len(linea_mas_corta.strip()) if linea_mas_corta.strip() else 0
        }
        
    except FileNotFoundError:
        return None

def crear_archivo_lectura():
    """Crea un archivo para pruebas de lectura"""
    contenido = """Este es un archivo de prueba para lectura línea por línea.
Contiene diferentes tipos de líneas.

Esta línea está después de una línea vacía.
Esta es una línea muy larga que contiene mucho texto para probar cómo se maneja el contenido extenso en nuestro lector de archivos.
Corta.
Línea con números: 12345
Línea con símbolos: !@#$%^&*()
Última línea del archivo."""
    
    with open('lectura_prueba.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)
    
    print("Archivo 'lectura_prueba.txt' creado")

def main():
    print("=== LECTOR DE ARCHIVOS LÍNEA POR LÍNEA ===")
    
    nombre_archivo = input("Nombre del archivo (o 'prueba' para crear uno): ")
    
    if nombre_archivo.lower() == 'prueba':
        crear_archivo_lectura()
        nombre_archivo = 'lectura_prueba.txt'
    
    # Opciones de lectura
    print("\nOpciones de lectura:")
    mostrar_numeros = input("¿Mostrar números de línea? (s/n): ").lower() != 'n'
    pausar = input("¿Pausar cada 5 líneas? (s/n): ").lower() == 's'
    
    # Leer archivo
    total_lineas = leer_archivo_linea_por_linea(nombre_archivo, mostrar_numeros, pausar)
    
    if total_lineas is None:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
        return
    
    print(f"\n=== LECTURA COMPLETADA ===")
    print(f"Total de líneas leídas: {total_lineas}")
    
    # Análisis adicional
    if input("\n¿Mostrar análisis del archivo? (s/n): ").lower() == 's':
        stats = analizar_archivo(nombre_archivo)
        if stats:
            print(f"\n=== ANÁLISIS DEL ARCHIVO ===")
            print(f"Total de líneas: {stats['total_lineas']}")
            print(f"Líneas vacías: {stats['lineas_vacias']}")
            print(f"Líneas con contenido: {stats['lineas_con_contenido']}")
            print(f"Línea más larga ({stats['longitud_maxima']} chars): {stats['linea_mas_larga'][:50]}...")
            print(f"Línea más corta ({stats['longitud_minima']} chars): {stats['linea_mas_corta']}")

if __name__ == "__main__":
    main()
