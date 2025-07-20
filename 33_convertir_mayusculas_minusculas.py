"""
Proyecto 33: Convertir texto a minúsculas y mayúsculas
"""

def convertir_texto(texto, modo):
    """Convierte texto según el modo especificado"""
    conversiones = {
        'mayusculas': texto.upper(),
        'minusculas': texto.lower(),
        'titulo': texto.title(),
        'capitalizar': texto.capitalize(),
        'alternar': ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(texto)]),
        'invertir': ''.join([c.lower() if c.isupper() else c.upper() for c in texto]),
        'primera_letra': ' '.join([palabra.capitalize() for palabra in texto.split()]),
        'camel_case': ''.join([palabra.capitalize() for palabra in texto.split()]),
        'snake_case': texto.lower().replace(' ', '_'),
        'kebab_case': texto.lower().replace(' ', '-')
    }
    
    return conversiones.get(modo, texto)

def convertir_archivo(archivo_entrada, modo, archivo_salida=None):
    """Convierte el contenido de un archivo"""
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        
        contenido_convertido = convertir_texto(contenido, modo)
        
        if archivo_salida is None:
            archivo_salida = f"{modo}_{archivo_entrada}"
        
        with open(archivo_salida, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido_convertido)
        
        return archivo_salida
        
    except FileNotFoundError:
        return None

def analizar_texto(texto):
    """Analiza las características del texto"""
    stats = {
        'total_caracteres': len(texto),
        'mayusculas': sum(1 for c in texto if c.isupper()),
        'minusculas': sum(1 for c in texto if c.islower()),
        'digitos': sum(1 for c in texto if c.isdigit()),
        'espacios': sum(1 for c in texto if c.isspace()),
        'signos_puntuacion': sum(1 for c in texto if not c.isalnum() and not c.isspace()),
        'palabras': len(texto.split()),
        'lineas': len(texto.split('\n'))
    }
    
    return stats

def mostrar_todas_conversiones(texto):
    """Muestra todas las conversiones posibles de un texto"""
    modos = {
        'mayusculas': 'TODO EN MAYÚSCULAS',
        'minusculas': 'todo en minúsculas',
        'titulo': 'Cada Palabra Capitalizada',
        'capitalizar': 'Solo primera letra',
        'alternar': 'AlTeRnAnDo MaYúScUlAs',
        'invertir': 'iNVIRTIENDO mAYÚSCULAS',
        'primera_letra': 'Primera Letra De Cada Palabra',
        'camel_case': 'CamelCaseFormat',
        'snake_case': 'snake_case_format',
        'kebab_case': 'kebab-case-format'
    }
    
    print(f"=== CONVERSIONES DE: '{texto}' ===")
    
    for modo, descripcion in modos.items():
        resultado = convertir_texto(texto, modo)
        print(f"{descripcion:25} → {resultado}")

def crear_archivo_texto_prueba():
    """Crea un archivo de texto para pruebas"""
    contenido = """Este es un TEXTO de prueba para conversiones.
Contiene MAYÚSCULAS, minúsculas y Palabras Mixtas.
También tiene números como 123 y símbolos como !@#.
¿Funcionará correctamente con acentos y ñ?
ÚLTIMA línea del archivo de PRUEBA."""
    
    with open('texto_conversiones.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)
    
    print("Archivo 'texto_conversiones.txt' creado")

def main():
    print("=== CONVERSOR DE MAYÚSCULAS Y MINÚSCULAS ===")
    
    while True:
        print("\n1. Convertir texto directo")
        print("2. Mostrar todas las conversiones")
        print("3. Convertir archivo")
        print("4. Analizar texto")
        print("5. Crear archivo de prueba")
        print("6. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                texto = input("Ingresa el texto a convertir: ")
                
                print("\nModos de conversión:")
                print("1. Mayúsculas    2. Minúsculas    3. Título")
                print("4. Capitalizar   5. Alternar      6. Invertir")
                print("7. Primera letra 8. CamelCase     9. snake_case")
                print("10. kebab-case")
                
                try:
                    modo_num = int(input("Selecciona modo (1-10): "))
                    modos = ['mayusculas', 'minusculas', 'titulo', 'capitalizar', 
                            'alternar', 'invertir', 'primera_letra', 'camel_case', 
                            'snake_case', 'kebab_case']
                    
                    if 1 <= modo_num <= 10:
                        modo = modos[modo_num - 1]
                        resultado = convertir_texto(texto, modo)
                        
                        print(f"\nTexto original: {texto}")
                        print(f"Texto convertido ({modo}): {resultado}")
                    else:
                        print("Modo no válido")
                        
                except ValueError:
                    print("Error: Ingresa un número válido")
            
            elif opcion == 2:
                texto = input("Ingresa el texto: ")
                mostrar_todas_conversiones(texto)
            
            elif opcion == 3:
                archivo_entrada = input("Archivo a convertir: ")
                
                if not os.path.exists(archivo_entrada):
                    print(f"Error: El archivo '{archivo_entrada}' no existe")
                    continue
                
                print("\nModos disponibles:")
                print("1. mayusculas  2. minusculas  3. titulo")
                print("4. capitalizar 5. alternar    6. invertir")
                
                try:
                    modo_num = int(input("Selecciona modo (1-6): "))
                    modos = ['mayusculas', 'minusculas', 'titulo', 'capitalizar', 'alternar', 'invertir']
                    
                    if 1 <= modo_num <= 6:
                        modo = modos[modo_num - 1]
                        archivo_salida = input("Archivo de salida (Enter para auto-generar): ").strip()
                        if not archivo_salida:
                            archivo_salida = None
                        
                        resultado = convertir_archivo(archivo_entrada, modo, archivo_salida)
                        
                        if resultado:
                            print(f"✅ Archivo convertido guardado como: {resultado}")
                            
                            # Mostrar preview
                            with open(resultado, 'r', encoding='utf-8') as archivo:
                                preview = archivo.read()[:200]
                            print(f"Preview: {preview}{'...' if len(preview) == 200 else ''}")
                        else:
                            print("❌ Error al convertir el archivo")
                    else:
                        print("Modo no válido")
                        
                except ValueError:
                    print("Error: Ingresa un número válido")
            
            elif opcion == 4:
                texto = input("Texto a analizar: ")
                stats = analizar_texto(texto)
                
                print(f"\n=== ANÁLISIS DE TEXTO ===")
                print(f"Total de caracteres: {stats['total_caracteres']}")
                print(f"Mayúsculas: {stats['mayusculas']}")
                print(f"Minúsculas: {stats['minusculas']}")
                print(f"Dígitos: {stats['digitos']}")
                print(f"Espacios: {stats['espacios']}")
                print(f"Signos de puntuación: {stats['signos_puntuacion']}")
                print(f"Palabras: {stats['palabras']}")
                print(f"Líneas: {stats['lineas']}")
                
                # Porcentajes
                total = stats['total_caracteres']
                if total > 0:
                    print(f"\nPorcentajes:")
                    print(f"Mayúsculas: {stats['mayusculas']/total*100:.1f}%")
                    print(f"Minúsculas: {stats['minusculas']/total*100:.1f}%")
                    print(f"Dígitos: {stats['digitos']/total*100:.1f}%")
            
            elif opcion == 5:
                crear_archivo_texto_prueba()
            
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
