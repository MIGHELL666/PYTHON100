"""
Proyecto 46: Conversión entre bases numéricas
"""

def decimal_a_binario(numero):
    """Convierte un número decimal a binario"""
    if numero == 0:
        return "0", ["0 en binario es 0"]
    
    if numero < 0:
        return f"-{decimal_a_binario(-numero)[0]}", [f"Número negativo: -{-numero} → -{decimal_a_binario(-numero)[0]}"]
    
    binario = ""
    pasos = []
    original = numero
    
    while numero > 0:
        resto = numero % 2
        cociente = numero // 2
        binario = str(resto) + binario
        pasos.append(f"{numero} ÷ 2 = {cociente} resto {resto}")
        numero = cociente
    
    pasos.append(f"Leyendo restos de abajo hacia arriba: {binario}")
    pasos.insert(0, f"Convirtiendo {original} a binario:")
    
    return binario, pasos

def binario_a_decimal(binario):
    """Convierte un número binario a decimal"""
    if not all(bit in '01' for bit in binario):
        return None, ["Error: El número binario solo puede contener 0s y 1s"]
    
    decimal = 0
    pasos = [f"Convirtiendo {binario} a decimal:"]
    
    for i, bit in enumerate(reversed(binario)):
        if bit == '1':
            valor = 2 ** i
            decimal += valor
            pasos.append(f"Posición {i}: {bit} × 2^{i} = {valor}")
        else:
            pasos.append(f"Posición {i}: {bit} × 2^{i} = 0")
    
    pasos.append(f"Suma total: {decimal}")
    
    return decimal, pasos

def decimal_a_octal(numero):
    """Convierte un número decimal a octal"""
    if numero == 0:
        return "0", ["0 en octal es 0"]
    
    if numero < 0:
        return f"-{decimal_a_octal(-numero)[0]}", [f"Número negativo: -{-numero} → -{decimal_a_octal(-numero)[0]}"]
    
    octal = ""
    pasos = []
    original = numero
    
    while numero > 0:
        resto = numero % 8
        cociente = numero // 8
        octal = str(resto) + octal
        pasos.append(f"{numero} ÷ 8 = {cociente} resto {resto}")
        numero = cociente
    
    pasos.append(f"Leyendo restos de abajo hacia arriba: {octal}")
    pasos.insert(0, f"Convirtiendo {original} a octal:")
    
    return octal, pasos

def octal_a_decimal(octal):
    """Convierte un número octal a decimal"""
    if not all(digito in '01234567' for digito in octal):
        return None, ["Error: El número octal solo puede contener dígitos 0-7"]
    
    decimal = 0
    pasos = [f"Convirtiendo {octal} a decimal:"]
    
    for i, digito in enumerate(reversed(octal)):
        valor = int(digito) * (8 ** i)
        decimal += valor
        pasos.append(f"Posición {i}: {digito} × 8^{i} = {valor}")
    
    pasos.append(f"Suma total: {decimal}")
    
    return decimal, pasos

def decimal_a_hexadecimal(numero):
    """Convierte un número decimal a hexadecimal"""
    if numero == 0:
        return "0", ["0 en hexadecimal es 0"]
    
    if numero < 0:
        return f"-{decimal_a_hexadecimal(-numero)[0]}", [f"Número negativo: -{-numero} → -{decimal_a_hexadecimal(-numero)[0]}"]
    
    hex_digits = "0123456789ABCDEF"
    hexadecimal = ""
    pasos = []
    original = numero
    
    while numero > 0:
        resto = numero % 16
        cociente = numero // 16
        hex_char = hex_digits[resto]
        hexadecimal = hex_char + hexadecimal
        pasos.append(f"{numero} ÷ 16 = {cociente} resto {resto} ({hex_char})")
        numero = cociente
    
    pasos.append(f"Leyendo restos de abajo hacia arriba: {hexadecimal}")
    pasos.insert(0, f"Convirtiendo {original} a hexadecimal:")
    
    return hexadecimal, pasos

def hexadecimal_a_decimal(hexadecimal):
    """Convierte un número hexadecimal a decimal"""
    hex_digits = "0123456789ABCDEF"
    hexadecimal = hexadecimal.upper()
    
    if not all(digito in hex_digits for digito in hexadecimal):
        return None, ["Error: El número hexadecimal solo puede contener dígitos 0-9 y letras A-F"]
    
    decimal = 0
    pasos = [f"Convirtiendo {hexadecimal} a decimal:"]
    
    for i, digito in enumerate(reversed(hexadecimal)):
        valor_digito = hex_digits.index(digito)
        valor = valor_digito * (16 ** i)
        decimal += valor
        pasos.append(f"Posición {i}: {digito} ({valor_digito}) × 16^{i} = {valor}")
    
    pasos.append(f"Suma total: {decimal}")
    
    return decimal, pasos

def conversion_directa(numero, base_origen, base_destino):
    """Convierte directamente entre cualquier par de bases"""
    # Primero convertir a decimal
    if base_origen == 10:
        decimal = numero
    elif base_origen == 2:
        decimal, _ = binario_a_decimal(str(numero))
    elif base_origen == 8:
        decimal, _ = octal_a_decimal(str(numero))
    elif base_origen == 16:
        decimal, _ = hexadecimal_a_decimal(str(numero))
    else:
        return None, "Base de origen no soportada"
    
    if decimal is None:
        return None, "Error en conversión a decimal"
    
    # Luego convertir de decimal a base destino
    if base_destino == 10:
        return decimal, f"{numero} (base {base_origen}) = {decimal} (base 10)"
    elif base_destino == 2:
        resultado, _ = decimal_a_binario(decimal)
        return resultado, f"{numero} (base {base_origen}) = {resultado} (base 2)"
    elif base_destino == 8:
        resultado, _ = decimal_a_octal(decimal)
        return resultado, f"{numero} (base {base_origen}) = {resultado} (base 8)"
    elif base_destino == 16:
        resultado, _ = decimal_a_hexadecimal(decimal)
        return resultado, f"{numero} (base {base_origen}) = {resultado} (base 16)"
    else:
        return None, "Base de destino no soportada"

def tabla_conversiones(numero_decimal):
    """Genera una tabla con el número en todas las bases"""
    binario, _ = decimal_a_binario(numero_decimal)
    octal, _ = decimal_a_octal(numero_decimal)
    hexadecimal, _ = decimal_a_hexadecimal(numero_decimal)
    
    tabla = {
        'decimal': numero_decimal,
        'binario': binario,
        'octal': octal,
        'hexadecimal': hexadecimal
    }
    
    return tabla

def operaciones_binarias(bin1, bin2, operacion):
    """Realiza operaciones básicas en binario"""
    # Convertir a decimal
    dec1, _ = binario_a_decimal(bin1)
    dec2, _ = binario_a_decimal(bin2)
    
    if dec1 is None or dec2 is None:
        return None, "Error: Números binarios inválidos"
    
    # Realizar operación
    if operacion == '+':
        resultado_dec = dec1 + dec2
        simbolo = "+"
    elif operacion == '-':
        resultado_dec = dec1 - dec2
        simbolo = "-"
    elif operacion == '*':
        resultado_dec = dec1 * dec2
        simbolo = "×"
    elif operacion == '/':
        if dec2 == 0:
            return None, "Error: División por cero"
        resultado_dec = dec1 // dec2  # División entera
        simbolo = "÷"
    else:
        return None, "Operación no válida"
    
    # Convertir resultado a binario
    if resultado_dec < 0:
        resultado_bin = f"-{decimal_a_binario(-resultado_dec)[0]}"
    else:
        resultado_bin, _ = decimal_a_binario(resultado_dec)
    
    explicacion = [
        f"Operación: {bin1} {simbolo} {bin2}",
        f"En decimal: {dec1} {simbolo} {dec2} = {resultado_dec}",
        f"En binario: {resultado_bin}"
    ]
    
    return resultado_bin, explicacion

def main():
    print("=== CONVERSOR DE BASES NUMÉRICAS ===")
    
    while True:
        print("\n1. Decimal a Binario")
        print("2. Binario a Decimal")
        print("3. Decimal a Octal")
        print("4. Octal a Decimal")
        print("5. Decimal a Hexadecimal")
        print("6. Hexadecimal a Decimal")
        print("7. Conversión entre cualquier base")
        print("8. Tabla de conversiones")
        print("9. Operaciones en binario")
        print("10. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                numero = int(input("Número decimal: "))
                resultado, pasos = decimal_a_binario(numero)
                
                print(f"\n=== CONVERSIÓN DECIMAL A BINARIO ===")
                for paso in pasos:
                    print(paso)
                print(f"\nResultado: {numero} (decimal) = {resultado} (binario)")
            
            elif opcion == 2:
                binario = input("Número binario: ")
                resultado, pasos = binario_a_decimal(binario)
                
                if resultado is not None:
                    print(f"\n=== CONVERSIÓN BINARIO A DECIMAL ===")
                    for paso in pasos:
                        print(paso)
                    print(f"\nResultado: {binario} (binario) = {resultado} (decimal)")
                else:
                    print(f"❌ {pasos[0]}")
            
            elif opcion == 3:
                numero = int(input("Número decimal: "))
                resultado, pasos = decimal_a_octal(numero)
                
                print(f"\n=== CONVERSIÓN DECIMAL A OCTAL ===")
                for paso in pasos:
                    print(paso)
                print(f"\nResultado: {numero} (decimal) = {resultado} (octal)")
            
            elif opcion == 4:
                octal = input("Número octal: ")
                resultado, pasos = octal_a_decimal(octal)
                
                if resultado is not None:
                    print(f"\n=== CONVERSIÓN OCTAL A DECIMAL ===")
                    for paso in pasos:
                        print(paso)
                    print(f"\nResultado: {octal} (octal) = {resultado} (decimal)")
                else:
                    print(f"❌ {pasos[0]}")
            
            elif opcion == 5:
                numero = int(input("Número decimal: "))
                resultado, pasos = decimal_a_hexadecimal(numero)
                
                print(f"\n=== CONVERSIÓN DECIMAL A HEXADECIMAL ===")
                for paso in pasos:
                    print(paso)
                print(f"\nResultado: {numero} (decimal) = {resultado} (hexadecimal)")
            
            elif opcion == 6:
                hexadecimal = input("Número hexadecimal: ")
                resultado, pasos = hexadecimal_a_decimal(hexadecimal)
                
                if resultado is not None:
                    print(f"\n=== CONVERSIÓN HEXADECIMAL A DECIMAL ===")
                    for paso in pasos:
                        print(paso)
                    print(f"\nResultado: {hexadecimal} (hexadecimal) = {resultado} (decimal)")
                else:
                    print(f"❌ {pasos[0]}")
            
            elif opcion == 7:
                numero = input("Número a convertir: ")
                base_origen = int(input("Base de origen (2, 8, 10, 16): "))
                base_destino = int(input("Base de destino (2, 8, 10, 16): "))
                
                if base_origen not in [2, 8, 10, 16] or base_destino not in [2, 8, 10, 16]:
                    print("❌ Bases soportadas: 2, 8, 10, 16")
                    continue
                
                # Convertir número según su base
                if base_origen == 10:
                    numero_input = int(numero)
                else:
                    numero_input = numero
                
                resultado, mensaje = conversion_directa(numero_input, base_origen, base_destino)
                
                if resultado is not None:
                    print(f"\n✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 8:
                numero = int(input("Número decimal para tabla de conversiones: "))
                tabla = tabla_conversiones(numero)
                
                print(f"\n=== TABLA DE CONVERSIONES PARA {numero} ===")
                print(f"Decimal:      {tabla['decimal']}")
                print(f"Binario:      {tabla['binario']}")
                print(f"Octal:        {tabla['octal']}")
                print(f"Hexadecimal:  {tabla['hexadecimal']}")
                
                # Mostrar también algunos números cercanos
                print(f"\nNúmeros cercanos:")
                for i in range(max(0, numero-2), numero+3):
                    if i != numero:
                        tabla_i = tabla_conversiones(i)
                        print(f"{i:3d}: bin={tabla_i['binario']:>8} oct={tabla_i['octal']:>3} hex={tabla_i['hexadecimal']:>3}")
            
            elif opcion == 9:
                print("Operaciones en binario")
                bin1 = input("Primer número binario: ")
                operacion = input("Operación (+, -, *, /): ")
                bin2 = input("Segundo número binario: ")
                
                resultado, explicacion = operaciones_binarias(bin1, bin2, operacion)
                
                if resultado is not None:
                    print(f"\n=== OPERACIÓN BINARIA ===")
                    for linea in explicacion:
                        print(linea)
                else:
                    print(f"❌ {explicacion}")
            
            elif opcion == 10:
                print("¡Hasta luego!")
                break
            
            else:
                print("Opción no válida")
                
        except ValueError:
            print("Error: Ingresa un número válido")
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
