"""
Proyecto 25: Guardar notas en un archivo
"""

from datetime import datetime

def agregar_nota(archivo_notas, nota):
    """Agrega una nota con timestamp al archivo"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea_nota = f"[{timestamp}] {nota}\n"
    
    with open(archivo_notas, 'a', encoding='utf-8') as archivo:
        archivo.write(linea_nota)
    
    return timestamp

def leer_notas(archivo_notas):
    """Lee todas las notas del archivo"""
    try:
        with open(archivo_notas, 'r', encoding='utf-8') as archivo:
            return archivo.readlines()
    except FileNotFoundError:
        return []

def buscar_notas(archivo_notas, termino_busqueda):
    """Busca notas que contengan un término específico"""
    notas = leer_notas(archivo_notas)
    notas_encontradas = []
    
    for i, nota in enumerate(notas, 1):
        if termino_busqueda.lower() in nota.lower():
            notas_encontradas.append((i, nota.strip()))
    
    return notas_encontradas

def main():
    archivo_notas = "mis_notas.txt"
    
    while True:
        print("\n=== BLOC DE NOTAS ===")
        print("1. Agregar nota")
        print("2. Ver todas las notas")
        print("3. Buscar en notas")
        print("4. Contar notas")
        print("5. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                nota = input("Escribe tu nota: ")
                if nota.strip():
                    timestamp = agregar_nota(archivo_notas, nota)
                    print(f"Nota guardada el {timestamp}")
                else:
                    print("No se puede guardar una nota vacía")
            
            elif opcion == 2:
                notas = leer_notas(archivo_notas)
                if notas:
                    print(f"\n=== TODAS LAS NOTAS ({len(notas)}) ===")
                    for i, nota in enumerate(notas, 1):
                        print(f"{i}. {nota.strip()}")
                else:
                    print("No hay notas guardadas")
            
            elif opcion == 3:
                termino = input("Término a buscar: ")
                notas_encontradas = buscar_notas(archivo_notas, termino)
                
                if notas_encontradas:
                    print(f"\nSe encontraron {len(notas_encontradas)} nota(s) con '{termino}':")
                    for num_nota, contenido in notas_encontradas:
                        print(f"{num_nota}. {contenido}")
                else:
                    print(f"No se encontraron notas con '{termino}'")
            
            elif opcion == 4:
                notas = leer_notas(archivo_notas)
                print(f"Total de notas guardadas: {len(notas)}")
                
                if notas:
                    primera_nota = notas[0].split(']')[0] + ']'
                    ultima_nota = notas[-1].split(']')[0] + ']'
                    print(f"Primera nota: {primera_nota}")
                    print(f"Última nota: {ultima_nota}")
            
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
