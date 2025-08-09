# Muestra el calendario de un mes y año
import calendar
anio = int(input("Año: "))
mes = int(input("Mes (1-12): "))
print(calendar.month(anio, mes))
