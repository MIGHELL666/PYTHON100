# Calcula la propina y el total a pagar
monto = float(input("Monto de la cuenta: "))
porc = float(input("Porcentaje de propina (ej. 10, 15): "))
propina = monto * (porc/100)
total = monto + propina
print(f"Propina: ${propina:.2f}")
print(f"Total: ${total:.2f}")
