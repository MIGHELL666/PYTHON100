# Calcula edad en años a partir de fecha YYYY-MM-DD
from datetime import date
y,m,d = map(int, input("Fecha de nacimiento (YYYY-MM-DD): ").split("-"))
hoy = date.today()
edad = hoy.year - y - ((hoy.month, hoy.day) < (m, d))
print(edad)
