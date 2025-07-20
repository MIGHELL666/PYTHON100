"""
Proyecto 13: Mostrar tabla de multiplicar de un número
"""

def mostrar_tabla_multiplicar(numero, hasta=10):
    print(f"=== TABLA DE MULTIPLICAR DEL {numero} ===")
    for i in range(1, hasta + 1):
        resultado = numero * i
        print(f"{numero} × {i} = {resultado}")

def main():
    try:
        numero = int(input("Ingresa un número para ver su tabla de multiplicar: "))
        hasta = input("¿Hasta qué número? (presiona Enter para 10): ")
        
        if hasta:
            hasta = int(hasta)
        else:
            hasta = 10
            
        mostrar_tabla_multiplicar(numero, hasta)
    except ValueError:
        print("Error: Ingresa números válidos")

if __name__ == "__main__":
    main()
