# Pide una lista de números y muestra promedio, máximo y mínimo
nums = [float(x) for x in input("Números separados por espacios: ").split()]
print(f"promedio: {sum(nums)/len(nums):.2f}, max: {max(nums)}, min: {min(nums)}")
