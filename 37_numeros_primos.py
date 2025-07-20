"""
Proyecto 37: Verificar si un número es primo
"""

def es_primo(numero):
    """Verifica si un número es primo"""
    if numero < 2:
        return False
    if numero == 2:
        return True
    if numero % 2 == 0:
        return False
    
    # Solo verificar divisores impares hasta la raíz cuadrada
    for i in range(3, int(numero**0.5) + 1, 2):
        if numero % i == 0:
            return False
    
    return True

def generar_primos(limite):
    """Genera todos los números primos hasta un límite"""
    primos = []
    for numero in range(2, limite + 1):
        if es_primo(numero):
            primos.append(numero)
    return primos

def criba_eratostenes(limite):
    """Genera primos usando la Criba de Eratóstenes (más eficiente)"""
    if limite < 2:
        return []
    
    # Crear lista de booleanos
    es_primo_lista = [True] * (limite + 1)
    es_primo_lista[0] = es_primo_lista[1] = False
    
    for i in range(2, int(limite**0.5) + 1):
        if es_primo_lista[i]:
            # Marcar múltiplos como no primos
            for j in range(i*i, limite + 1, i):
                es_primo_lista[j] = False
    
    # Recopilar números primos
    primos = [i for i in range(2, limite + 1) if es_primo_lista[i]]
    return primos

def factorizar_primo(numero):
    """Encuentra la factorización prima de un número"""
    if numero < 2:
        return []
    
    factores = []
    divisor = 2
    
    while divisor * divisor <= numero:
        while numero % divisor == 0:
            factores.append(divisor)
            numero //= divisor
        divisor += 1
    
    if numero > 1:
        factores.append(numero)
    
    return factores

def siguiente_primo(numero):
    """Encuentra el siguiente número primo después del dado"""
    candidato = numero + 1
    while not es_primo(candidato):
        candidato += 1
    return candidato

def primo_anterior(numero):
    """Encuentra el número primo anterior al dado"""
    if numero <= 2:
        return None
    
    candidato = numero - 1
    while candidato >= 2 and not es_primo(candidato):
        candidato -= 1
    
    return candidato if candidato >= 2 else None

def main():
    print("=== CALCULADORA DE NÚMEROS PRIMOS ===")
    
    while True:
        print("\n1. Verificar si un número es primo")
        print("2. Generar primos hasta un límite")
        print("3. Generar primos (Criba de Eratóstenes)")
        print("4. Factorización prima")
        print("5. Encontrar primo siguiente/anterior")
        print("6. Análisis de rango de números")
        print("7. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                numero = int(input("Número a verificar: "))
                
                if es_primo(numero):
                    print(f"✅ {numero} ES un número primo")
                    
                    # Información adicional
                    if numero > 2:
                        anterior = primo_anterior(numero)
                        siguiente = siguiente_primo(numero)
                        print(f"Primo anterior: {anterior}")
                        print(f"Primo siguiente: {siguiente}")
                        if anterior:
                            print(f"Distancia al anterior: {numero - anterior}")
                        print(f"Distancia al siguiente: {siguiente - numero}")
                else:
                    print(f"❌ {numero} NO es un número primo")
                    
                    if numero > 1:
                        factores = factorizar_primo(numero)
                        print(f"Factorización prima: {' × '.join(map(str, factores))}")
                        
                        # Mostrar primos cercanos
                        anterior = primo_anterior(numero)
                        siguiente = siguiente_primo(numero)
                        print(f"Primo anterior más cercano: {anterior}")
                        print(f"Primo siguiente más cercano: {siguiente}")
            
            elif opcion == 2:
                limite = int(input("Límite superior: "))
                if limite < 2:
                    print("Error: El límite debe ser al menos 2")
                    continue
                
                print(f"Generando primos hasta {limite}...")
                primos = generar_primos(limite)
                
                print(f"\nSe encontraron {len(primos)} números primos:")
                
                # Mostrar en filas de 10
                for i in range(0, len(primos), 10):
                    fila = primos[i:i+10]
                    print(" ".join(f"{p:4d}" for p in fila))
                
                if primos:
                    print(f"\nPrimo más grande: {primos[-1]}")
                    densidad = len(primos) / limite * 100
                    print(f"Densidad de primos: {densidad:.2f}%")
            
            elif opcion == 3:
                limite = int(input("Límite superior: "))
                if limite < 2:
                    print("Error: El límite debe ser al menos 2")
                    continue
                
                print(f"Generando primos hasta {limite} (Criba de Eratóstenes)...")
                primos = criba_eratostenes(limite)
                
                print(f"\nSe encontraron {len(primos)} números primos:")
                
                # Mostrar primeros y últimos
                if len(primos) <= 50:
                    for i in range(0, len(primos), 10):
                        fila = primos[i:i+10]
                        print(" ".join(f"{p:4d}" for p in fila))
                else:
                    print("Primeros 20:", primos[:20])
                    print("...")
                    print("Últimos 20:", primos[-20:])
                
                if primos:
                    print(f"\nEstadísticas:")
                    print(f"Primo más grande: {primos[-1]}")
                    print(f"Densidad: {len(primos)/limite*100:.2f}%")
            
            elif opcion == 4:
                numero = int(input("Número a factorizar: "))
                if numero < 2:
                    print("Error: Ingresa un número mayor o igual a 2")
                    continue
                
                factores = factorizar_primo(numero)
                
                print(f"\nFactorización prima de {numero}:")
                print(f"{numero} = {' × '.join(map(str, factores))}")
                
                # Contar factores únicos
                from collections import Counter
                contador_factores = Counter(factores)
                
                print(f"\nFactores únicos:")
                for factor, cantidad in sorted(contador_factores.items()):
                    if cantidad == 1:
                        print(f"  {factor}")
                    else:
                        print(f"  {factor}^{cantidad}")
                
                print(f"\nTotal de factores primos: {len(factores)}")
                print(f"Factores únicos: {len(contador_factores)}")
            
            elif opcion == 5:
                numero = int(input("Número de referencia: "))
                
                anterior = primo_anterior(numero)
                siguiente = siguiente_primo(numero)
                
                print(f"\nPara el número {numero}:")
                
                if anterior:
                    print(f"Primo anterior: {anterior} (distancia: {numero - anterior})")
                else:
                    print("No hay primo anterior (número muy pequeño)")
                
                print(f"Primo siguiente: {siguiente} (distancia: {siguiente - numero})")
                
                if es_primo(numero):
                    print(f"Nota: {numero} es primo")
            
            elif opcion == 6:
                inicio = int(input("Número inicial: "))
                fin = int(input("Número final: "))
                
                if inicio > fin:
                    inicio, fin = fin, inicio
                
                print(f"\nAnalizando rango [{inicio}, {fin}]...")
                
                primos_en_rango = []
                compuestos = []
                
                for num in range(max(2, inicio), fin + 1):
                    if es_primo(num):
                        primos_en_rango.append(num)
                    else:
                        compuestos.append(num)
                
                total_numeros = fin - max(2, inicio) + 1
                
                print(f"\nResultados:")
                print(f"Total de números analizados: {total_numeros}")
                print(f"Números primos: {len(primos_en_rango)}")
                print(f"Números compuestos: {len(compuestos)}")
                
                if total_numeros > 0:
                    print(f"Porcentaje de primos: {len(primos_en_rango)/total_numeros*100:.2f}%")
                
                if primos_en_rango:
                    print(f"Primos encontrados: {primos_en_rango}")
            
            elif opcion == 7:
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
