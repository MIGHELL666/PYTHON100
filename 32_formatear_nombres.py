"""
Proyecto 32: Formatear nombres propios (capitalizar)
"""

def capitalizar_nombre(nombre):
    """Capitaliza correctamente un nombre propio"""
    if not nombre:
        return nombre
    
    # Dividir por espacios y procesar cada parte
    partes = nombre.strip().split()
    partes_formateadas = []
    
    # Prefijos que no se capitalizan (excepto al inicio)
    prefijos_minusculas = ['de', 'del', 'la', 'las', 'el', 'los', 'y', 'e', 'da', 'das', 'do', 'dos']
    
    for i, parte in enumerate(partes):
        parte_lower = parte.lower()
        
        # Si es el primer nombre o no es un prefijo, capitalizar
        if i == 0 or parte_lower not in prefijos_minusculas:
            # Manejar nombres con apostrofe (O'Connor, D'Angelo)
            if "'" in parte:
                subpartes = parte.split("'")
                parte_formateada = "'".join([subparte.capitalize() for subparte in subpartes])
            else:
                parte_formateada = parte.capitalize()
        else:
            # Mantener prefijos en minúscula
            parte_formateada = parte_lower
        
        partes_formateadas.append(parte_formateada)
    
    return ' '.join(partes_formateadas)

def formatear_lista_nombres(nombres):
    """Formatea una lista de nombres"""
    nombres_formateados = []
    
    for nombre in nombres:
        nombre_formateado = capitalizar_nombre(nombre)
        nombres_formateados.append(nombre_formateado)
    
    return nombres_formateados

def formatear_archivo_nombres(archivo_entrada, archivo_salida=None):
    """Formatea nombres en un archivo"""
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        
        lineas_formateadas = []
        nombres_procesados = 0
        
        for linea in lineas:
            linea_limpia = linea.strip()
            if linea_limpia:  # Si la línea no está vacía
                nombre_formateado = capitalizar_nombre(linea_limpia)
                lineas_formateadas.append(nombre_formateado + '\n')
                nombres_procesados += 1
            else:
                lineas_formateadas.append('\n')
        
        if archivo_salida is None:
            archivo_salida = f"nombres_formateados_{archivo_entrada}"
        
        with open(archivo_salida, 'w', encoding='utf-8') as archivo:
            archivo.writelines(lineas_formateadas)
        
        return archivo_salida, nombres_procesados
        
    except FileNotFoundError:
        return None, 0

def detectar_formato_incorrecto(nombre):
    """Detecta si un nombre tiene formato incorrecto"""
    problemas = []
    
    if nombre != nombre.strip():
        problemas.append("Espacios extra al inicio/final")
    
    if nombre.isupper():
        problemas.append("Todo en mayúsculas")
    
    if nombre.islower():
        problemas.append("Todo en minúsculas")
    
    # Verificar espacios múltiples
    if '  ' in nombre:
        problemas.append("Espacios múltiples")
    
    # Verificar si empieza con minúscula
    if nombre and nombre[0].islower():
        problemas.append("Empieza con minúscula")
    
    return problemas

def crear_archivo_nombres_prueba():
    """Crea un archivo con nombres mal formateados para pruebas"""
    nombres_mal_formateados = """JUAN PÉREZ
maría garcía lópez
PEDRO DE LA CRUZ
ana  maría  gonzález
josé luis de los santos
MARÍA DEL CARMEN RODRÍGUEZ
francisco javier o'connor
  carlos   alberto   
LUIS FERNANDO Y GONZÁLEZ
patricia da silva"""
    
    with open('nombres_mal_formateados.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(nombres_mal_formateados)
    
    print("Archivo 'nombres_mal_formateados.txt' creado")

def main():
    print("=== FORMATEADOR DE NOMBRES PROPIOS ===")
    
    while True:
        print("\n1. Formatear nombre individual")
        print("2. Formatear lista de nombres")
        print("3. Formatear archivo de nombres")
        print("4. Analizar formato de nombre")
        print("5. Crear archivo de prueba")
        print("6. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                nombre = input("Ingresa el nombre a formatear: ")
                
                print(f"Nombre original: '{nombre}'")
                
                # Detectar problemas
                problemas = detectar_formato_incorrecto(nombre)
                if problemas:
                    print(f"Problemas detectados: {', '.join(problemas)}")
                
                nombre_formateado = capitalizar_nombre(nombre)
                print(f"Nombre formateado: '{nombre_formateado}'")
                
                if nombre != nombre_formateado:
                    print("✅ Formato corregido")
                else:
                    print("✅ El nombre ya tenía formato correcto")
            
            elif opcion == 2:
                print("Ingresa nombres separados por comas:")
                entrada = input("Nombres: ")
                nombres = [n.strip() for n in entrada.split(',') if n.strip()]
                
                if not nombres:
                    print("No se ingresaron nombres válidos")
                    continue
                
                print(f"\n=== FORMATEO DE {len(nombres)} NOMBRES ===")
                nombres_formateados = formatear_lista_nombres(nombres)
                
                for i, (original, formateado) in enumerate(zip(nombres, nombres_formateados), 1):
                    cambio = "✓" if original != formateado else "="
                    print(f"{i:2d}. {cambio} '{original}' → '{formateado}'")
            
            elif opcion == 3:
                archivo_entrada = input("Archivo con nombres: ")
                
                if not os.path.exists(archivo_entrada):
                    print(f"Error: El archivo '{archivo_entrada}' no existe")
                    continue
                
                archivo_salida = input("Archivo de salida (Enter para auto-generar): ").strip()
                if not archivo_salida:
                    archivo_salida = None
                
                resultado, nombres_procesados = formatear_archivo_nombres(archivo_entrada, archivo_salida)
                
                if resultado:
                    print(f"✅ Archivo procesado: {resultado}")
                    print(f"Nombres formateados: {nombres_procesados}")
                    
                    # Mostrar preview del resultado
                    with open(resultado, 'r', encoding='utf-8') as archivo:
                        lineas = archivo.readlines()[:10]  # Primeras 10 líneas
                    
                    print("\nPreview del resultado:")
                    for i, linea in enumerate(lineas, 1):
                        print(f"{i:2d}. {linea.strip()}")
                    
                    if len(lineas) == 10:
                        print("...")
                else:
                    print("❌ Error al procesar el archivo")
            
            elif opcion == 4:
                nombre = input("Nombre a analizar: ")
                
                problemas = detectar_formato_incorrecto(nombre)
                nombre_formateado = capitalizar_nombre(nombre)
                
                print(f"\n=== ANÁLISIS DE: '{nombre}' ===")
                
                if problemas:
                    print("❌ Problemas encontrados:")
                    for problema in problemas:
                        print(f"  • {problema}")
                else:
                    print("✅ No se encontraron problemas de formato")
                
                print(f"Versión corregida: '{nombre_formateado}'")
                
                if nombre == nombre_formateado:
                    print("✅ El nombre ya tiene formato correcto")
                else:
                    print("🔧 Se aplicaron correcciones")
            
            elif opcion == 5:
                crear_archivo_nombres_prueba()
            
            elif opcion == 6:
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
