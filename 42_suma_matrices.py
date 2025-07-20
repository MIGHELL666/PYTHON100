"""
Proyecto 42: Sumar dos matrices
"""

def crear_matriz_ceros(filas, columnas):
    """Crea una matriz de ceros"""
    return [[0 for _ in range(columnas)] for _ in range(filas)]

def sumar_matrices(matriz1, matriz2):
    """Suma dos matrices si tienen las mismas dimensiones"""
    if not matriz1 or not matriz2:
        return None, "Una o ambas matrices están vacías"
    
    filas1, columnas1 = len(matriz1), len(matriz1[0])
    filas2, columnas2 = len(matriz2), len(matriz2[0])
    
    if filas1 != filas2 or columnas1 != columnas2:
        return None, f"Dimensiones incompatibles: {filas1}x{columnas1} vs {filas2}x{columnas2}"
    
    # Crear matriz resultado
    resultado = crear_matriz_ceros(filas1, columnas1)
    
    for i in range(filas1):
        for j in range(columnas1):
            resultado[i][j] = matriz1[i][j] + matriz2[i][j]
    
    return resultado, "Suma realizada correctamente"

def restar_matrices(matriz1, matriz2):
    """Resta dos matrices si tienen las mismas dimensiones"""
    if not matriz1 or not matriz2:
        return None, "Una o ambas matrices están vacías"
    
    filas1, columnas1 = len(matriz1), len(matriz1[0])
    filas2, columnas2 = len(matriz2), len(matriz2[0])
    
    if filas1 != filas2 or columnas1 != columnas2:
        return None, f"Dimensiones incompatibles: {filas1}x{columnas1} vs {filas2}x{columnas2}"
    
    # Crear matriz resultado
    resultado = crear_matriz_ceros(filas1, columnas1)
    
    for i in range(filas1):
        for j in range(columnas1):
            resultado[i][j] = matriz1[i][j] - matriz2[i][j]
    
    return resultado, "Resta realizada correctamente"

def multiplicar_matriz_escalar(matriz, escalar):
    """Multiplica una matriz por un escalar"""
    if not matriz:
        return None, "Matriz vacía"
    
    filas, columnas = len(matriz), len(matriz[0])
    resultado = crear_matriz_ceros(filas, columnas)
    
    for i in range(filas):
        for j in range(columnas):
            resultado[i][j] = matriz[i][j] * escalar
    
    return resultado, f"Multiplicación por escalar {escalar} realizada"

def generar_matriz_aleatoria(filas, columnas, minimo=-10, maximo=10):
    """Genera una matriz con valores aleatorios"""
    import random
    matriz = []
    
    for i in range(filas):
        fila = []
        for j in range(columnas):
            valor = random.randint(minimo, maximo)
            fila.append(valor)
        matriz.append(fila)
    
    return matriz

def ingresar_matriz_simple(nombre="matriz"):
    """Permite ingresar una matriz de forma simplificada"""
    try:
        print(f"\nIngresando {nombre}:")
        filas = int(input("Número de filas: "))
        columnas = int(input("Número de columnas: "))
        
        if filas <= 0 or columnas <= 0:
            return None, "Dimensiones inválidas"
        
        print(f"Ingresa los elementos fila por fila (separados por espacios):")
        matriz = []
        
        for i in range(filas):
            while True:
                try:
                    entrada = input(f"Fila {i+1}: ")
                    elementos = [float(x) for x in entrada.split()]
                    
                    if len(elementos) != columnas:
                        print(f"Error: Se esperaban {columnas} elementos, se recibieron {len(elementos)}")
                        continue
                    
                    matriz.append(elementos)
                    break
                except ValueError:
                    print("Error: Ingresa solo números válidos")
        
        return matriz, "Matriz ingresada correctamente"
        
    except ValueError:
        return None, "Error en la entrada de datos"

def mostrar_operacion_matrices(matriz1, matriz2, resultado, operacion):
    """Muestra una operación entre matrices de forma visual"""
    if not all([matriz1, matriz2, resultado]):
        print("Error: Matrices inválidas")
        return
    
    filas = len(matriz1)
    
    # Calcular anchos para alineación
    def calcular_ancho_matriz(matriz):
        max_ancho = 0
        for fila in matriz:
            for elemento in fila:
                ancho = len(str(elemento))
                if ancho > max_ancho:
                    max_ancho = ancho
        return max_ancho
    
    ancho1 = calcular_ancho_matriz(matriz1)
    ancho2 = calcular_ancho_matriz(matriz2)
    ancho_resultado = calcular_ancho_matriz(resultado)
    
    print(f"\n=== OPERACIÓN: MATRIZ A {operacion} MATRIZ B ===")
    
    for i in range(filas):
        # Matriz A
        fila1_str = " ".join(f"{elemento:>{ancho1}}" for elemento in matriz1[i])
        
        # Operador (solo en la fila del medio)
        if i == filas // 2:
            operador = f" {operacion} "
        else:
            operador = "   "
        
        # Matriz B
        fila2_str = " ".join(f"{elemento:>{ancho2}}" for elemento in matriz2[i])
        
        # Igual (solo en la fila del medio)
        if i == filas // 2:
            igual = " = "
        else:
            igual = "   "
        
        # Resultado
        resultado_str = " ".join(f"{elemento:>{ancho_resultado}}" for elemento in resultado[i])
        
        print(f"  [{fila1_str}]{operador}[{fila2_str}]{igual}[{resultado_str}]")

def operaciones_multiples(matriz1, matriz2):
    """Realiza múltiples operaciones entre dos matrices"""
    if not matriz1 or not matriz2:
        return {}
    
    resultados = {}
    
    # Suma
    suma, msg_suma = sumar_matrices(matriz1, matriz2)
    if suma:
        resultados['suma'] = suma
    
    # Resta A - B
    resta_ab, msg_resta_ab = restar_matrices(matriz1, matriz2)
    if resta_ab:
        resultados['resta_ab'] = resta_ab
    
    # Resta B - A
    resta_ba, msg_resta_ba = restar_matrices(matriz2, matriz1)
    if resta_ba:
        resultados['resta_ba'] = resta_ba
    
    return resultados

def main():
    print("=== CALCULADORA DE SUMA DE MATRICES ===")
    
    matriz_a = None
    matriz_b = None
    
    while True:
        print(f"\nEstado actual:")
        if matriz_a:
            print(f"Matriz A: {len(matriz_a)}x{len(matriz_a[0])}")
        else:
            print("Matriz A: No cargada")
        
        if matriz_b:
            print(f"Matriz B: {len(matriz_b)}x{len(matriz_b[0])}")
        else:
            print("Matriz B: No cargada")
        
        print("\n1. Ingresar Matriz A")
        print("2. Ingresar Matriz B")
        print("3. Generar matrices aleatorias del mismo tamaño")
        print("4. Sumar matrices (A + B)")
        print("5. Restar matrices (A - B)")
        print("6. Restar matrices (B - A)")
        print("7. Multiplicar matriz por escalar")
        print("8. Mostrar matrices actuales")
        print("9. Operaciones múltiples")
        print("10. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                matriz, mensaje = ingresar_matriz_simple("Matriz A")
                if matriz:
                    matriz_a = matriz
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 2:
                matriz, mensaje = ingresar_matriz_simple("Matriz B")
                if matriz:
                    matriz_b = matriz
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 3:
                filas = int(input("Número de filas: "))
                columnas = int(input("Número de columnas: "))
                minimo = int(input("Valor mínimo (-10 por defecto): ") or "-10")
                maximo = int(input("Valor máximo (10 por defecto): ") or "10")
                
                if filas > 0 and columnas > 0:
                    matriz_a = generar_matriz_aleatoria(filas, columnas, minimo, maximo)
                    matriz_b = generar_matriz_aleatoria(filas, columnas, minimo, maximo)
                    print("✅ Matrices A y B generadas aleatoriamente")
                else:
                    print("❌ Dimensiones inválidas")
            
            elif opcion == 4:
                if not matriz_a or not matriz_b:
                    print("❌ Error: Necesitas cargar ambas matrices")
                    continue
                
                resultado, mensaje = sumar_matrices(matriz_a, matriz_b)
                
                if resultado:
                    mostrar_operacion_matrices(matriz_a, matriz_b, resultado, "+")
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 5:
                if not matriz_a or not matriz_b:
                    print("❌ Error: Necesitas cargar ambas matrices")
                    continue
                
                resultado, mensaje = restar_matrices(matriz_a, matriz_b)
                
                if resultado:
                    mostrar_operacion_matrices(matriz_a, matriz_b, resultado, "-")
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 6:
                if not matriz_a or not matriz_b:
                    print("❌ Error: Necesitas cargar ambas matrices")
                    continue
                
                resultado, mensaje = restar_matrices(matriz_b, matriz_a)
                
                if resultado:
                    mostrar_operacion_matrices(matriz_b, matriz_a, resultado, "-")
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 7:
                print("¿Qué matriz multiplicar?")
                print("1. Matriz A")
                print("2. Matriz B")
                
                matriz_opcion = int(input("Selecciona: "))
                escalar = float(input("Ingresa el escalar: "))
                
                if matriz_opcion == 1 and matriz_a:
                    resultado, mensaje = multiplicar_matriz_escalar(matriz_a, escalar)
                    matriz_original = matriz_a
                    nombre = "A"
                elif matriz_opcion == 2 and matriz_b:
                    resultado, mensaje = multiplicar_matriz_escalar(matriz_b, escalar)
                    matriz_original = matriz_b
                    nombre = "B"
                else:
                    print("❌ Matriz no válida o no cargada")
                    continue
                
                if resultado:
                    print(f"\n=== MULTIPLICACIÓN DE MATRIZ {nombre} POR ESCALAR {escalar} ===")
                    
                    # Mostrar lado a lado
                    filas = len(matriz_original)
                    for i in range(filas):
                        fila_orig = " ".join(f"{elem:>4}" for elem in matriz_original[i])
                        fila_result = " ".join(f"{elem:>4}" for elem in resultado[i])
                        
                        if i == filas // 2:
                            print(f"  [{fila_orig}] × {escalar} = [{fila_result}]")
                        else:
                            print(f"  [{fila_orig}]     [{fila_result}]")
                    
                    print(f"✅ {mensaje}")
            
            elif opcion == 8:
                if matriz_a:
                    print(f"\n=== MATRIZ A ({len(matriz_a)}x{len(matriz_a[0])}) ===")
                    for fila in matriz_a:
                        fila_str = " ".join(f"{elem:>6}" for elem in fila)
                        print(f"  [{fila_str}]")
                else:
                    print("\nMatriz A: No cargada")
                
                if matriz_b:
                    print(f"\n=== MATRIZ B ({len(matriz_b)}x{len(matriz_b[0])}) ===")
                    for fila in matriz_b:
                        fila_str = " ".join(f"{elem:>6}" for elem in fila)
                        print(f"  [{fila_str}]")
                else:
                    print("\nMatriz B: No cargada")
            
            elif opcion == 9:
                if not matriz_a or not matriz_b:
                    print("❌ Error: Necesitas cargar ambas matrices")
                    continue
                
                resultados = operaciones_multiples(matriz_a, matriz_b)
                
                if not resultados:
                    print("❌ No se pudieron realizar las operaciones (dimensiones incompatibles)")
                    continue
                
                print(f"\n=== OPERACIONES MÚLTIPLES ===")
                
                if 'suma' in resultados:
                    print("\n1. SUMA (A + B):")
                    mostrar_operacion_matrices(matriz_a, matriz_b, resultados['suma'], "+")
                
                if 'resta_ab' in resultados:
                    print("\n2. RESTA (A - B):")
                    mostrar_operacion_matrices(matriz_a, matriz_b, resultados['resta_ab'], "-")
                
                if 'resta_ba' in resultados:
                    print("\n3. RESTA (B - A):")
                    mostrar_operacion_matrices(matriz_b, matriz_a, resultados['resta_ba'], "-")
            
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
