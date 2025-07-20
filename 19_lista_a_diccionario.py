"""
Proyecto 19: Convertir una lista en un diccionario
"""

def lista_a_diccionario_indices(lista):
    """Convierte lista usando índices como claves"""
    return {i: valor for i, valor in enumerate(lista)}

def lista_a_diccionario_pares(lista):
    """Convierte lista de pares en diccionario"""
    diccionario = {}
    for i in range(0, len(lista), 2):
        if i + 1 < len(lista):
            diccionario[lista[i]] = lista[i + 1]
        else:
            diccionario[lista[i]] = None
    return diccionario

def lista_a_diccionario_contador(lista):
    """Cuenta frecuencia de elementos"""
    diccionario = {}
    for elemento in lista:
        diccionario[elemento] = diccionario.get(elemento, 0) + 1
    return diccionario

def main():
    print("=== CONVERTIR LISTA A DICCIONARIO ===")
    print("1. Lista con índices como claves")
    print("2. Lista de pares (clave, valor)")
    print("3. Contador de frecuencias")
    
    try:
        opcion = int(input("Selecciona una opción (1-3): "))
        elementos = input("Ingresa elementos separados por comas: ").split(',')
        elementos = [elem.strip() for elem in elementos]
        
        if opcion == 1:
            resultado = lista_a_diccionario_indices(elementos)
            print(f"Lista original: {elementos}")
            print(f"Diccionario con índices: {resultado}")
            
        elif opcion == 2:
            resultado = lista_a_diccionario_pares(elementos)
            print(f"Lista original: {elementos}")
            print(f"Diccionario de pares: {resultado}")
            
        elif opcion == 3:
            resultado = lista_a_diccionario_contador(elementos)
            print(f"Lista original: {elementos}")
            print(f"Contador de frecuencias: {resultado}")
            
        else:
            print("Opción no válida")
            
    except ValueError:
        print("Error: Ingresa una opción válida")

if __name__ == "__main__":
    main()
