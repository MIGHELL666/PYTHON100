# Convierte segundos a HH:MM:SS
s = int(input("Segundos: "))
h = s // 3600
m = (s % 3600) // 60
sec = s % 60
print(f"{h:02d}:{m:02d}:{sec:02d}")
