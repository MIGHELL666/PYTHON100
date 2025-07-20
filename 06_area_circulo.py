"""
Proyecto 6: Calcular el área de un círculo
"""

import math

def calcular_area_circulo(radio):
    return math.pi * radio ** 2

def main():
    try:
        radio = float(input("Ingresa el radio del círculo: "))
        if radio < 0:
            print("Error: El radio no puede ser negativo")
            return
        
        area = calcular_area_circulo(radio)
        print(f"El área del círculo con radio {radio} es: {area:.2f}")
    except ValueError:
        print("Error: Ingresa un número válido")

if __name__ == "__main__":
    main()
