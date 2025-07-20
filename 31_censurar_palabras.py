"""
Proyecto 31: Censurar palabras ofensivas
"""

def censurar_texto(texto, palabras_censurar, caracter_censura='*', censurar_completa=False):
    """Censura palabras específicas en un texto"""
    texto_censurado = texto
    palabras_censuradas = []
    
    for palabra in palabras_censurar:
        palabra_lower = palabra.lower()
        
        # Buscar la palabra en el texto (case insensitive)
        palabras_en_texto = texto_censurado.split()
        
        for i, palabra_texto in enumerate(palabras_en_texto):
            # Limpiar signos de puntuación para comparar
            palabra_limpia = palabra_texto.strip('.,!?;:"()[]{}').lower()
            
            if palabra_limpia == palabra_lower:
                if censurar_completa:
                    # Censurar toda la palabra
                    censura = caracter_censura * len(palabra_texto)
                else:
                    # Censurar solo las letras del medio
                    if len(palabra_texto) <= 2:
                        censura = caracter_censura * len(palabra_texto)
                    else:
                        censura = palabra_texto[0] + caracter_censura * (len(palabra_texto) - 2) + palabra_texto[-1]
                
                # Mantener signos de puntuación
                for signo in '.,!?;:"()[]{}':
                    if palabra_texto.endswith(signo):
                        censura += signo
                        break
                
                palabras_en_texto[i] = censura
                palabras_censuradas.append(palabra_texto)
        
        texto_censurado = ' '.join(palabras_en_texto)
    
    return texto_censurado, palabras_censuradas

def censurar_archivo(archivo_entrada, palabras_censurar, archivo_salida=None, **kwargs):
    """Censura palabras en un archivo completo"""
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        
        contenido_censurado, palabras_encontradas = censurar_texto(contenido, palabras_censurar, **kwargs)
        
        if archivo_salida is None:
            archivo_salida = f"censurado_{archivo_entrada}"
        
        with open(archivo_salida, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido_censurado)
        
        return archivo_salida, len(palabras_encontradas), palabras_encontradas
        
    except FileNotFoundError:
        return None, 0, []

def obtener_estadisticas_censura(texto_original, texto_censurado):
    """Obtiene estadísticas de la censura aplicada"""
    palabras_originales = len(texto_original.split())
    palabras_censuradas = len([p for p in texto_censurado.split() if '*' in p])
    
    return {
        'palabras_totales': palabras_originales,
        'palabras_censuradas': palabras_censuradas,
        'porcentaje_censurado': (palabras_censuradas / palabras_originales * 100) if palabras_originales > 0 else 0
    }

def crear_archivo_prueba_censura():
    """Crea un archivo con contenido para probar la censura"""
    contenido = """Este es un texto de prueba para el sistema de censura.
Contiene algunas palabras que podrían considerarse inapropiadas.
Por ejemplo: tonto, idiota, estúpido son palabras que censuraremos.
También podemos censurar palabras como malo o feo.
El sistema debe mantener la puntuación: ¡qué tonto!
Y también funcionar con mayúsculas: IDIOTA o Estúpido."""
    
    with open('texto_censura.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)
    
    print("Archivo 'texto_censura.txt' creado para pruebas")

def main():
    print("=== SISTEMA DE CENSURA DE PALABRAS ===")
    
    # Lista predeterminada de palabras a censurar
    palabras_predeterminadas = ['tonto', 'idiota', 'estúpido', 'malo', 'feo']
    
    while True:
        print("\n1. Censurar texto directo")
        print("2. Censurar archivo")
        print("3. Configurar palabras a censurar")
        print("4. Crear archivo de prueba")
        print("5. Ver palabras actuales")
        print("6. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                texto = input("Ingresa el texto a censurar: ")
                
                print("\nOpciones de censura:")
                caracter = input("Carácter de censura (* por defecto): ").strip() or '*'
                completa = input("¿Censurar palabra completa? (s/n): ").lower() == 's'
                
                texto_censurado, palabras_encontradas = censurar_texto(
                    texto, palabras_predeterminadas, caracter, completa
                )
                
                print(f"\nTexto original: {texto}")
                print(f"Texto censurado: {texto_censurado}")
                
                if palabras_encontradas:
                    print(f"Palabras censuradas: {len(palabras_encontradas)}")
                    print(f"Palabras encontradas: {list(set(palabras_encontradas))}")
                else:
                    print("No se encontraron palabras para censurar")
                
                # Estadísticas
                stats = obtener_estadisticas_censura(texto, texto_censurado)
                print(f"Estadísticas: {stats['palabras_censuradas']}/{stats['palabras_totales']} palabras censuradas ({stats['porcentaje_censurado']:.1f}%)")
            
            elif opcion == 2:
                archivo_entrada = input("Archivo a censurar: ")
                
                if not os.path.exists(archivo_entrada):
                    print(f"Error: El archivo '{archivo_entrada}' no existe")
                    continue
                
                archivo_salida = input("Archivo de salida (Enter para auto-generar): ").strip()
                if not archivo_salida:
                    archivo_salida = None
                
                print("\nOpciones de censura:")
                caracter = input("Carácter de censura (* por defecto): ").strip() or '*'
                completa = input("¿Censurar palabra completa? (s/n): ").lower() == 's'
                
                resultado, total_palabras, palabras_encontradas = censurar_archivo(
                    archivo_entrada, palabras_predeterminadas, archivo_salida,
                    caracter_censura=caracter, censurar_completa=completa
                )
                
                if resultado:
                    print(f"\n✅ Archivo censurado guardado como: {resultado}")
                    print(f"Total de palabras censuradas: {total_palabras}")
                    if palabras_encontradas:
                        print(f"Palabras únicas censuradas: {list(set(palabras_encontradas))}")
                else:
                    print("❌ Error al procesar el archivo")
            
            elif opcion == 3:
                print(f"\nPalabras actuales: {palabras_predeterminadas}")
                print("1. Agregar palabra")
                print("2. Eliminar palabra")
                print("3. Reemplazar lista completa")
                
                sub_opcion = int(input("Selecciona: "))
                
                if sub_opcion == 1:
                    nueva_palabra = input("Palabra a agregar: ").strip().lower()
                    if nueva_palabra and nueva_palabra not in palabras_predeterminadas:
                        palabras_predeterminadas.append(nueva_palabra)
                        print(f"Palabra '{nueva_palabra}' agregada")
                    else:
                        print("Palabra vacía o ya existe")
                
                elif sub_opcion == 2:
                    palabra_eliminar = input("Palabra a eliminar: ").strip().lower()
                    if palabra_eliminar in palabras_predeterminadas:
                        palabras_predeterminadas.remove(palabra_eliminar)
                        print(f"Palabra '{palabra_eliminar}' eliminada")
                    else:
                        print("Palabra no encontrada")
                
                elif sub_opcion == 3:
                    nuevas_palabras = input("Nuevas palabras (separadas por comas): ")
                    palabras_predeterminadas = [p.strip().lower() for p in nuevas_palabras.split(',') if p.strip()]
                    print(f"Lista actualizada: {palabras_predeterminadas}")
            
            elif opcion == 4:
                crear_archivo_prueba_censura()
            
            elif opcion == 5:
                print(f"\nPalabras configuradas para censurar: {palabras_predeterminadas}")
                print(f"Total: {len(palabras_predeterminadas)} palabras")
            
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
