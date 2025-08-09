# Simula N lanzamientos de moneda y muestra porcentajes
import random
n = int(input("Número de lanzamientos: "))
cara = sum(1 for _ in range(n) if random.random() < 0.5)
cruz = n - cara
print(f"cara: {cara} ({cara/n*100:.2f}%)")
print(f"cruz: {cruz} ({cruz/n*100:.2f}%)")
