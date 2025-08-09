# Convierte bytes a KB, MB, GB y viceversa
modo = input("b->otras o otras->b: ").strip().lower()
valor = float(input("Valor: "))
if modo == "b->otras":
    print(f"KB: {valor/1024:.2f}")
    print(f"MB: {valor/1024**2:.2f}")
    print(f"GB: {valor/1024**3:.2f}")
elif modo == "otras->b":
    unidad = input("Unidad (KB/MB/GB): ").strip().upper()
    factor = {"KB":1024, "MB":1024**2, "GB":1024**3}.get(unidad)
    if factor:
        print(f"{valor*factor} bytes")
    else:
        print("Unidad no válida")
else:
    print("Modo no reconocido")
