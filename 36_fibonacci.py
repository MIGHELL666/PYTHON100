"""
Proyecto 36: Secuencia de Fibonacci
"""

def fibonacci_iterativo(n):
    """Genera la secuencia de Fibonacci de forma iterativa"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    secuencia = [0, 1]
    for i in range(2, n):
        siguiente = secuencia[i-1] + secuencia[i-2]
        secuencia.append(siguiente)
    
    return secuencia

def fibonacci_recursivo(n):
    """Calcula el n-ésimo número de Fibonacci recursivamente"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursivo(n-1) + fibonacci_recursivo(n-2)

def fibonacci_optimizado(n, memo={}):
    """Fibonacci con memoización para optimizar recursión"""
    if n in memo:
        return memo[n]
    
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        memo[n] = fibonacci_optimizado(n-1, memo) + fibonacci_optimizado(n-2, memo)
        return memo[n]

def es_numero_fibonacci(numero):
    """Verifica si un número pertenece a la secuencia de Fibonacci"""
    if numero < 0:
        return False
    
    a, b = 0, 1
    if numero == a or numero == b:
        return True
    
    while b < numero:
        a, b = b, a + b
        if b == numero:
            return True
    
    return False

def main():
    print("=== SECUENCIA DE FIBONACCI ===")
    
    while True:
        print("\n1. Generar secuencia (iterativo)")
        print("2. Calcular n-ésimo número (recursivo)")
        print("3. Calcular n-ésimo número (optimizado)")
        print("4. Verificar si un número es Fibonacci")
        print("5. Mostrar propiedades de la secuencia")
        print("6. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                n = int(input("¿Cuántos números de Fibonacci generar? "))
                if n <= 0:
                    print("Error: Ingresa un número positivo")
                    continue
                
                secuencia = fibonacci_iterativo(n)
                print(f"\nPrimeros {n} números de Fibonacci:")
                
                # Mostrar en filas de 10
                for i in range(0, len(secuencia), 10):
                    fila = secuencia[i:i+10]
                    print(" ".join(f"{num:8d}" for num in fila))
                
                if n > 1:
                    print(f"\nÚltimo número: {secuencia[-1]}")
                    if n > 2:
                        ratio = secuencia[-1] / secuencia[-2]
                        print(f"Ratio áureo aproximado: {ratio:.6f}")
            
            elif opcion == 2:
                n = int(input("¿Qué posición de Fibonacci calcular? "))
                if n < 0:
                    print("Error: Ingresa un número no negativo")
                    continue
                
                if n > 35:
                    print("Advertencia: Números grandes pueden tardar mucho tiempo")
                    continuar = input("¿Continuar? (s/n): ").lower() == 's'
                    if not continuar:
                        continue
                
                resultado = fibonacci_recursivo(n)
                print(f"Fibonacci({n}) = {resultado}")
            
            elif opcion == 3:
                n = int(input("¿Qué posición de Fibonacci calcular? "))
                if n < 0:
                    print("Error: Ingresa un número no negativo")
                    continue
                
                resultado = fibonacci_optimizado(n)
                print(f"Fibonacci({n}) = {resultado}")
                
                # Mostrar algunos números anteriores para contexto
                if n > 0:
                    print(f"\nContexto:")
                    inicio = max(0, n-5)
                    for i in range(inicio, n+1):
                        fib_i = fibonacci_optimizado(i)
                        print(f"F({i}) = {fib_i}")
            
            elif opcion == 4:
                numero = int(input("Número a verificar: "))
                
                if es_numero_fibonacci(numero):
                    print(f"✅ {numero} SÍ es un número de Fibonacci")
                    
                    # Encontrar su posición
                    secuencia = fibonacci_iterativo(50)  # Generar suficientes números
                    try:
                        posicion = secuencia.index(numero)
                        print(f"Es el número en la posición {posicion}")
                    except ValueError:
                        print("Posición no encontrada en los primeros 50 números")
                else:
                    print(f"❌ {numero} NO es un número de Fibonacci")
                
                # Mostrar los números Fibonacci más cercanos
                secuencia = fibonacci_iterativo(30)
                menores = [f for f in secuencia if f < numero]
                mayores = [f for f in secuencia if f > numero]
                
                if menores:
                    print(f"Fibonacci menor más cercano: {menores[-1]}")
                if mayores:
                    print(f"Fibonacci mayor más cercano: {mayores[0]}")
            
            elif opcion == 5:
                n = int(input("¿Cuántos números analizar? (20 por defecto): ") or "20")
                secuencia = fibonacci_iterativo(n)
                
                print(f"\n=== PROPIEDADES DE LOS PRIMEROS {n} NÚMEROS ===")
                print(f"Secuencia: {secuencia}")
                
                if len(secuencia) > 1:
                    print(f"\nSuma total: {sum(secuencia)}")
                    
                    # Ratios entre números consecutivos
                    print(f"\nRatios entre números consecutivos:")
                    for i in range(1, min(10, len(secuencia))):
                        if secuencia[i-1] != 0:
                            ratio = secuencia[i] / secuencia[i-1]
                            print(f"F({i})/F({i-1}) = {secuencia[i]}/{secuencia[i-1]} = {ratio:.6f}")
                    
                    # Números pares e impares
                    pares = [f for f in secuencia if f % 2 == 0]
                    impares = [f for f in secuencia if f % 2 == 1]
                    print(f"\nNúmeros pares: {len(pares)} → {pares[:10]}{'...' if len(pares) > 10 else ''}")
                    print(f"Números impares: {len(impares)} → {impares[:10]}{'...' if len(impares) > 10 else ''}")
            
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
    main()
