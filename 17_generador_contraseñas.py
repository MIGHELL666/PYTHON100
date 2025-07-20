"""
Proyecto 17: Generador de contraseñas simples
"""

import random
import string

def generar_contraseña(longitud=8, incluir_mayusculas=True, incluir_numeros=True, incluir_simbolos=False):
    caracteres = string.ascii_lowercase
    
    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += "!@#$%^&*"
    
    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña

def main():
    print("=== GENERADOR DE CONTRASEÑAS ===")
    
    try:
        longitud = int(input("Longitud de la contraseña (8 por defecto): ") or "8")
        
        print("Opciones (s/n):")
        mayusculas = input("¿Incluir mayúsculas? (s): ").lower() != 'n'
        numeros = input("¿Incluir números? (s): ").lower() != 'n'
        simbolos = input("¿Incluir símbolos? (n): ").lower() == 's'
        
        cantidad = int(input("¿Cuántas contraseñas generar? (1): ") or "1")
        
        print(f"\nGenerando {cantidad} contraseña(s) de {longitud} caracteres:")
        
        for i in range(cantidad):
            contraseña = generar_contraseña(longitud, mayusculas, numeros, simbolos)
            print(f"Contraseña {i+1}: {contraseña}")
            
    except ValueError:
        print("Error: Ingresa valores válidos")

if __name__ == "__main__":
    main()
