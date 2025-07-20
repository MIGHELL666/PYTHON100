"""
Proyecto 15: Generar números aleatorios
"""

import random

def generar_numeros_aleatorios():
    print("=== GENERADOR DE NÚMEROS ALEATORIOS ===")
    print("1. Número entero en un rango")
    print("2. Número decimal entre 0 y 1")
    print("3. Lista de números aleatorios")
    print("4. Número de una lista")
    
    try:
        opcion = int(input("Selecciona una opción (1-4): "))
        
        if opcion == 1:
            min_val = int(input("Valor mínimo: "))
            max_val = int(input("Valor máximo: "))
            numero = random.randint(min_val, max_val)
            print(f"Número aleatorio entre {min_val} y {max_val}: {numero}")
            
        elif opcion == 2:
            numero = random.random()
            print(f"Número decimal aleatorio: {numero:.6f}")
            
        elif opcion == 3:
            cantidad = int(input("¿Cuántos números quieres generar? "))
            min_val = int(input("Valor mínimo: "))
            max_val = int(input("Valor máximo: "))
            numeros = [random.randint(min_val, max_val) for _ in range(cantidad)]
            print(f"Lista de {cantidad} números aleatorios: {numeros}")
            
        elif opcion == 4:
            elementos = input("Ingresa elementos separados por comas: ").split(',')
            elementos = [elem.strip() for elem in elementos]
            seleccionado = random.choice(elementos)
            print(f"Elemento seleccionado aleatoriamente: {seleccionado}")
            
        else:
            print("Opción no válida")
            
    except ValueError:
        print("Error: Ingresa valores válidos")

if __name__ == "__main__":
    generar_numeros_aleatorios()
