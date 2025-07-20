"""
Proyecto 3: Sumar dos números ingresados por el usuario
"""

def main():
    try:
        num1 = float(input("Ingresa el primer número: "))
        num2 = float(input("Ingresa el segundo número: "))
        suma = num1 + num2
        print(f"La suma de {num1} + {num2} = {suma}")
    except ValueError:
        print("Error: Por favor ingresa números válidos")

if __name__ == "__main__":
    main()
