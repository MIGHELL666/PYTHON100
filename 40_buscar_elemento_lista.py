"""
Proyecto 40: Buscar un elemento en una lista
"""

def busqueda_lineal(lista, elemento):
    """Búsqueda lineal - O(n)"""
    posiciones = []
    comparaciones = 0
    
    for i, item in enumerate(lista):
        comparaciones += 1
        if item == elemento:
            posiciones.append(i)
    
    return posiciones, comparaciones

def busqueda_binaria(lista_ordenada, elemento):
    """Búsqueda binaria - O(log n) - requiere lista ordenada"""
    izquierda = 0
    derecha = len(lista_ordenada) - 1
    comparaciones = 0
    
    while izquierda <= derecha:
        comparaciones += 1
        medio = (izquierda + derecha) // 2
        
        if lista_ordenada[medio] == elemento:
            return medio, comparaciones
        elif lista_ordenada[medio] < elemento:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    
    return -1, comparaciones

def busqueda_binaria_recursiva(lista_ordenada, elemento, izquierda=0, derecha=None, comparaciones=0):
    """Búsqueda binaria recursiva"""
    if derecha is None:
        derecha = len(lista_ordenada) - 1
    
    if izquierda > derecha:
        return -1, comparaciones
    
    comparaciones += 1
    medio = (izquierda + derecha) // 2
    
    if lista_ordenada[medio] == elemento:
        return medio, comparaciones
    elif lista_ordenada[medio] < elemento:
        return busqueda_binaria_recursiva(lista_ordenada, elemento, medio + 1, derecha, comparaciones)
    else:
        return busqueda_binaria_recursiva(lista_ordenada, elemento, izquierda, medio - 1, comparaciones)

def buscar_patron(lista, patron):
    """Busca un patrón de elementos consecutivos en la lista"""
    if not patron:
        return []
    
    posiciones = []
    patron_len = len(patron)
    
    for i in range(len(lista) - patron_len + 1):
        if lista[i:i + patron_len] == patron:
            posiciones.append(i)
    
    return posiciones

def buscar_rango(lista, minimo, maximo):
    """Busca todos los elementos dentro de un rango"""
    elementos_en_rango = []
    
    for i, elemento in enumerate(lista):
        if minimo <= elemento <= maximo:
            elementos_en_rango.append((i, elemento))
    
    return elementos_en_rango

def buscar_con_condicion(lista, condicion):
    """Busca elementos que cumplan una condición específica"""
    resultados = []
    
    for i, elemento in enumerate(lista):
        if condicion(elemento):
            resultados.append((i, elemento))
    
    return resultados

def estadisticas_busqueda(lista, elemento):
    """Proporciona estadísticas detalladas sobre la búsqueda"""
    posiciones, comparaciones = busqueda_lineal(lista, elemento)
    
    stats = {
        'elemento_buscado': elemento,
        'tamaño_lista': len(lista),
        'encontrado': len(posiciones) > 0,
        'posiciones': posiciones,
        'cantidad_encontrada': len(posiciones),
        'comparaciones_lineales': comparaciones,
        'porcentaje_lista': (comparaciones / len(lista) * 100) if lista else 0
    }
    
    # Si la lista está ordenada, también hacer búsqueda binaria
    lista_ordenada = sorted(lista)
    if lista == lista_ordenada:
        posicion_binaria, comp_binarias = busqueda_binaria(lista, elemento)
        stats['lista_ordenada'] = True
        stats['posicion_binaria'] = posicion_binaria
        stats['comparaciones_binarias'] = comp_binarias
    else:
        stats['lista_ordenada'] = False
    
    return stats

def generar_lista_prueba(tamaño=20, minimo=1, maximo=50):
    """Genera una lista de prueba con algunos duplicados"""
    import random
    lista = []
    
    # Generar números con algunos duplicados intencionalmente
    for _ in range(tamaño):
        if random.random() < 0.3:  # 30% de probabilidad de duplicado
            if lista:
                lista.append(random.choice(lista))
            else:
                lista.append(random.randint(minimo, maximo))
        else:
            lista.append(random.randint(minimo, maximo))
    
    return lista

def main():
    print("=== BUSCADOR DE ELEMENTOS EN LISTAS ===")
    
    lista_actual = []
    
    while True:
        print(f"\nLista actual: {lista_actual if len(lista_actual) <= 15 else lista_actual[:15] + ['...']}")
        print(f"Tamaño: {len(lista_actual)}")
        
        print("\n1. Ingresar lista manualmente")
        print("2. Generar lista de prueba")
        print("3. Búsqueda lineal")
        print("4. Búsqueda binaria")
        print("5. Buscar patrón")
        print("6. Buscar en rango")
        print("7. Buscar con condición")
        print("8. Estadísticas de búsqueda")
        print("9. Comparar métodos de búsqueda")
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
                tamaño = int(input("Tamaño de la lista (20 por defecto): ") or "20")
                minimo = int(input("Valor mínimo (1 por defecto): ") or "1")
                maximo = int(input("Valor máximo (50 por defecto): ") or "50")
                
                lista_actual = generar_lista_prueba(tamaño, minimo, maximo)
                print(f"Lista generada: {lista_actual if len(lista_actual) <= 15 else lista_actual[:15] + ['...']}")
            
            elif opcion == 3:
                if not lista_actual:
                    print("Error: Primero ingresa o genera una lista")
                    continue
                
                elemento = float(input("Elemento a buscar: "))
                
                import time
                inicio = time.time()
                posiciones, comparaciones = busqueda_lineal(lista_actual, elemento)
                tiempo = time.time() - inicio
                
                print(f"\n=== BÚSQUEDA LINEAL ===")
                print(f"Elemento buscado: {elemento}")
                
                if posiciones:
                    print(f"✅ Encontrado en {len(posiciones)} posición(es): {posiciones}")
                    print(f"Valores: {[lista_actual[pos] for pos in posiciones]}")
                else:
                    print("❌ Elemento no encontrado")
                
                print(f"Comparaciones realizadas: {comparaciones}")
                print(f"Tiempo: {tiempo:.6f} segundos")
            
            elif opcion == 4:
                if not lista_actual:
                    print("Error: Primero ingresa o genera una lista")
                    continue
                
                # Verificar si está ordenada
                lista_ordenada = sorted(lista_actual)
                if lista_actual != lista_ordenada:
                    print("La lista no está ordenada. Ordenando automáticamente...")
                    lista_actual = lista_ordenada
                    print(f"Lista ordenada: {lista_actual if len(lista_actual) <= 15 else lista_actual[:15] + ['...']}")
                
                elemento = float(input("Elemento a buscar: "))
                
                import time
                
                # Búsqueda binaria iterativa
                inicio = time.time()
                posicion_iter, comp_iter = busqueda_binaria(lista_actual, elemento)
                tiempo_iter = time.time() - inicio
                
                # Búsqueda binaria recursiva
                inicio = time.time()
                posicion_rec, comp_rec = busqueda_binaria_recursiva(lista_actual, elemento)
                tiempo_rec = time.time() - inicio
                
                print(f"\n=== BÚSQUEDA BINARIA ===")
                print(f"Elemento buscado: {elemento}")
                
                if posicion_iter != -1:
                    print(f"✅ Encontrado en posición: {posicion_iter}")
                    print(f"Valor: {lista_actual[posicion_iter]}")
                else:
                    print("❌ Elemento no encontrado")
                
                print(f"\nIterativa - Comparaciones: {comp_iter}, Tiempo: {tiempo_iter:.6f}s")
                print(f"Recursiva - Comparaciones: {comp_rec}, Tiempo: {tiempo_rec:.6f}s")
            
            elif opcion == 5:
                if not lista_actual:
                    print("Error: Primero ingresa o genera una lista")
                    continue
                
                entrada_patron = input("Ingresa el patrón a buscar (números separados por espacios): ")
                try:
                    patron = [float(x) for x in entrada_patron.split()]
                    posiciones = buscar_patron(lista_actual, patron)
                    
                    print(f"\n=== BÚSQUEDA DE PATRÓN ===")
                    print(f"Patrón buscado: {patron}")
                    
                    if posiciones:
                        print(f"✅ Patrón encontrado en {len(posiciones)} posición(es): {posiciones}")
                        for pos in posiciones:
                            print(f"  Posición {pos}: {lista_actual[pos:pos+len(patron)]}")
                    else:
                        print("❌ Patrón no encontrado")
                        
                except ValueError:
                    print("Error: Ingresa números válidos para el patrón")
            
            elif opcion == 6:
                if not lista_actual:
                    print("Error: Primero ingresa o genera una lista")
                    continue
                
                minimo = float(input("Valor mínimo del rango: "))
                maximo = float(input("Valor máximo del rango: "))
                
                elementos_rango = buscar_rango(lista_actual, minimo, maximo)
                
                print(f"\n=== BÚSQUEDA EN RANGO [{minimo}, {maximo}] ===")
                
                if elementos_rango:
                    print(f"✅ Encontrados {len(elementos_rango)} elementos:")
                    for pos, valor in elementos_rango:
                        print(f"  Posición {pos}: {valor}")
                else:
                    print("❌ No se encontraron elementos en el rango")
            
            elif opcion == 7:
                if not lista_actual:
                    print("Error: Primero ingresa o genera una lista")
                    continue
                
                print("Condiciones disponibles:")
                print("1. Números pares")
                print("2. Números impares")
                print("3. Números mayores que X")
                print("4. Números menores que X")
                print("5. Números negativos")
                print("6. Números positivos")
                
                cond_opcion = int(input("Selecciona condición: "))
                
                if cond_opcion == 1:
                    condicion = lambda x: x % 2 == 0
                    desc = "números pares"
                elif cond_opcion == 2:
                    condicion = lambda x: x % 2 != 0
                    desc = "números impares"
                elif cond_opcion == 3:
                    limite = float(input("Mayor que: "))
                    condicion = lambda x: x > limite
                    desc = f"números > {limite}"
                elif cond_opcion == 4:
                    limite = float(input("Menor que: "))
                    condicion = lambda x: x < limite
                    desc = f"números < {limite}"
                elif cond_opcion == 5:
                    condicion = lambda x: x < 0
                    desc = "números negativos"
                elif cond_opcion == 6:
                    condicion = lambda x: x > 0
                    desc = "números positivos"
                else:
                    print("Opción no válida")
                    continue
                
                resultados = buscar_con_condicion(lista_actual, condicion)
                
                print(f"\n=== BÚSQUEDA CON CONDICIÓN: {desc} ===")
                
                if resultados:
                    print(f"✅ Encontrados {len(resultados)} elementos:")
                    for pos, valor in resultados:
                        print(f"  Posición {pos}: {valor}")
                else:
                    print("❌ No se encontraron elementos que cumplan la condición")
            
            elif opcion == 8:
                if not lista_actual:
                    print("Error: Primero ingresa o genera una lista")
                    continue
                
                elemento = float(input("Elemento para análisis: "))
                stats = estadisticas_busqueda(lista_actual, elemento)
                
                print(f"\n=== ESTADÍSTICAS DE BÚSQUEDA ===")
                print(f"Elemento buscado: {stats['elemento_buscado']}")
                print(f"Tamaño de lista: {stats['tamaño_lista']}")
                print(f"Encontrado: {'Sí' if stats['encontrado'] else 'No'}")
                
                if stats['encontrado']:
                    print(f"Posiciones: {stats['posiciones']}")
                    print(f"Cantidad encontrada: {stats['cantidad_encontrada']}")
                
                print(f"Comparaciones (lineal): {stats['comparaciones_lineales']}")
                print(f"Porcentaje de lista revisado: {stats['porcentaje_lista']:.1f}%")
                
                if stats['lista_ordenada']:
                    print(f"Lista ordenada: Sí")
                    if stats['posicion_binaria'] != -1:
                        print(f"Posición (binaria): {stats['posicion_binaria']}")
                    print(f"Comparaciones (binaria): {stats['comparaciones_binarias']}")
                else:
                    print(f"Lista ordenada: No")
            
            elif opcion == 9:
                if not lista_actual:
                    print("Error: Primero ingresa o genera una lista")
                    continue
                
                elemento = float(input("Elemento a buscar: "))
                
                import time
                
                print(f"\n=== COMPARACIÓN DE MÉTODOS ===")
                print(f"Buscando: {elemento} en lista de {len(lista_actual)} elementos")
                
                # Búsqueda lineal
                inicio = time.time()
                pos_lineal, comp_lineal = busqueda_lineal(lista_actual, elemento)
                tiempo_lineal = time.time() - inicio
                
                print(f"\nBúsqueda Lineal:")
                print(f"  Encontrado: {'Sí' if pos_lineal else 'No'}")
                print(f"  Posiciones: {pos_lineal}")
                print(f"  Comparaciones: {comp_lineal}")
                print(f"  Tiempo: {tiempo_lineal:.6f}s")
                
                # Búsqueda binaria (si está ordenada)
                lista_ordenada = sorted(lista_actual)
                if lista_actual == lista_ordenada:
                    inicio = time.time()
                    pos_binaria, comp_binaria = busqueda_binaria(lista_actual, elemento)
                    tiempo_binaria = time.time() - inicio
                    
                    print(f"\nBúsqueda Binaria:")
                    print(f"  Encontrado: {'Sí' if pos_binaria != -1 else 'No'}")
                    print(f"  Posición: {pos_binaria}")
                    print(f"  Comparaciones: {comp_binaria}")
                    print(f"  Tiempo: {tiempo_binaria:.6f}s")
                    
                    if comp_lineal > 0 and comp_binaria > 0:
                        mejora = comp_lineal / comp_binaria
                        print(f"\nMejora binaria: {mejora:.1f}x menos comparaciones")
                else:
                    print(f"\nLista no ordenada - búsqueda binaria no aplicable")
            
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
