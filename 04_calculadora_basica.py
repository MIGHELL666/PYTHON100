"""
Proyecto 4: Calculadora básica (suma, resta, multiplicación, división)
"""

def calculadora():
    print("=== CALCULADORA BÁSICA ===")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. División")
    
    try:
        opcion = int(input("Selecciona una opción (1-4): "))
        num1 = float(input("Primer número: "))
        num2 = float(input("Segundo número: "))
        
        if opcion == 1:
            resultado = num1 + num2
            print(f"{num1} + {num2} = {resultado}")
        elif opcion == 2:
            resultado = num1 - num2
            print(f"{num1} - {num2} = {resultado}")
        elif opcion == 3:
            resultado = num1 * num2
            print(f"{num1} × {num2} = {resultado}")
        elif opcion == 4:
            if num2 != 0:
                resultado = num1 / num2
                print(f"{num1} ÷ {num2} = {resultado}")
            else:
                print("Error: No se puede dividir por cero")
        else:
            print("Opción no válida")
    except ValueError:
        print("Error: Ingresa valores numéricos válidos")

if __name__ == "__main__":
    calculadora()
