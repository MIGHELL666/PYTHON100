"""
Proyecto 39: Ordenar una lista de números
"""

def burbuja(lista, ascendente=True):
    """Algoritmo de ordenamiento burbuja"""
    lista_copia = lista.copy()
    n = len(lista_copia)
    comparaciones = 0
    intercambios = 0
    
    for i in range(n):
        intercambio_realizado = False
        for j in range(0, n - i - 1):
            comparaciones += 1
            condicion = lista_copia[j] > lista_copia[j + 1] if ascendente else lista_copia[j] < lista_copia[j + 1]
            
            if condicion:
                lista_copia[j], lista_copia[j + 1] = lista_copia[j + 1], lista_copia[j]
                intercambios += 1
                intercambio_realizado = True
        
        # Optimización: si no hubo intercambios, la lista ya está ordenada
        if not intercambio_realizado:
            break
    
    return lista_copia, comparaciones, intercambios

def seleccion(lista, ascendente=True):
    """Algoritmo de ordenamiento por selección"""
    lista_copia = lista.copy()
    n = len(lista_copia)
    comparaciones = 0
    intercambios = 0
    
    for i in range(n):
        indice_extremo = i
        
        for j in range(i + 1, n):
            comparaciones += 1
            condicion = lista_copia[j] < lista_copia[indice_extremo] if ascendente else lista_copia[j] > lista_copia[indice_extremo]
            
            if condicion:
                indice_extremo = j
        
        if indice_extremo != i:
            lista_copia[i], lista_copia[indice_extremo] = lista_copia[indice_extremo], lista_copia[i]
            intercambios += 1
    
    return lista_copia, comparaciones, intercambios

def insercion(lista, ascendente=True):
    """Algoritmo de ordenamiento por inserción"""
    lista_copia = lista.copy()
    comparaciones = 0
    intercambios = 0
    
    for i in range(1, len(lista_copia)):
        clave = lista_copia[i]
        j = i - 1
        
        while j >= 0:
            comparaciones += 1
            condicion = lista_copia[j] > clave if ascendente else lista_copia[j] < clave
            
            if condicion:
                lista_copia[j + 1] = lista_copia[j]
                intercambios += 1
                j -= 1
            else:
                break
        
        lista_copia[j + 1] = clave
    
    return lista_copia, comparaciones, intercambios

def merge_sort(lista, ascendente=True):
    """Algoritmo de ordenamiento merge sort"""
    def merge(izq, der):
        resultado = []
        i = j = 0
        
        while i < len(izq) and j < len(der):
            condicion = izq[i] <= der[j] if ascendente else izq[i] >= der[j]
            
            if condicion:
                resultado.append(izq[i])
                i += 1
            else:
                resultado.append(der[j])
                j += 1
        
        resultado.extend(izq[i:])
        resultado.extend(der[j:])
        return resultado
    
    if len(lista) <= 1:
        return lista.copy()
    
    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio], ascendente)
    derecha = merge_sort(lista[medio:], ascendente)
    
    return merge(izquierda, derecha)

def quick_sort(lista, ascendente=True):
    """Algoritmo de ordenamiento quick sort"""
    if len(lista) <= 1:
        return lista.copy()
    
    pivote = lista[len(lista) // 2]
    
    if ascendente:
        menores = [x for x in lista if x < pivote]
        iguales = [x for x in lista if x == pivote]
        mayores = [x for x in lista if x > pivote]
    else:
        menores = [x for x in lista if x > pivote]
        iguales = [x for x in lista if x == pivote]
        mayores = [x for x in lista if x < pivote]
    
    return quick_sort(menores, ascendente) + iguales + quick_sort(mayores, ascendente)

def generar_lista_aleatoria(tamaño, minimo=1, maximo=100):
    """Genera una lista de números aleatorios"""
    import random
    return [random.randint(minimo, maximo) for _ in range(tamaño)]

def analizar_lista(lista):
    """Analiza las características de una lista"""
    if not lista:
        return {}
    
    return {
        'tamaño': len(lista),
        'minimo': min(lista),
        'maximo': max(lista),
        'suma': sum(lista),
        'promedio': sum(lista) / len(lista),
        'duplicados': len(lista) - len(set(lista)),
        'ya_ordenada_asc': lista == sorted(lista),
        'ya_ordenada_desc': lista == sorted(lista, reverse=True),
        'rango': max(lista) - min(lista)
    }

def main():
    print("=== ORDENADOR DE LISTAS DE NÚMEROS ===")
    
    lista_actual = []
    
    while True:
        print(f"\nLista actual: {lista_actual if len(lista_actual) <= 20 else lista_actual[:20] + ['...']}")
        print(f"Tamaño: {len(lista_actual)}")
        
        print("\n1. Ingresar lista manualmente")
        print("2. Generar lista aleatoria")
        print("3. Ordenar con burbuja")
        print("4. Ordenar con selección")
        print("5. Ordenar con inserción")
        print("6. Ordenar con merge sort")
        print("7. Ordenar con quick sort")
        print("8. Comparar todos los algoritmos")
        print("9. Analizar lista actual")
        print("10. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                entrada = input("Ingresa números separados por espacios: ")
                try:
                    lista_actual = [float(x) for x in entrada.split()]
                    print(f"Lista ingresada: {lista_actual}")
                except ValueError:
                    print("Error: Ingresa solo números válidos")
            
            elif opcion == 2:
                tamaño = int(input("Tamaño de la lista: "))
                minimo = int(input("Valor mínimo (1 por defecto): ") or "1")
                maximo = int(input("Valor máximo (100 por defecto): ") or "100")
                
                lista_actual = generar_lista_aleatoria(tamaño, minimo, maximo)
                print(f"Lista generada: {lista_actual if len(lista_actual) <= 20 else lista_actual[:20] + ['...']}")
            
            elif opcion in [3, 4, 5, 6, 7]:
                if not lista_actual:
                    print("Error: Primero ingresa o genera una lista")
                    continue
                
                orden = input("¿Orden ascendente? (s/n): ").lower() != 'n'
                
                import time
                inicio = time.time()
                
                if opcion == 3:
                    resultado, comp, inter = burbuja(lista_actual, orden)
                    algoritmo = "Burbuja"
                    stats = f"Comparaciones: {comp}, Intercambios: {inter}"
                elif opcion == 4:
                    resultado, comp, inter = seleccion(lista_actual, orden)
                    algoritmo = "Selección"
                    stats = f"Comparaciones: {comp}, Intercambios: {inter}"
                elif opcion == 5:
                    resultado, comp, inter = insercion(lista_actual, orden)
                    algoritmo = "Inserción"
                    stats = f"Comparaciones: {comp}, Intercambios: {inter}"
                elif opcion == 6:
                    resultado = merge_sort(lista_actual, orden)
                    algoritmo = "Merge Sort"
                    stats = "Algoritmo divide y vencerás"
                else:  # opcion == 7
                    resultado = quick_sort(lista_actual, orden)
                    algoritmo = "Quick Sort"
                    stats = "Algoritmo con pivote"
                
                tiempo = time.time() - inicio
                
                print(f"\n=== RESULTADO - {algoritmo} ===")
                print(f"Lista original: {lista_actual if len(lista_actual) <= 15 else lista_actual[:15] + ['...']}")
                print(f"Lista ordenada: {resultado if len(resultado) <= 15 else resultado[:15] + ['...']}")
                print(f"Tiempo: {tiempo:.6f} segundos")
                print(f"Estadísticas: {stats}")
                
                # Verificar que esté correctamente ordenada
                verificacion = sorted(lista_actual) if orden else sorted(lista_actual, reverse=True)
                if resultado == verificacion:
                    print("✅ Ordenamiento correcto")
                else:
                    print("❌ Error en el ordenamiento")
            
            elif opcion == 8:
                if not lista_actual:
                    print("Error: Primero ingresa o genera una lista")
                    continue
                
                if len(lista_actual) > 1000:
                    print("Advertencia: Lista grande, algunos algoritmos pueden ser lentos")
                    continuar = input("¿Continuar? (s/n): ").lower() == 's'
                    if not continuar:
                        continue
                
                orden = input("¿Orden ascendente? (s/n): ").lower() != 'n'
                
                print(f"\n=== COMPARACIÓN DE ALGORITMOS ===")
                print(f"Lista de {len(lista_actual)} elementos")
                
                algoritmos = [
                    ("Burbuja", lambda: burbuja(lista_actual, orden)),
                    ("Selección", lambda: seleccion(lista_actual, orden)),
                    ("Inserción", lambda: insercion(lista_actual, orden)),
                    ("Merge Sort", lambda: (merge_sort(lista_actual, orden), 0, 0)),
                    ("Quick Sort", lambda: (quick_sort(lista_actual, orden), 0, 0))
                ]
                
                import time
                resultados = []
                
                for nombre, func in algoritmos:
                    inicio = time.time()
                    try:
                        resultado, comp, inter = func()
                        tiempo = time.time() - inicio
                        resultados.append((nombre, tiempo, comp, inter))
                        print(f"{nombre:12}: {tiempo:.6f}s", end="")
                        if comp > 0:
                            print(f" (Comp: {comp}, Inter: {inter})")
                        else:
                            print()
                    except Exception as e:
                        print(f"{nombre:12}: Error - {e}")
                
                # Mostrar ranking
                if resultados:
                    print(f"\nRanking por velocidad:")
                    resultados_ordenados = sorted(resultados, key=lambda x: x[1])
                    for i, (nombre, tiempo, comp, inter) in enumerate(resultados_ordenados, 1):
                        print(f"{i}. {nombre}: {tiempo:.6f}s")
            
            elif opcion == 9:
                if not lista_actual:
                    print("Error: No hay lista para analizar")
                    continue
                
                stats = analizar_lista(lista_actual)
                
                print(f"\n=== ANÁLISIS DE LA LISTA ===")
                print(f"Tamaño: {stats['tamaño']}")
                print(f"Mínimo: {stats['minimo']}")
                print(f"Máximo: {stats['maximo']}")
                print(f"Suma: {stats['suma']}")
                print(f"Promedio: {stats['promedio']:.2f}")
                print(f"Rango: {stats['rango']}")
                print(f"Duplicados: {stats['duplicados']}")
                print(f"Ya ordenada (asc): {'Sí' if stats['ya_ordenada_asc'] else 'No'}")
                print(f"Ya ordenada (desc): {'Sí' if stats['ya_ordenada_desc'] else 'No'}")
            
            elif opcion == 10:
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
