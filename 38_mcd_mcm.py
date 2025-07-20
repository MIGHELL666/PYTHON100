"""
Proyecto 38: Calcular MCD (Máximo Común Divisor) y MCM (Mínimo Común Múltiplo)
"""

def mcd_euclidiano(a, b):
    """Calcula el MCD usando el algoritmo de Euclides"""
    while b:
        a, b = b, a % b
    return abs(a)

def mcd_recursivo(a, b):
    """Calcula el MCD de forma recursiva"""
    if b == 0:
        return abs(a)
    return mcd_recursivo(b, a % b)

def mcm(a, b):
    """Calcula el MCM usando la relación MCM(a,b) = |a*b| / MCD(a,b)"""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // mcd_euclidiano(a, b)

def mcd_multiple(*numeros):
    """Calcula el MCD de múltiples números"""
    if not numeros:
        return 0
    
    resultado = abs(numeros[0])
    for num in numeros[1:]:
        resultado = mcd_euclidiano(resultado, abs(num))
        if resultado == 1:  # Optimización: si MCD es 1, no puede ser menor
            break
    
    return resultado

def mcm_multiple(*numeros):
    """Calcula el MCM de múltiples números"""
    if not numeros:
        return 0
    
    if 0 in numeros:
        return 0
    
    resultado = abs(numeros[0])
    for num in numeros[1:]:
        resultado = mcm(resultado, abs(num))
    
    return resultado

def encontrar_divisores(numero):
    """Encuentra todos los divisores de un número"""
    if numero == 0:
        return []
    
    numero = abs(numero)
    divisores = []
    
    for i in range(1, int(numero**0.5) + 1):
        if numero % i == 0:
            divisores.append(i)
            if i != numero // i:  # Evitar duplicados para cuadrados perfectos
                divisores.append(numero // i)
    
    return sorted(divisores)

def algoritmo_euclides_extendido(a, b):
    """Algoritmo de Euclides extendido para encontrar coeficientes de Bézout"""
    if b == 0:
        return a, 1, 0
    
    mcd, x1, y1 = algoritmo_euclides_extendido(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    return mcd, x, y

def main():
    print("=== CALCULADORA DE MCD Y MCM ===")
    
    while True:
        print("\n1. MCD de dos números")
        print("2. MCM de dos números")
        print("3. MCD y MCM de múltiples números")
        print("4. Análisis completo de dos números")
        print("5. Algoritmo de Euclides paso a paso")
        print("6. Encontrar divisores comunes")
        print("7. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                a = int(input("Primer número: "))
                b = int(input("Segundo número: "))
                
                mcd_resultado = mcd_euclidiano(a, b)
                
                print(f"\nMCD({a}, {b}) = {mcd_resultado}")
                
                # Verificación con método recursivo
                mcd_rec = mcd_recursivo(a, b)
                print(f"Verificación (recursivo): {mcd_rec}")
                
                # Información adicional
                if mcd_resultado == 1:
                    print("Los números son coprimos (relativamente primos)")
                else:
                    print(f"Los números tienen {mcd_resultado} como factor común")
            
            elif opcion == 2:
                a = int(input("Primer número: "))
                b = int(input("Segundo número: "))
                
                if a == 0 or b == 0:
                    print("El MCM de cualquier número con 0 es 0")
                    continue
                
                mcm_resultado = mcm(a, b)
                
                print(f"\nMCM({a}, {b}) = {mcm_resultado}")
                
                # Mostrar la relación
                mcd_resultado = mcd_euclidiano(a, b)
                print(f"MCD({a}, {b}) = {mcd_resultado}")
                print(f"Verificación: {a} × {b} = {a * b}")
                print(f"MCD × MCM = {mcd_resultado} × {mcm_resultado} = {mcd_resultado * mcm_resultado}")
            
            elif opcion == 3:
                entrada = input("Ingresa números separados por espacios: ")
                numeros = [int(x) for x in entrada.split()]
                
                if len(numeros) < 2:
                    print("Error: Ingresa al menos 2 números")
                    continue
                
                mcd_resultado = mcd_multiple(*numeros)
                mcm_resultado = mcm_multiple(*numeros)
                
                print(f"\nNúmeros: {numeros}")
                print(f"MCD = {mcd_resultado}")
                print(f"MCM = {mcm_resultado}")
                
                if mcd_resultado == 1:
                    print("Todos los números son coprimos entre sí")
            
            elif opcion == 4:
                a = int(input("Primer número: "))
                b = int(input("Segundo número: "))
                
                print(f"\n=== ANÁLISIS COMPLETO DE {a} Y {b} ===")
                
                # Cálculos básicos
                mcd_resultado = mcd_euclidiano(a, b)
                mcm_resultado = mcm(a, b) if a != 0 and b != 0 else 0
                
                print(f"MCD({a}, {b}) = {mcd_resultado}")
                print(f"MCM({a}, {b}) = {mcm_resultado}")
                
                # Divisores
                divisores_a = encontrar_divisores(a)
                divisores_b = encontrar_divisores(b)
                divisores_comunes = sorted(set(divisores_a) & set(divisores_b))
                
                print(f"\nDivisores de {a}: {divisores_a}")
                print(f"Divisores de {b}: {divisores_b}")
                print(f"Divisores comunes: {divisores_comunes}")
                
                # Relaciones
                if mcd_resultado == 1:
                    print(f"\n{a} y {b} son coprimos")
                else:
                    print(f"\n{a} y {b} comparten el factor {mcd_resultado}")
                
                # Algoritmo de Euclides extendido
                if a != 0 and b != 0:
                    mcd_ext, x, y = algoritmo_euclides_extendido(a, b)
                    print(f"\nEcuación de Bézout: {a} × ({x}) + {b} × ({y}) = {mcd_ext}")
            
            elif opcion == 5:
                a = int(input("Primer número: "))
                b = int(input("Segundo número: "))
                
                print(f"\n=== ALGORITMO DE EUCLIDES PASO A PASO ===")
                print(f"Calculando MCD({a}, {b}):")
                
                original_a, original_b = a, b
                paso = 1
                
                while b != 0:
                    cociente = a // b
                    resto = a % b
                    print(f"Paso {paso}: {a} = {b} × {cociente} + {resto}")
                    a, b = b, resto
                    paso += 1
                
                print(f"\nResultado: MCD({original_a}, {original_b}) = {abs(a)}")
            
            elif opcion == 6:
                a = int(input("Primer número: "))
                b = int(input("Segundo número: "))
                
                divisores_a = encontrar_divisores(a)
                divisores_b = encontrar_divisores(b)
                divisores_comunes = sorted(set(divisores_a) & set(divisores_b))
                
                print(f"\n=== DIVISORES COMUNES DE {a} Y {b} ===")
                print(f"Divisores de {a}: {divisores_a}")
                print(f"Divisores de {b}: {divisores_b}")
                print(f"Divisores comunes: {divisores_comunes}")
                
                if divisores_comunes:
                    print(f"Máximo divisor común: {max(divisores_comunes)}")
                    print(f"Total de divisores comunes: {len(divisores_comunes)}")
                else:
                    print("No hay divisores comunes (además de 1)")
            
            elif opcion == 7:
                print("¡Hasta luego!")
                break
            
            else:
                print("Opción no válida")
                
        except ValueError:
            print("Error: Ingresa números válidos")
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
