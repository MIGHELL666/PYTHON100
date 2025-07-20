"""
Proyecto 8: Verificar si un número es par o impar
"""

def es_par(numero):
    return numero % 2 == 0

def main():
    try:
        numero = int(input("Ingresa un número: "))
        
        if es_par(numero):
            print(f"El número {numero} es PAR")
        else:
            print(f"El número {numero} es IMPAR")
    except ValueError:
        print("Error: Ingresa un número entero válido")

if __name__ == "__main__":
    main()
