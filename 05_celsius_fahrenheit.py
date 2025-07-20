"""
Proyecto 5: Conversor de grados Celsius a Fahrenheit
"""

def celsius_a_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_a_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9

def main():
    print("=== CONVERSOR DE TEMPERATURA ===")
    print("1. Celsius a Fahrenheit")
    print("2. Fahrenheit a Celsius")
    
    try:
        opcion = int(input("Selecciona una opción (1-2): "))
        
        if opcion == 1:
            celsius = float(input("Ingresa la temperatura en Celsius: "))
            fahrenheit = celsius_a_fahrenheit(celsius)
            print(f"{celsius}°C = {fahrenheit:.2f}°F")
        elif opcion == 2:
            fahrenheit = float(input("Ingresa la temperatura en Fahrenheit: "))
            celsius = fahrenheit_a_celsius(fahrenheit)
            print(f"{fahrenheit}°F = {celsius:.2f}°C")
        else:
            print("Opción no válida")
    except ValueError:
        print("Error: Ingresa un número válido")

if __name__ == "__main__":
    main()
