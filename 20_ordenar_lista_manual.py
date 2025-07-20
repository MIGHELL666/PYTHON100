"""
Proyecto 20: Ordenar una lista sin usar sorted()
"""

def burbuja(lista):
    """Algoritmo de ordenamiento burbuja"""
    n = len(lista)
    lista_copia = lista.copy()
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_copia[j] > lista_copia[j + 1]:
                lista_copia[j], lista_copia[j + 1] = lista_copia[j + 1], lista_copia[j]
    
    return lista_copia

def seleccion(lista):
    """Algoritmo de ordenamiento por selección"""
    lista_copia = lista.copy()
    n = len(lista_copia)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if lista_copia[j] < lista_copia[min_idx]:
                min_idx = j
        lista_copia[i], lista_copia[min_idx] = lista_copia[min_idx], lista_copia[i]
    
    return lista_copia

def insercion(lista):
    """Algoritmo de ordenamiento por inserción"""
    lista_copia = lista.copy()
    
    for i in range(1, len(lista_copia)):
        clave = lista_copia[i]
        j = i - 1
        
        while j >= 0 and lista_copia[j] > clave:
            lista_copia[j + 1] = lista_copia[j]
            j -= 1
        
        lista_copia[j + 1] = clave
    
    return lista_copia

def main():
    print("=== ORDENAR LISTA SIN SORTED() ===")
    
    # Obtener lista del usuario
    entrada = input("Ingresa números separados por comas: ")
    try:
        lista = [float(x.strip()) for x in entrada.split(',')]
    except ValueError:
        print("Error: Ingresa números válidos")
        return
    
    print(f"Lista original: {lista}")
    
    # Mostrar diferentes algoritmos
    print("\nAlgoritmos de ordenamiento:")
    
    lista_burbuja = burbuja(lista)
    print(f"Burbuja: {lista_burbuja}")
    
    lista_seleccion = seleccion(lista)
    print(f"Selección: {lista_seleccion}")
    
    lista_insercion = insercion(lista)
    print(f"Inserción: {lista_insercion}")

if __name__ == "__main__":
    main()
