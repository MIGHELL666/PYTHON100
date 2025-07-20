"""
Proyecto 34: Comparar dos archivos línea por línea
"""

def comparar_archivos_linea_por_linea(archivo1, archivo2):
    """Compara dos archivos línea por línea"""
    try:
        with open(archivo1, 'r', encoding='utf-8') as f1:
            lineas1 = f1.readlines()
        
        with open(archivo2, 'r', encoding='utf-8') as f2:
            lineas2 = f2.readlines()
        
        # Información básica
        info = {
            'archivo1': archivo1,
            'archivo2': archivo2,
            'lineas_archivo1': len(lineas1),
            'lineas_archivo2': len(lineas2),
            'son_identicos': False,
            'diferencias': [],
            'lineas_solo_archivo1': [],
            'lineas_solo_archivo2': []
        }
        
        # Comparar línea por línea
        max_lineas = max(len(lineas1), len(lineas2))
        
        for i in range(max_lineas):
            linea1 = lineas1[i].rstrip() if i < len(lineas1) else None
            linea2 = lineas2[i].rstrip() if i < len(lineas2) else None
            
            if linea1 is None:
                info['lineas_solo_archivo2'].append((i + 1, linea2))
            elif linea2 is None:
                info['lineas_solo_archivo1'].append((i + 1, linea1))
            elif linea1 != linea2:
                info['diferencias'].append({
                    'linea': i + 1,
                    'archivo1': linea1,
                    'archivo2': linea2
                })
        
        # Determinar si son idénticos
        info['son_identicos'] = (len(info['diferencias']) == 0 and 
                                len(info['lineas_solo_archivo1']) == 0 and 
                                len(info['lineas_solo_archivo2']) == 0)
        
        return info
        
    except FileNotFoundError as e:
        return {'error': f"Archivo no encontrado: {e}"}

def mostrar_diferencias(info_comparacion, mostrar_contexto=True, max_diferencias=10):
    """Muestra las diferencias encontradas"""
    if 'error' in info_comparacion:
        print(f"❌ Error: {info_comparacion['error']}")
        return
    
    print(f"=== COMPARACIÓN DE ARCHIVOS ===")
    print(f"Archivo 1: {info_comparacion['archivo1']} ({info_comparacion['lineas_archivo1']} líneas)")
    print(f"Archivo 2: {info_comparacion['archivo2']} ({info_comparacion['lineas_archivo2']} líneas)")
    
    if info_comparacion['son_identicos']:
        print("✅ Los archivos son IDÉNTICOS")
        return
    
    print("❌ Los archivos son DIFERENTES")
    
    # Mostrar diferencias línea por línea
    if info_comparacion['diferencias']:
        print(f"\n🔍 Diferencias encontradas: {len(info_comparacion['diferencias'])}")
        
        diferencias_mostrar = info_comparacion['diferencias'][:max_diferencias]
        
        for diff in diferencias_mostrar:
            print(f"\nLínea {diff['linea']}:")
            print(f"  Archivo 1: {diff['archivo1']}")
            print(f"  Archivo 2: {diff['archivo2']}")
        
        if len(info_comparacion['diferencias']) > max_diferencias:
            print(f"\n... y {len(info_comparacion['diferencias']) - max_diferencias} diferencias más")
    
    # Mostrar líneas que solo están en un archivo
    if info_comparacion['lineas_solo_archivo1']:
        print(f"\n📄 Líneas solo en {info_comparacion['archivo1']}: {len(info_comparacion['lineas_solo_archivo1'])}")
        for num_linea, contenido in info_comparacion['lineas_solo_archivo1'][:5]:
            print(f"  Línea {num_linea}: {contenido}")
        
        if len(info_comparacion['lineas_solo_archivo1']) > 5:
            print(f"  ... y {len(info_comparacion['lineas_solo_archivo1']) - 5} líneas más")
    
    if info_comparacion['lineas_solo_archivo2']:
        print(f"\n📄 Líneas solo en {info_comparacion['archivo2']}: {len(info_comparacion['lineas_solo_archivo2'])}")
        for num_linea, contenido in info_comparacion['lineas_solo_archivo2'][:5]:
            print(f"  Línea {num_linea}: {contenido}")
        
        if len(info_comparacion['lineas_solo_archivo2']) > 5:
            print(f"  ... y {len(info_comparacion['lineas_solo_archivo2']) - 5} líneas más")

def generar_reporte_diferencias(info_comparacion, archivo_reporte):
    """Genera un reporte detallado de las diferencias"""
    try:
        with open(archivo_reporte, 'w', encoding='utf-8') as reporte:
            reporte.write("REPORTE DE COMPARACIÓN DE ARCHIVOS\n")
            reporte.write("=" * 50 + "\n\n")
            
            reporte.write(f"Archivo 1: {info_comparacion['archivo1']} ({info_comparacion['lineas_archivo1']} líneas)\n")
            reporte.write(f"Archivo 2: {info_comparacion['archivo2']} ({info_comparacion['lineas_archivo2']} líneas)\n\n")
            
            if info_comparacion['son_identicos']:
                reporte.write("RESULTADO: Los archivos son IDÉNTICOS\n")
            else:
                reporte.write("RESULTADO: Los archivos son DIFERENTES\n\n")
                
                if info_comparacion['diferencias']:
                    reporte.write(f"DIFERENCIAS LÍNEA POR LÍNEA ({len(info_comparacion['diferencias'])} encontradas):\n")
                    reporte.write("-" * 50 + "\n")
                    
                    for diff in info_comparacion['diferencias']:
                        reporte.write(f"\nLínea {diff['linea']}:\n")
                        reporte.write(f"  Archivo 1: {diff['archivo1']}\n")
                        reporte.write(f"  Archivo 2: {diff['archivo2']}\n")
                
                if info_comparacion['lineas_solo_archivo1']:
                    reporte.write(f"\nLÍNEAS SOLO EN {info_comparacion['archivo1']}:\n")
                    reporte.write("-" * 50 + "\n")
                    for num_linea, contenido in info_comparacion['lineas_solo_archivo1']:
                        reporte.write(f"Línea {num_linea}: {contenido}\n")
                
                if info_comparacion['lineas_solo_archivo2']:
                    reporte.write(f"\nLÍNEAS SOLO EN {info_comparacion['archivo2']}:\n")
                    reporte.write("-" * 50 + "\n")
                    for num_linea, contenido in info_comparacion['lineas_solo_archivo2']:
                        reporte.write(f"Línea {num_linea}: {contenido}\n")
        
        return True
        
    except Exception as e:
        print(f"Error al generar reporte: {e}")
        return False

def crear_archivos_prueba_comparacion():
    """Crea dos archivos para probar la comparación"""
    archivo1_contenido = """Primera línea igual
Segunda línea igual
Esta línea es diferente en archivo1
Cuarta línea igual
Línea que solo está en archivo1
Sexta línea igual"""
    
    archivo2_contenido = """Primera línea igual
Segunda línea igual
Esta línea es diferente en archivo2
Cuarta línea igual
Sexta línea igual
Línea que solo está en archivo2
Línea adicional en archivo2"""
    
    with open('archivo_comparacion1.txt', 'w', encoding='utf-8') as f:
        f.write(archivo1_contenido)
    
    with open('archivo_comparacion2.txt', 'w', encoding='utf-8') as f:
        f.write(archivo2_contenido)
    
    print("Archivos 'archivo_comparacion1.txt' y 'archivo_comparacion2.txt' creados")

def main():
    print("=== COMPARADOR DE ARCHIVOS LÍNEA POR LÍNEA ===")
    
    while True:
        print("\n1. Comparar dos archivos")
        print("2. Crear archivos de prueba")
        print("3. Generar reporte de diferencias")
        print("4. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                archivo1 = input("Primer archivo: ")
                archivo2 = input("Segundo archivo: ")
                
                if not os.path.exists(archivo1):
                    print(f"Error: El archivo '{archivo1}' no existe")
                    continue
                
                if not os.path.exists(archivo2):
                    print(f"Error: El archivo '{archivo2}' no existe")
                    continue
                
                print("Comparando archivos...")
                info = comparar_archivos_linea_por_linea(archivo1, archivo2)
                
                # Opciones de visualización
                print("\nOpciones de visualización:")
                max_diff = input("Máximo de diferencias a mostrar (10 por defecto): ")
                try:
                    max_diff = int(max_diff) if max_diff else 10
                except ValueError:
                    max_diff = 10
                
                mostrar_diferencias(info, True, max_diff)
                
                # Ofrecer generar reporte
                if not info.get('son_identicos', True):
                    generar = input("\n¿Generar reporte detallado? (s/n): ").lower() == 's'
                    if generar:
                        nombre_reporte = f"reporte_comparacion_{archivo1}_{archivo2}.txt".replace('/', '_')
                        if generar_reporte_diferencias(info, nombre_reporte):
                            print(f"✅ Reporte generado: {nombre_reporte}")
            
            elif opcion == 2:
                crear_archivos_prueba_comparacion()
            
            elif opcion == 3:
                archivo1 = input("Primer archivo: ")
                archivo2 = input("Segundo archivo: ")
                
                if not os.path.exists(archivo1) or not os.path.exists(archivo2):
                    print("Error: Uno o ambos archivos no existen")
                    continue
                
                nombre_reporte = input("Nombre del archivo de reporte: ")
                
                info = comparar_archivos_linea_por_linea(archivo1, archivo2)
                
                if generar_reporte_diferencias(info, nombre_reporte):
                    print(f"✅ Reporte generado: {nombre_reporte}")
                else:
                    print("❌ Error al generar el reporte")
            
            elif opcion == 4:
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
    import os
    main()
