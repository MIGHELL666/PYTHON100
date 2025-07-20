"""
Proyecto 44: Calcular el determinante de una matriz
"""

def determinante_2x2(matriz):
    """Calcula el determinante de una matriz 2x2"""
    if len(matriz) != 2 or len(matriz[0]) != 2:
        return None, "La matriz no es 2x2"
    
    det = matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
    calculo = f"{matriz[0][0]} × {matriz[1][1]} - {matriz[0][1]} × {matriz[1][0]} = {det}"
    
    return det, calculo

def determinante_3x3(matriz):
    """Calcula el determinante de una matriz 3x3 usando la regla de Sarrus"""
    if len(matriz) != 3 or len(matriz[0]) != 3:
        return None, "La matriz no es 3x3", []
    
    # Método de Sarrus
    # Productos positivos (diagonal principal y paralelas)
    pos1 = matriz[0][0] * matriz[1][1] * matriz[2][2]
    pos2 = matriz[0][1] * matriz[1][2] * matriz[2][0]
    pos3 = matriz[0][2] * matriz[1][0] * matriz[2][1]
    
    # Productos negativos (diagonal secundaria y paralelas)
    neg1 = matriz[0][2] * matriz[1][1] * matriz[2][0]
    neg2 = matriz[0][0] * matriz[1][2] * matriz[2][1]
    neg3 = matriz[0][1] * matriz[1][0] * matriz[2][2]
    
    det = pos1 + pos2 + pos3 - neg1 - neg2 - neg3
    
    pasos = [
        f"Productos positivos:",
        f"  {matriz[0][0]} × {matriz[1][1]} × {matriz[2][2]} = {pos1}",
        f"  {matriz[0][1]} × {matriz[1][2]} × {matriz[2][0]} = {pos2}",
        f"  {matriz[0][2]} × {matriz[1][0]} × {matriz[2][1]} = {pos3}",
        f"Productos negativos:",
        f"  {matriz[0][2]} × {matriz[1][1]} × {matriz[2][0]} = {neg1}",
        f"  {matriz[0][0]} × {matriz[1][2]} × {matriz[2][1]} = {neg2}",
        f"  {matriz[0][1]} × {matriz[1][0]} × {matriz[2][2]} = {neg3}",
        f"Determinante = ({pos1} + {pos2} + {pos3}) - ({neg1} + {neg2} + {neg3}) = {det}"
    ]
    
    return det, f"Determinante = {det}", pasos

def obtener_menor(matriz, fila_excluir, columna_excluir):
    """Obtiene la matriz menor eliminando una fila y columna"""
    menor = []
    for i in range(len(matriz)):
        if i != fila_excluir:
            fila_menor = []
            for j in range(len(matriz[0])):
                if j != columna_excluir:
                    fila_menor.append(matriz[i][j])
            menor.append(fila_menor)
    return menor

def determinante_recursivo(matriz):
    """Calcula el determinante usando expansión por cofactores (recursivo)"""
    n = len(matriz)
    
    # Caso base: matriz 1x1
    if n == 1:
        return matriz[0][0], f"det = {matriz[0][0]}", []
    
    # Caso base: matriz 2x2
    if n == 2:
        return determinante_2x2(matriz)
    
    # Expansión por la primera fila
    det = 0
    pasos = [f"Expansión por la primera fila:"]
    
    for j in range(n):
        # Obtener menor
        menor = obtener_menor(matriz, 0, j)
        
        # Calcular determinante del menor recursivamente
        det_menor, _, _ = determinante_recursivo(menor)
        
        # Calcular cofactor
        signo = (-1) ** (0 + j)
        cofactor = signo * det_menor
        termino = matriz[0][j] * cofactor
        
        det += termino
        
        signo_str = "+" if signo > 0 else "-"
        pasos.append(f"  {signo_str} {matriz[0][j]} × det(menor_{0+1},{j+1}) = {signo_str} {matriz[0][j]} × {det_menor} = {termino}")
    
    pasos.append(f"Determinante total = {det}")
    
    return det, f"det = {det}", pasos

def es_matriz_cuadrada(matriz):
    """Verifica si una matriz es cuadrada"""
    if not matriz:
        return False
    return len(matriz) == len(matriz[0])

def matriz_cofactores(matriz):
    """Calcula la matriz de cofactores"""
    if not es_matriz_cuadrada(matriz):
        return None, "La matriz debe ser cuadrada"
    
    n = len(matriz)
    cofactores = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            menor = obtener_menor(matriz, i, j)
            det_menor, _, _ = determinante_recursivo(menor)
            signo = (-1) ** (i + j)
            cofactores[i][j] = signo * det_menor
    
    return cofactores, "Matriz de cofactores calculada"

def propiedades_determinante(matriz):
    """Analiza propiedades relacionadas con el determinante"""
    if not es_matriz_cuadrada(matriz):
        return {"error": "La matriz debe ser cuadrada"}
    
    det, _, _ = determinante_recursivo(matriz)
    
    propiedades = {
        'determinante': det,
        'es_singular': det == 0,
        'es_invertible': det != 0,
        'valor_absoluto': abs(det),
        'signo': 'positivo' if det > 0 else 'negativo' if det < 0 else 'cero'
    }
    
    return propiedades

def generar_matriz_cuadrada(tamaño, minimo=-5, maximo=5):
    """Genera una matriz cuadrada aleatoria"""
    import random
    matriz = []
    for i in range(tamaño):
        fila = []
        for j in range(tamaño):
            valor = random.randint(minimo, maximo)
            fila.append(valor)
        matriz.append(fila)
    return matriz

def mostrar_matriz_con_indices(matriz, nombre="Matriz"):
    """Muestra una matriz con índices de filas y columnas"""
    if not matriz:
        print(f"{nombre}: Matriz vacía")
        return
    
    n = len(matriz)
    
    print(f"\n{nombre} ({n}×{n}):")
    
    # Encabezado de columnas
    print("    ", end="")
    for j in range(n):
        print(f"{j+1:>6}", end="")
    print()
    
    # Filas con índices
    for i in range(n):
        print(f"{i+1:2d}: ", end="")
        for j in range(n):
            print(f"{matriz[i][j]:>6}", end="")
        print()

def main():
    print("=== CALCULADORA DE DETERMINANTES ===")
    
    matriz_actual = None
    
    while True:
        if matriz_actual:
            print(f"\nMatriz actual ({len(matriz_actual)}×{len(matriz_actual[0])}):")
            mostrar_matriz_con_indices(matriz_actual, "")
        else:
            print("\nNo hay matriz cargada")
        
        print("\n1. Ingresar matriz manualmente")
        print("2. Generar matriz cuadrada aleatoria")
        print("3. Calcular determinante")
        print("4. Calcular determinante con pasos")
        print("5. Matriz de cofactores")
        print("6. Propiedades del determinante")
        print("7. Ejemplos de matrices especiales")
        print("8. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                tamaño = int(input("Tamaño de la matriz cuadrada: "))
                
                if tamaño <= 0:
                    print("❌ El tamaño debe ser positivo")
                    continue
                
                print(f"Ingresa los elementos de la matriz {tamaño}×{tamaño}:")
                matriz = []
                
                for i in range(tamaño):
                    while True:
                        try:
                            entrada = input(f"Fila {i+1} (separados por espacios): ")
                            elementos = [float(x) for x in entrada.split()]
                            
                            if len(elementos) != tamaño:
                                print(f"Error: Se esperaban {tamaño} elementos")
                                continue
                            
                            matriz.append(elementos)
                            break
                        except ValueError:
                            print("Error: Ingresa solo números válidos")
                
                matriz_actual = matriz
                print("✅ Matriz ingresada correctamente")
            
            elif opcion == 2:
                tamaño = int(input("Tamaño de la matriz: "))
                minimo = int(input("Valor mínimo (-5 por defecto): ") or "-5")
                maximo = int(input("Valor máximo (5 por defecto): ") or "5")
                
                if tamaño <= 0:
                    print("❌ El tamaño debe ser positivo")
                    continue
                
                matriz_actual = generar_matriz_cuadrada(tamaño, minimo, maximo)
                print("✅ Matriz generada aleatoriamente")
            
            elif opcion == 3:
                if not matriz_actual:
                    print("❌ Error: Primero carga una matriz")
                    continue
                
                if not es_matriz_cuadrada(matriz_actual):
                    print("❌ Error: La matriz debe ser cuadrada")
                    continue
                
                det, mensaje, _ = determinante_recursivo(matriz_actual)
                
                print(f"\n=== CÁLCULO DEL DETERMINANTE ===")
                mostrar_matriz_con_indices(matriz_actual)
                print(f"\n✅ {mensaje}")
                
                # Información adicional
                if det == 0:
                    print("⚠️  La matriz es singular (no invertible)")
                else:
                    print("✅ La matriz es invertible")
            
            elif opcion == 4:
                if not matriz_actual:
                    print("❌ Error: Primero carga una matriz")
                    continue
                
                if not es_matriz_cuadrada(matriz_actual):
                    print("❌ Error: La matriz debe ser cuadrada")
                    continue
                
                tamaño = len(matriz_actual)
                
                if tamaño > 4:
                    print("⚠️  Matriz grande: los pasos pueden ser muy extensos")
                    continuar = input("¿Continuar? (s/n): ").lower() == 's'
                    if not continuar:
                        continue
                
                det, mensaje, pasos = determinante_recursivo(matriz_actual)
                
                print(f"\n=== CÁLCULO PASO A PASO ===")
                mostrar_matriz_con_indices(matriz_actual)
                
                print(f"\nPasos del cálculo:")
                for paso in pasos:
                    print(paso)
                
                print(f"\n✅ Resultado final: {mensaje}")
            
            elif opcion == 5:
                if not matriz_actual:
                    print("❌ Error: Primero carga una matriz")
                    continue
                
                if not es_matriz_cuadrada(matriz_actual):
                    print("❌ Error: La matriz debe ser cuadrada")
                    continue
                
                cofactores, mensaje = matriz_cofactores(matriz_actual)
                
                if cofactores:
                    print(f"\n=== MATRIZ DE COFACTORES ===")
                    mostrar_matriz_con_indices(matriz_actual, "Matriz Original")
                    mostrar_matriz_con_indices(cofactores, "Matriz de Cofactores")
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 6:
                if not matriz_actual:
                    print("❌ Error: Primero carga una matriz")
                    continue
                
                if not es_matriz_cuadrada(matriz_actual):
                    print("❌ Error: La matriz debe ser cuadrada")
                    continue
                
                props = propiedades_determinante(matriz_actual)
                
                if 'error' in props:
                    print(f"❌ {props['error']}")
                    continue
                
                print(f"\n=== PROPIEDADES DEL DETERMINANTE ===")
                print(f"Determinante: {props['determinante']}")
                print(f"Valor absoluto: {props['valor_absoluto']}")
                print(f"Signo: {props['signo']}")
                print(f"Es singular: {'Sí' if props['es_singular'] else 'No'}")
                print(f"Es invertible: {'Sí' if props['es_invertible'] else 'No'}")
                
                if props['es_singular']:
                    print("⚠️  La matriz no tiene inversa")
                else:
                    print("✅ La matriz tiene inversa")
            
            elif opcion == 7:
                print("\n=== EJEMPLOS DE MATRICES ESPECIALES ===")
                print("1. Matriz identidad 3×3")
                print("2. Matriz con determinante 0")
                print("3. Matriz triangular superior")
                print("4. Matriz con determinante negativo")
                
                ejemplo = int(input("Selecciona ejemplo: "))
                
                if ejemplo == 1:
                    matriz_actual = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
                    print("✅ Matriz identidad cargada (det = 1)")
                
                elif ejemplo == 2:
                    matriz_actual = [[1, 2, 3], [2, 4, 6], [1, 2, 3]]
                    print("✅ Matriz singular cargada (det = 0)")
                
                elif ejemplo == 3:
                    matriz_actual = [[2, 3, 1], [0, 4, 2], [0, 0, 5]]
                    print("✅ Matriz triangular superior cargada")
                
                elif ejemplo == 4:
                    matriz_actual = [[1, 2], [3, 4]]
                    print("✅ Matriz con determinante negativo cargada")
                
                else:
                    print("❌ Ejemplo no válido")
            
            elif opcion == 8:
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
