"""
Proyecto 9: Verificar si un año es bisiesto
"""

def es_bisiesto(año):
    return (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)

def main():
    try:
        año = int(input("Ingresa un año: "))
        
        if es_bisiesto(año):
            print(f"El año {año} ES bisiesto")
        else:
            print(f"El año {año} NO es bisiesto")
    except ValueError:
        print("Error: Ingresa un año válido")

if __name__ == "__main__":
    main()
