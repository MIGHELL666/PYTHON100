"""
Proyecto 43: Multiplicar dos matrices
"""

def multiplicar_matrices(matriz1, matriz2):
    """Multiplica dos matrices si es posible (columnas de A = filas de B)"""
    if not matriz1 or not matriz2:
        return None, "Una o ambas matrices están vacías"
    
    filas1, columnas1 = len(matriz1), len(matriz1[0])
    filas2, columnas2 = len(matriz2), len(matriz2[0])
    
    # Verificar compatibilidad para multiplicación
    if columnas1 != filas2:
        return None, f"Multiplicación imposible: {filas1}x{columnas1} × {filas2}x{columnas2} (columnas de A ≠ filas de B)"
    
    # Crear matriz resultado (filas1 × columnas2)
    resultado = [[0 for _ in range(columnas2)] for _ in range(filas1)]
    
    # Realizar multiplicación
    for i in range(filas1):
        for j in range(columnas2):
            suma = 0
            for k in range(columnas1):
                suma += matriz1[i][k] * matriz2[k][j]
            resultado[i][j] = suma
    
    return resultado, f"Multiplicación exitosa: resultado {filas1}x{columnas2}"

def multiplicar_matrices_con_pasos(matriz1, matriz2, mostrar_pasos=False):
    """Multiplica matrices mostrando los pasos del cálculo"""
    if not matriz1 or not matriz2:
        return None, [], "Matrices inválidas"
    
    filas1, columnas1 = len(matriz1), len(matriz1[0])
    filas2, columnas2 = len(matriz2), len(matriz2[0])
    
    if columnas1 != filas2:
        return None, [], f"Dimensiones incompatibles: {filas1}x{columnas1} × {filas2}x{columnas2}"
    
    resultado = [[0 for _ in range(columnas2)] for _ in range(filas1)]
    pasos = []
    
    for i in range(filas1):
        for j in range(columnas2):
            suma = 0
            calculo_detalle = []
            
            for k in range(columnas1):
                producto = matriz1[i][k] * matriz2[k][j]
                suma += producto
                calculo_detalle.append(f"{matriz1[i][k]}×{matriz2[k][j]}={producto}")
            
            resultado[i][j] = suma
            paso = {
                'posicion': (i, j),
                'calculo': " + ".join(calculo_detalle),
                'resultado': suma
            }
            pasos.append(paso)
            
            if mostrar_pasos:
                print(f"Elemento [{i+1}][{j+1}]: {paso['calculo']} = {suma}")
    
    return resultado, pasos, "Multiplicación completada"

def es_multiplicacion_posible(matriz1, matriz2):
    """Verifica si dos matrices se pueden multiplicar"""
    if not matriz1 or not matriz2:
        return False, "Matrices vacías"
    
    columnas1 = len(matriz1[0])
    filas2 = len(matriz2)
    
    if columnas1 == filas2:
        return True, f"Multiplicación posible: {len(matriz1)}x{columnas1} × {filas2}x{len(matriz2[0])} = {len(matriz1)}x{len(matriz2[0])}"
    else:
        return False, f"Multiplicación imposible: columnas de A ({columnas1}) ≠ filas de B ({filas2})"

def potencia_matriz(matriz, exponente):
    """Calcula la potencia de una matriz cuadrada"""
    if not matriz:
        return None, "Matriz vacía"
    
    filas, columnas = len(matriz), len(matriz[0])
    
    if filas != columnas:
        return None, "La matriz debe ser cuadrada para calcular potencias"
    
    if exponente < 0:
        return None, "Exponente negativo no soportado"
    
    if exponente == 0:
        # Matriz identidad
        identidad = [[0 for _ in range(columnas)] for _ in range(filas)]
        for i in range(filas):
            identidad[i][i] = 1
        return identidad, "A^0 = Matriz Identidad"
    
    if exponente == 1:
        return [fila[:] for fila in matriz], "A^1 = A"
    
    # Multiplicación sucesiva
    resultado = [fila[:] for fila in matriz]  # Copia de la matriz original
    
    for _ in range(exponente - 1):
        resultado, mensaje = multiplicar_matrices(resultado, matriz)
        if not resultado:
            return None, f"Error en multiplicación: {mensaje}"
    
    return resultado, f"A^{exponente} calculada"

def crear_matriz_identidad(tamaño):
    """Crea una matriz identidad de tamaño dado"""
    identidad = [[0 for _ in range(tamaño)] for _ in range(tamaño)]
    for i in range(tamaño):
        identidad[i][i] = 1
    return identidad

def mostrar_multiplicacion_visual(matriz1, matriz2, resultado):
    """Muestra la multiplicación de matrices de forma visual"""
    if not all([matriz1, matriz2, resultado]):
        print("Error: Matrices inválidas")
        return
    
    filas1, columnas1 = len(matriz1), len(matriz1[0])
    filas2, columnas2 = len(matriz2), len(matriz2[0])
    
    print(f"\n=== MULTIPLICACIÓN DE MATRICES ===")
    print(f"A ({filas1}×{columnas1}) × B ({filas2}×{columnas2}) = C ({len(resultado)}×{len(resultado[0])})")
    
    # Mostrar matrices lado a lado (para matrices pequeñas)
    if filas1 <= 5 and columnas2 <= 5:
        max_filas = max(filas1, filas2, len(resultado))
        
        for i in range(max_filas):
            # Matriz A
            if i < filas1:
                fila_a = " ".join(f"{matriz1[i][j]:>4}" for j in range(columnas1))
                print(f"  [{fila_a}]", end="")
            else:
                print(f"  {' ' * (columnas1 * 5 + 1)}", end="")
            
            # Operador
            if i == max_filas // 2:
                print("  ×  ", end="")
            else:
                print("     ", end="")
            
            # Matriz B
            if i < filas2:
                fila_b = " ".join(f"{matriz2[i][j]:>4}" for j in range(columnas2))
                print(f"[{fila_b}]", end="")
            else:
                print(f"{' ' * (columnas2 * 5 + 1)}", end="")
            
            # Igual
            if i == max_filas // 2:
                print("  =  ", end="")
            else:
                print("     ", end="")
            
            # Resultado
            if i < len(resultado):
                fila_c = " ".join(f"{resultado[i][j]:>4}" for j in range(len(resultado[0])))
                print(f"[{fila_c}]")
            else:
                print()
    else:
        # Para matrices grandes, mostrar por separado
        print("\nMatriz A:")
        for fila in matriz1:
            fila_str = " ".join(f"{elem:>6}" for elem in fila)
            print(f"  [{fila_str}]")
        
        print("\nMatriz B:")
        for fila in matriz2:
            fila_str = " ".join(f"{elem:>6}" for elem in fila)
            print(f"  [{fila_str}]")
        
        print("\nResultado (A × B):")
        for fila in resultado:
            fila_str = " ".join(f"{elem:>6}" for elem in fila)
            print(f"  [{fila_str}]")

def main():
    print("=== MULTIPLICADOR DE MATRICES ===")
    
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
        
        # Verificar si se pueden multiplicar
        if matriz_a and matriz_b:
            posible, mensaje = es_multiplicacion_posible(matriz_a, matriz_b)
            print(f"A × B: {'✅ Posible' if posible else '❌ No posible'} - {mensaje}")
            
            posible_ba, mensaje_ba = es_multiplicacion_posible(matriz_b, matriz_a)
            print(f"B × A: {'✅ Posible' if posible_ba else '❌ No posible'} - {mensaje_ba}")
        
        print("\n1. Ingresar Matriz A")
        print("2. Ingresar Matriz B")
        print("3. Generar matrices compatibles")
        print("4. Multiplicar A × B")
        print("5. Multiplicar B × A")
        print("6. Multiplicar con pasos detallados")
        print("7. Calcular potencia de matriz")
        print("8. Crear matriz identidad")
        print("9. Mostrar matrices actuales")
        print("10. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                matriz_a = ingresar_matriz("Matriz A")
                if matriz_a:
                    print("✅ Matriz A cargada")
            
            elif opcion == 2:
                matriz_b = ingresar_matriz("Matriz B")
                if matriz_b:
                    print("✅ Matriz B cargada")
            
            elif opcion == 3:
                print("Generando matrices compatibles para multiplicación...")
                filas_a = int(input("Filas de matriz A: "))
                columnas_a = int(input("Columnas de matriz A: "))
                columnas_b = int(input("Columnas de matriz B: "))
                
                # filas_b = columnas_a (para que sean compatibles)
                filas_b = columnas_a
                
                print(f"Generando A({filas_a}×{columnas_a}) y B({filas_b}×{columnas_b})")
                
                import random
                matriz_a = [[random.randint(1, 9) for _ in range(columnas_a)] for _ in range(filas_a)]
                matriz_b = [[random.randint(1, 9) for _ in range(columnas_b)] for _ in range(filas_b)]
                
                print("✅ Matrices compatibles generadas")
            
            elif opcion == 4:
                if not matriz_a or not matriz_b:
                    print("❌ Error: Necesitas cargar ambas matrices")
                    continue
                
                resultado, mensaje = multiplicar_matrices(matriz_a, matriz_b)
                
                if resultado:
                    mostrar_multiplicacion_visual(matriz_a, matriz_b, resultado)
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 5:
                if not matriz_a or not matriz_b:
                    print("❌ Error: Necesitas cargar ambas matrices")
                    continue
                
                resultado, mensaje = multiplicar_matrices(matriz_b, matriz_a)
                
                if resultado:
                    mostrar_multiplicacion_visual(matriz_b, matriz_a, resultado)
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 6:
                if not matriz_a or not matriz_b:
                    print("❌ Error: Necesitas cargar ambas matrices")
                    continue
                
                mostrar = input("¿Mostrar pasos detallados? (s/n): ").lower() == 's'
                
                resultado, pasos, mensaje = multiplicar_matrices_con_pasos(matriz_a, matriz_b, mostrar)
                
                if resultado:
                    if not mostrar:
                        print(f"\n=== CÁLCULO DETALLADO ===")
                        for paso in pasos[:6]:  # Mostrar solo los primeros 6 pasos
                            pos = paso['posicion']
                            print(f"C[{pos[0]+1}][{pos[1]+1}] = {paso['calculo']} = {paso['resultado']}")
                        
                        if len(pasos) > 6:
                            print(f"... y {len(pasos) - 6} cálculos más")
                    
                    mostrar_multiplicacion_visual(matriz_a, matriz_b, resultado)
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 7:
                print("¿Qué matriz elevar a potencia?")
                print("1. Matriz A")
                print("2. Matriz B")
                
                matriz_opcion = int(input("Selecciona: "))
                exponente = int(input("Exponente: "))
                
                if matriz_opcion == 1 and matriz_a:
                    resultado, mensaje = potencia_matriz(matriz_a, exponente)
                    matriz_base = matriz_a
                    nombre = "A"
                elif matriz_opcion == 2 and matriz_b:
                    resultado, mensaje = potencia_matriz(matriz_b, exponente)
                    matriz_base = matriz_b
                    nombre = "B"
                else:
                    print("❌ Matriz no válida o no cargada")
                    continue
                
                if resultado:
                    print(f"\n=== {nombre}^{exponente} ===")
                    
                    print(f"Matriz {nombre}:")
                    for fila in matriz_base:
                        fila_str = " ".join(f"{elem:>4}" for elem in fila)
                        print(f"  [{fila_str}]")
                    
                    print(f"\n{nombre}^{exponente}:")
                    for fila in resultado:
                        fila_str = " ".join(f"{elem:>6}" for elem in fila)
                        print(f"  [{fila_str}]")
                    
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 8:
                tamaño = int(input("Tamaño de la matriz identidad: "))
                
                if tamaño <= 0:
                    print("❌ El tamaño debe ser positivo")
                    continue
                
                identidad = crear_matriz_identidad(tamaño)
                
                print("¿Asignar como matriz A o B?")
                print("1. Matriz A")
                print("2. Matriz B")
                
                asignacion = int(input("Selecciona: "))
                
                if asignacion == 1:
                    matriz_a = identidad
                    print(f"✅ Matriz identidad {tamaño}×{tamaño} asignada como Matriz A")
                elif asignacion == 2:
                    matriz_b = identidad
                    print(f"✅ Matriz identidad {tamaño}×{tamaño} asignada como Matriz B")
                
                print(f"\nMatriz Identidad {tamaño}×{tamaño}:")
                for fila in identidad:
                    fila_str = " ".join(f"{elem:>3}" for elem in fila)
                    print(f"  [{fila_str}]")
            
            elif opcion == 9:
                if matriz_a:
                    print(f"\n=== MATRIZ A ({len(matriz_a)}×{len(matriz_a[0])}) ===")
                    for fila in matriz_a:
                        fila_str = " ".join(f"{elem:>6}" for elem in fila)
                        print(f"  [{fila_str}]")
                else:
                    print("\nMatriz A: No cargada")
                
                if matriz_b:
                    print(f"\n=== MATRIZ B ({len(matriz_b)}×{len(matriz_b[0])}) ===")
                    for fila in matriz_b:
                        fila_str = " ".join(f"{elem:>6}" for elem in fila)
                        print(f"  [{fila_str}]")
                else:
                    print("\nMatriz B: No cargada")
            
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

def ingresar_matriz(nombre="matriz"):
    """Función auxiliar para ingresar una matriz"""
    try:
        print(f"\nIngresando {nombre}:")
        filas = int(input("Número de filas: "))
        columnas = int(input("Número de columnas: "))
        
        if filas <= 0 or columnas <= 0:
            print("❌ Dimensiones inválidas")
            return None
        
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
        
        return matriz
        
    except ValueError:
        print("❌ Error en la entrada de datos")
        return None

if __name__ == "__main__":
    main()
