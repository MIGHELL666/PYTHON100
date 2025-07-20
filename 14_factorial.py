"""
Proyecto 14: Calcular factorial de un número
"""

def factorial_iterativo(n):
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado

def factorial_recursivo(n):
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    return n * factorial_recursivo(n - 1)

def main():
    try:
        numero = int(input("Ingresa un número para calcular su factorial: "))
        
        if numero < 0:
            print("Error: El factorial no está definido para números negativos")
            return
        
        # Método iterativo
        fact_iter = factorial_iterativo(numero)
        print(f"Factorial de {numero} (iterativo): {fact_iter}")
        
        # Método recursivo
        fact_rec = factorial_recursivo(numero)
        print(f"Factorial de {numero} (recursivo): {fact_rec}")
        
    except ValueError:
        print("Error: Ingresa un número entero válido")

if __name__ == "__main__":
    main()
