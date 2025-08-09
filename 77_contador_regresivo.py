# Cuenta regresiva simple en segundos
import time
n = int(input("Segundos para la cuenta regresiva: "))
for i in range(n, -1, -1):
    print(i)
    time.sleep(1)
print("¡Tiempo!")
