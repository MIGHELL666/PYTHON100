"""
Proyecto 7: Calcular el área de un triángulo
"""

def calcular_area_triangulo(base, altura):
    return (base * altura) / 2

def main():
    try:
        base = float(input("Ingresa la base del triángulo: "))
        altura = float(input("Ingresa la altura del triángulo: "))
        
        if base < 0 or altura < 0:
            print("Error: La base y altura deben ser positivas")
            return
        
        area = calcular_area_triangulo(base, altura)
        print(f"El área del triángulo es: {area:.2f}")
    except ValueError:
        print("Error: Ingresa números válidos")

if __name__ == "__main__":
    main()
