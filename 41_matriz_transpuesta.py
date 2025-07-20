"""
Proyecto 41: Calcular la transpuesta de una matriz
"""

def crear_matriz(filas, columnas, valor_inicial=0):
    """Crea una matriz de tamaño filas x columnas"""
    return [[valor_inicial for _ in range(columnas)] for _ in range(filas)]

def ingresar_matriz():
    """Permite al usuario ingresar una matriz manualmente"""
    try:
        filas = int(input("Número de filas: "))
        columnas = int(input("Número de columnas: "))
        
        if filas <= 0 or columnas <= 0:
            print("Error: Las dimensiones deben ser positivas")
            return None
        
        matriz = []
        print(f"\nIngresa los elementos de la matriz {filas}x{columnas}:")
        
        for i in range(filas):
            fila = []
            for j in range(columnas):
                valor = float(input(f"Elemento [{i+1}][{j+1}]: "))
                fila.append(valor)
            matriz.append(fila)
        
        return matriz
        
    except ValueError:
        print("Error: Ingresa números válidos")
        return None

def generar_matriz_aleatoria(filas, columnas, minimo=1, maximo=10):
    """Genera una matriz con números aleatorios"""
    import random
    matriz = []
    
    for i in range(filas):
        fila = []
        for j in range(columnas):
            valor = random.randint(minimo, maximo)
            fila.append(valor)
        matriz.append(fila)
    
    return matriz

def transponer_matriz(matriz):
    """Calcula la transpuesta de una matriz"""
    if not matriz or not matriz[0]:
        return []
    
    filas = len(matriz)
    columnas = len(matriz[0])
    
    # Crear matriz transpuesta
    transpuesta = crear_matriz(columnas, filas)
    
    for i in range(filas):
        for j in range(columnas):
            transpuesta[j][i] = matriz[i][j]
    
    return transpuesta

def mostrar_matriz(matriz, nombre="Matriz"):
    """Muestra una matriz de forma organizada"""
    if not matriz:
        print(f"{nombre}: Matriz vacía")
        return
    
    print(f"\n{nombre}:")
    
    # Calcular el ancho máximo para alineación
    max_ancho = 0
    for fila in matriz:
        for elemento in fila:
            ancho = len(str(elemento))
            if ancho > max_ancho:
                max_ancho = ancho
    
    # Mostrar matriz
    for fila in matriz:
        fila_str = " ".join(f"{elemento:>{max_ancho}}" for elemento in fila)
        print(f"  [{fila_str}]")
    
    print(f"Dimensiones: {len(matriz)}x{len(matriz[0])}")

def es_matriz_cuadrada(matriz):
    """Verifica si una matriz es cuadrada"""
    if not matriz:
        return False
    return len(matriz) == len(matriz[0])

def es_matriz_simetrica(matriz):
    """Verifica si una matriz es simétrica (A = A^T)"""
    if not es_matriz_cuadrada(matriz):
        return False
    
    transpuesta = transponer_matriz(matriz)
    
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if matriz[i][j] != transpuesta[i][j]:
                return False
    
    return True

def propiedades_matriz(matriz):
    """Analiza las propiedades de una matriz"""
    if not matriz:
        return {}
    
    filas = len(matriz)
    columnas = len(matriz[0])
    
    # Elementos únicos
    elementos = []
    for fila in matriz:
        elementos.extend(fila)
    
    propiedades = {
        'dimensiones': (filas, columnas),
        'es_cuadrada': es_matriz_cuadrada(matriz),
        'es_simetrica': es  (filas, columnas),
        'es_cuadrada': es_matriz_cuadrada(matriz),
        'es_simetrica': es_matriz_simetrica(matriz) if es_matriz_cuadrada(matriz) else False,
        'total_elementos': filas * columnas,
        'elementos_unicos': len(set(elementos)),
        'suma_total': sum(elementos),
        'promedio': sum(elementos) / len(elementos) if elementos else 0,
        'minimo': min(elementos) if elementos else 0,
        'maximo': max(elementos) if elementos else 0
    }
    
    return propiedades

def multiplicar_matrices(matriz1, matriz2):
    """Multiplica dos matrices si es posible"""
    if not matriz1 or not matriz2:
        return None
    
    filas1, columnas1 = len(matriz1), len(matriz1[0])
    filas2, columnas2 = len(matriz2), len(matriz2[0])
    
    # Verificar si la multiplicación es posible
    if columnas1 != filas2:
        return None
    
    # Crear matriz resultado
    resultado = crear_matriz(filas1, columnas2)
    
    for i in range(filas1):
        for j in range(columnas2):
            suma = 0
            for k in range(columnas1):
                suma += matriz1[i][k] * matriz2[k][j]
            resultado[i][j] = suma
    
    return resultado

def main():
    print("=== CALCULADORA DE MATRIZ TRANSPUESTA ===")
    
    matriz_actual = None
    
    while True:
        if matriz_actual:
            print(f"\nMatriz actual ({len(matriz_actual)}x{len(matriz_actual[0])}):")
            mostrar_matriz(matriz_actual, "")
        else:
            print("\nNo hay matriz cargada")
        
        print("\n1. Ingresar matriz manualmente")
        print("2. Generar matriz aleatoria")
        print("3. Calcular transpuesta")
        print("4. Mostrar propiedades de la matriz")
        print("5. Verificar si es simétrica")
        print("6. Comparar matriz con su transpuesta")
        print("7. Multiplicar matriz por su transpuesta")
        print("8. Crear matriz identidad")
        print("9. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                matriz_actual = ingresar_matriz()
                if matriz_actual:
                    print("✅ Matriz ingresada correctamente")
            
            elif opcion == 2:
                filas = int(input("Número de filas: "))
                columnas = int(input("Número de columnas: "))
                minimo = int(input("Valor mínimo (1 por defecto): ") or "1")
                maximo = int(input("Valor máximo (10 por defecto): ") or "10")
                
                if filas > 0 and columnas > 0:
                    matriz_actual = generar_matriz_aleatoria(filas, columnas, minimo, maximo)
                    print("✅ Matriz generada correctamente")
                else:
                    print("Error: Las dimensiones deben ser positivas")
            
            elif opcion == 3:
                if not matriz_actual:
                    print("Error: Primero carga una matriz")
                    continue
                
                transpuesta = transponer_matriz(matriz_actual)
                
                mostrar_matriz(matriz_actual, "Matriz Original")
                mostrar_matriz(transpuesta, "Matriz Transpuesta")
                
                # Guardar transpuesta como matriz actual
                guardar = input("\n¿Guardar transpuesta como matriz actual? (s/n): ").lower() == 's'
                if guardar:
                    matriz_actual = transpuesta
                    print("✅ Transpuesta guardada como matriz actual")
            
            elif opcion == 4:
                if not matriz_actual:
                    print("Error: Primero carga una matriz")
                    continue
                
                props = propiedades_matriz(matriz_actual)
                
                print(f"\n=== PROPIEDADES DE LA MATRIZ ===")
                print(f"Dimensiones: {props['dimensiones'][0]}x{props['dimensiones'][1]}")
                print(f"Es cuadrada: {'Sí' if props['es_cuadrada'] else 'No'}")
                print(f"Es simétrica: {'Sí' if props['es_simetrica'] else 'No'}")
                print(f"Total de elementos: {props['total_elementos']}")
                print(f"Elementos únicos: {props['elementos_unicos']}")
                print(f"Suma total: {props['suma_total']}")
                print(f"Promedio: {props['promedio']:.2f}")
                print(f"Valor mínimo: {props['minimo']}")
                print(f"Valor máximo: {props['maximo']}")
            
            elif opcion == 5:
                if not matriz_actual:
                    print("Error: Primero carga una matriz")
                    continue
                
                if not es_matriz_cuadrada(matriz_actual):
                    print("❌ La matriz no es cuadrada, por lo tanto no puede ser simétrica")
                    continue
                
                es_simetrica = es_matriz_simetrica(matriz_actual)
                
                if es_simetrica:
                    print("✅ La matriz ES simétrica (A = A^T)")
                else:
                    print("❌ La matriz NO es simétrica (A ≠ A^T)")
                
                # Mostrar comparación
                transpuesta = transponer_matriz(matriz_actual)
                mostrar_matriz(matriz_actual, "Matriz Original")
                mostrar_matriz(transpuesta, "Transpuesta")
            
            elif opcion == 6:
                if not matriz_actual:
                    print("Error: Primero carga una matriz")
                    continue
                
                transpuesta = transponer_matriz(matriz_actual)
                
                print(f"\n=== COMPARACIÓN MATRIZ vs TRANSPUESTA ===")
                mostrar_matriz(matriz_actual, "Matriz Original")
                mostrar_matriz(transpuesta, "Transpuesta")
                
                # Comparar elemento por elemento
                print(f"\nComparación elemento por elemento:")
                filas, columnas = len(matriz_actual), len(matriz_actual[0])
                diferencias = 0
                
                for i in range(min(filas, columnas)):  # Solo comparar hasta el mínimo
                    for j in range(min(columnas, filas)):
                        if i < len(transpuesta) and j < len(transpuesta[0]):
                            if matriz_actual[i][j] != transpuesta[i][j]:
                                print(f"  Diferencia en [{i+1}][{j+1}]: {matriz_actual[i][j]} ≠ {transpuesta[i][j]}")
                                diferencias += 1
                
                if diferencias == 0 and es_matriz_cuadrada(matriz_actual):
                    print("  ✅ Todos los elementos comparables son iguales (matriz simétrica)")
                elif diferencias == 0:
                    print("  ✅ No hay elementos comparables diferentes")
                else:
                    print(f"  ❌ Se encontraron {diferencias} diferencias")
            
            elif opcion == 7:
                if not matriz_actual:
                    print("Error: Primero carga una matriz")
                    continue
                
                transpuesta = transponer_matriz(matriz_actual)
                
                print("Opciones de multiplicación:")
                print("1. A × A^T")
                print("2. A^T × A")
                
                mult_opcion = int(input("Selecciona: "))
                
                if mult_opcion == 1:
                    resultado = multiplicar_matrices(matriz_actual, transpuesta)
                    operacion = "A × A^T"
                elif mult_opcion == 2:
                    resultado = multiplicar_matrices(transpuesta, matriz_actual)
                    operacion = "A^T × A"
                else:
                    print("Opción no válida")
                    continue
                
                if resultado:
                    print(f"\n=== RESULTADO DE {operacion} ===")
                    mostrar_matriz(matriz_actual, "Matriz A")
                    mostrar_matriz(transpuesta, "Transpuesta A^T")
                    mostrar_matriz(resultado, f"Resultado ({operacion})")
                    
                    # Verificar si el resultado es simétrico
                    if es_matriz_simetrica(resultado):
                        print("✅ El resultado es una matriz simétrica")
                else:
                    print("❌ No se puede realizar la multiplicación (dimensiones incompatibles)")
            
            elif opcion == 8:
                tamaño = int(input("Tamaño de la matriz identidad: "))
                
                if tamaño <= 0:
                    print("Error: El tamaño debe ser positivo")
                    continue
                
                # Crear matriz identidad
                identidad = crear_matriz(tamaño, tamaño, 0)
                for i in range(tamaño):
                    identidad[i][i] = 1
                
                matriz_actual = identidad
                print(f"✅ Matriz identidad {tamaño}x{tamaño} creada")
                mostrar_matriz(matriz_actual, "Matriz Identidad")
            
            elif opcion == 9:
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
