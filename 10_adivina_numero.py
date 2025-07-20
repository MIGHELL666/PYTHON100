"""
Proyecto 10: Adivina el número (juego)
"""

import random

def juego_adivinar():
    numero_secreto = random.randint(1, 100)
    intentos = 0
    max_intentos = 7
    
    print("=== JUEGO: ADIVINA EL NÚMERO ===")
    print("He pensado un número entre 1 y 100")
    print(f"Tienes {max_intentos} intentos para adivinarlo")
    
    while intentos < max_intentos:
        try:
            intento = int(input(f"Intento {intentos + 1}: "))
            intentos += 1
            
            if intento == numero_secreto:
                print(f"¡FELICIDADES! Adivinaste el número {numero_secreto} en {intentos} intentos")
                return
            elif intento < numero_secreto:
                print("El número es MAYOR")
            else:
                print("El número es MENOR")
                
        except ValueError:
            print("Error: Ingresa un número válido")
            continue
    
    print(f"Se acabaron los intentos. El número era: {numero_secreto}")

if __name__ == "__main__":
    juego_adivinar()
