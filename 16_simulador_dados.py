"""
Proyecto 16: Simulador de dados
"""

import random

def lanzar_dado(caras=6):
    return random.randint(1, caras)

def simulador_dados():
    print("=== SIMULADOR DE DADOS ===")
    
    try:
        num_dados = int(input("¿Cuántos dados quieres lanzar? "))
        caras = int(input("¿Cuántas caras tiene cada dado? (6 por defecto): ") or "6")
        
        if num_dados <= 0 or caras <= 0:
            print("Error: Los valores deben ser positivos")
            return
        
        print(f"\nLanzando {num_dados} dado(s) de {caras} caras...")
        
        resultados = []
        for i in range(num_dados):
            resultado = lanzar_dado(caras)
            resultados.append(resultado)
            print(f"Dado {i+1}: {resultado}")
        
        print(f"\nResultados: {resultados}")
        print(f"Suma total: {sum(resultados)}")
        print(f"Promedio: {sum(resultados)/len(resultados):.2f}")
        
    except ValueError:
        print("Error: Ingresa números válidos")

if __name__ == "__main__":
    simulador_dados()
