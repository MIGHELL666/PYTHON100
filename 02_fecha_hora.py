"""
Proyecto 2: Mostrar fecha y hora actual
"""

from datetime import datetime

def main():
    ahora = datetime.now()
    print(f"Fecha actual: {ahora.strftime('%d/%m/%Y')}")
    print(f"Hora actual: {ahora.strftime('%H:%M:%S')}")
    print(f"Fecha y hora completa: {ahora.strftime('%d/%m/%Y %H:%M:%S')}")

if __name__ == "__main__":
    main()
