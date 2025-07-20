"""
Proyecto 35: Mostrar la línea más larga de un archivo
"""

def encontrar_linea_mas_larga(nombre_archivo):
    """Encuentra la línea más larga de un archivo"""
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        if not lineas:
            return None
        
        # Encontrar la línea más larga
        linea_mas_larga = max(lineas, key=len)
        numero_linea = lineas.index(linea_mas_larga) + 1
        longitud = len(linea_mas_larga.rstrip())
        
        # Encontrar todas las líneas con la misma longitud máxima
        longitud_maxima = len(linea_mas_larga.rstrip())
        lineas_maximas = []
        
        for i, linea in enumerate(lineas, 1):
            if len(linea.rstrip()) == longitud_maxima:
                lineas_maximas.append((i, linea.rstrip()))
        
        return {
            'linea_mas_larga': linea_mas_larga.rstrip(),
            'numero_linea': numero_linea,
            'longitud': longitud,
            'total_lineas': len(lineas),
            'lineas_maximas': lineas_maximas
        }
        
    except FileNotFoundError:
        return None

def analizar_longitudes_lineas(nombre_archivo):
    """Analiza las longitudes de todas las líneas"""
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        if not lineas:
            return None
        
        longitudes = [len(linea.rstrip()) for linea in lineas]
        
        stats = {
            'total_lineas': len(lineas),
            'longitud_maxima': max(longitudes),
            'longitud_minima': min(longitudes),
            'longitud_promedio': sum(longitudes) / len(longitudes),
            'lineas_vacias': sum(1 for l in longitudes if l == 0),
            'distribucion': {}
        }
        
        # Crear distribución por rangos
        rangos = [(0, 10), (11, 50), (51, 100), (101, 200), (201, float('inf'))]
        for inicio, fin in rangos:
            if fin == float('inf'):
                nombre_rango = f"{inicio}+"
                count = sum(1 for l in longitudes if l >= inicio)
            else:
                nombre_rango = f"{inicio}-{fin}"
                count = sum(1 for l in longitudes if inicio <= l <= fin)
            stats['distribucion'][nombre_rango] = count
        
        return stats
        
    except FileNotFoundError:
        return None

def mostrar_top_lineas_largas(nombre_archivo, top=5):
    """Muestra las N líneas más largas"""
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        if not lineas:
            return []
        
        # Crear lista de (número_línea, contenido, longitud)
        lineas_con_info = []
        for i, linea in enumerate(lineas, 1):
            contenido = linea.rstrip()
            longitud = len(contenido)
            lineas_con_info.append((i, contenido, longitud))
        
        # Ordenar por longitud (descendente)
        lineas_ordenadas = sorted(lineas_con_info, key=lambda x: x[2], reverse=True)
        
        return lineas_ordenadas[:top]
        
    except FileNotFoundError:
        return None

def crear_archivo_lineas_variadas():
    """Crea un archivo con líneas de diferentes longitudes"""
    contenido = """Corta
Esta es una línea un poco más larga que la anterior
X
Esta es una línea considerablemente más larga que contiene mucho más texto para probar la funcionalidad de encontrar la línea más larga del archivo
Línea mediana con texto normal
Esta es la línea más larga de todo el archivo y contiene una gran cantidad de texto para asegurar que sea detectada correctamente por nuestro programa analizador de longitudes de líneas
Otra línea corta
Línea con números: 1234567890 y símbolos: !@#$%^&*()
Final"""
    
    with open('archivo_lineas_variadas.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)
    
    print("Archivo 'archivo_lineas_variadas.txt' creado")

def main():
    print("=== ANALIZADOR DE LÍNEAS MÁS LARGAS ===")
    
    while True:
        print("\n1. Encontrar línea más larga")
        print("2. Análisis completo de longitudes")
        print("3. Top N líneas más largas")
        print("4. Crear archivo de prueba")
        print("5. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                archivo = input("Nombre del archivo: ")
                
                resultado = encontrar_linea_mas_larga(archivo)
                
                if resultado is None:
                    print(f"Error: No se encontró el archivo '{archivo}' o está vacío")
                    continue
                
                print(f"\n=== LÍNEA MÁS LARGA DE: {archivo} ===")
                print(f"Línea número: {resultado['numero_linea']}")
                print(f"Longitud: {resultado['longitud']} caracteres")
                print(f"Contenido: {resultado['linea_mas_larga']}")
                
                if len(resultado['lineas_maximas']) > 1:
                    print(f"\nSe encontraron {len(resultado['lineas_maximas'])} líneas con la longitud máxima:")
                    for num, contenido in resultado['lineas_maximas']:
                        preview = contenido[:50] + "..." if len(contenido) > 50 else contenido
                        print(f"  Línea {num}: {preview}")
            
            elif opcion == 2:
                archivo = input("Nombre del archivo: ")
                
                stats = analizar_longitudes_lineas(archivo)
                
                if stats is None:
                    print(f"Error: No se encontró el archivo '{archivo}' o está vacío")
                    continue
                
                print(f"\n=== ANÁLISIS DE LONGITUDES: {archivo} ===")
                print(f"Total de líneas: {stats['total_lineas']}")
                print(f"Longitud máxima: {stats['longitud_maxima']} caracteres")
                print(f"Longitud mínima: {stats['longitud_minima']} caracteres")
                print(f"Longitud promedio: {stats['longitud_promedio']:.1f} caracteres")
                print(f"Líneas vacías: {stats['lineas_vacias']}")
                
                print(f"\nDistribución por rangos:")
                for rango, cantidad in stats['distribucion'].items():
                    porcentaje = (cantidad / stats['total_lineas']) * 100
                    print(f"  {rango:8} caracteres: {cantidad:3d} líneas ({porcentaje:4.1f}%)")
            
            elif opcion == 3:
                archivo = input("Nombre del archivo: ")
                
                try:
                    top = int(input("¿Cuántas líneas mostrar? (5 por defecto): ") or "5")
                except ValueError:
                    top = 5
                
                resultado = mostrar_top_lineas_largas(archivo, top)
                
                if resultado is None:
                    print(f"Error: No se encontró el archivo '{archivo}' o está vacío")
                    continue
                
                print(f"\n=== TOP {len(resultado)} LÍNEAS MÁS LARGAS: {archivo} ===")
                
                for i, (num_linea, contenido, longitud) in enumerate(resultado, 1):
                    preview = contenido[:60] + "..." if len(contenido) > 60 else contenido
                    print(f"{i:2d}. Línea {num_linea:3d} ({longitud:3d} chars): {preview}")
            
            elif opcion == 4:
                crear_archivo_lineas_variadas()
            
            elif opcion == 5:
                print("¡Hasta luego!")
                break
            
            else:
                print("Opción no válida")
                
        except ValueError:
            print("Error: Ingresa un número válido")
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
