"""
Proyecto 47: Calculadora científica
"""

import math

def operaciones_basicas(a, b, operacion):
    """Realiza operaciones básicas"""
    try:
        if operacion == '+':
            return a + b, f"{a} + {b} = {a + b}"
        elif operacion == '-':
            return a - b, f"{a} - {b} = {a - b}"
        elif operacion == '*':
            return a * b, f"{a} × {b} = {a * b}"
        elif operacion == '/':
            if b == 0:
                return None, "Error: División por cero"
            return a / b, f"{a} ÷ {b} = {a / b}"
        elif operacion == '**' or operacion == '^':
            return a ** b, f"{a}^{b} = {a ** b}"
        elif operacion == '%':
            if b == 0:
                return None, "Error: Módulo por cero"
            return a % b, f"{a} mod {b} = {a % b}"
        else:
            return None, "Operación no válida"
    except OverflowError:
        return None, "Error: Resultado demasiado grande"
    except Exception as e:
        return None, f"Error: {e}"

def funciones_trigonometricas(angulo, unidad='radianes'):
    """Calcula funciones trigonométricas"""
    try:
        # Convertir a radianes si es necesario
        if unidad == 'grados':
            angulo_rad = math.radians(angulo)
            conversion = f"{angulo}° = {angulo_rad:.6f} radianes"
        else:
            angulo_rad = angulo
            conversion = f"{angulo} radianes"
        
        # Calcular funciones
        seno = math.sin(angulo_rad)
        coseno = math.cos(angulo_rad)
        
        # Evitar división por cero para tangente
        if abs(coseno) < 1e-10:
            tangente = "indefinido"
        else:
            tangente = math.tan(angulo_rad)
        
        resultados = {
            'angulo_original': angulo,
            'angulo_radianes': angulo_rad,
            'conversion': conversion,
            'seno': seno,
            'coseno': coseno,
            'tangente': tangente
        }
        
        return resultados, "Cálculo exitoso"
        
    except Exception as e:
        return None, f"Error: {e}"

def funciones_trigonometricas_inversas(valor):
    """Calcula funciones trigonométricas inversas"""
    try:
        resultados = {}
        
        # Arcoseno (dominio: [-1, 1])
        if -1 <= valor <= 1:
            arcsen_rad = math.asin(valor)
            arcsen_grados = math.degrees(arcsen_rad)
            resultados['arcsen'] = {
                'radianes': arcsen_rad,
                'grados': arcsen_grados
            }
        else:
            resultados['arcsen'] = "indefinido (valor fuera del dominio [-1, 1])"
        
        # Arcocoseno (dominio: [-1, 1])
        if -1 <= valor <= 1:
            arccos_rad = math.acos(valor)
            arccos_grados = math.degrees(arccos_rad)
            resultados['arccos'] = {
                'radianes': arccos_rad,
                'grados': arccos_grados
            }
        else:
            resultados['arccos'] = "indefinido (valor fuera del dominio [-1, 1])"
        
        # Arcotangente (dominio: todos los reales)
        arctan_rad = math.atan(valor)
        arctan_grados = math.degrees(arctan_rad)
        resultados['arctan'] = {
            'radianes': arctan_rad,
            'grados': arctan_grados
        }
        
        return resultados, "Cálculo exitoso"
        
    except Exception as e:
        return None, f"Error: {e}"

def funciones_logaritmicas(numero, base=None):
    """Calcula logaritmos en diferentes bases"""
    try:
        if numero <= 0:
            return None, "Error: El logaritmo no está definido para números ≤ 0"
        
        resultados = {
            'numero': numero,
            'ln': math.log(numero),  # Logaritmo natural
            'log10': math.log10(numero),  # Logaritmo base 10
            'log2': math.log2(numero)  # Logaritmo base 2
        }
        
        if base and base > 0 and base != 1:
            resultados[f'log_{base}'] = math.log(numero) / math.log(base)
        
        return resultados, "Cálculo exitoso"
        
    except Exception as e:
        return None, f"Error: {e}"

def funciones_exponenciales(numero):
    """Calcula funciones exponenciales"""
    try:
        resultados = {
            'numero': numero,
            'exp': math.exp(numero),  # e^x
            'exp2': 2 ** numero,  # 2^x
            'exp10': 10 ** numero  # 10^x
        }
        
        return resultados, "Cálculo exitoso"
        
    except OverflowError:
        return None, "Error: Resultado demasiado grande"
    except Exception as e:
        return None, f"Error: {e}"

def funciones_hiperbolicas(numero):
    """Calcula funciones hiperbólicas"""
    try:
        resultados = {
            'numero': numero,
            'sinh': math.sinh(numero),  # Seno hiperbólico
            'cosh': math.cosh(numero),  # Coseno hiperbólico
            'tanh': math.tanh(numero)   # Tangente hiperbólica
        }
        
        return resultados, "Cálculo exitoso"
        
    except Exception as e:
        return None, f"Error: {e}"

def estadisticas_basicas(numeros):
    """Calcula estadísticas básicas de una lista de números"""
    try:
        if not numeros:
            return None, "Error: Lista vacía"
        
        n = len(numeros)
        suma = sum(numeros)
        media = suma / n
        
        # Mediana
        numeros_ordenados = sorted(numeros)
        if n % 2 == 0:
            mediana = (numeros_ordenados[n//2 - 1] + numeros_ordenados[n//2]) / 2
        else:
            mediana = numeros_ordenados[n//2]
        
        # Varianza y desviación estándar
        varianza = sum((x - media) ** 2 for x in numeros) / n
        desviacion_estandar = math.sqrt(varianza)
        
        resultados = {
            'cantidad': n,
            'suma': suma,
            'media': media,
            'mediana': mediana,
            'minimo': min(numeros),
            'maximo': max(numeros),
            'rango': max(numeros) - min(numeros),
            'varianza': varianza,
            'desviacion_estandar': desviacion_estandar
        }
        
        return resultados, "Cálculo exitoso"
        
    except Exception as e:
        return None, f"Error: {e}"

def combinatoria(n, r, tipo='combinacion'):
    """Calcula combinaciones y permutaciones"""
    try:
        if n < 0 or r < 0 or r > n:
            return None, "Error: n y r deben ser no negativos y r ≤ n"
        
        if tipo == 'combinacion':
            # C(n,r) = n! / (r! * (n-r)!)
            resultado = math.comb(n, r)
            formula = f"C({n},{r}) = {n}! / ({r}! × {n-r}!) = {resultado}"
        elif tipo == 'permutacion':
            # P(n,r) = n! / (n-r)!
            resultado = math.perm(n, r)
            formula = f"P({n},{r}) = {n}! / {n-r}! = {resultado}"
        else:
            return None, "Tipo debe ser 'combinacion' o 'permutacion'"
        
        return resultado, formula
        
    except Exception as e:
        return None, f"Error: {e}"

def evaluar_expresion(expresion):
    """Evalúa una expresión matemática de forma segura"""
    try:
        # Reemplazar funciones comunes
        expresion = expresion.replace('^', '**')
        expresion = expresion.replace('π', str(math.pi))
        expresion = expresion.replace('e', str(math.e))
        
        # Funciones permitidas
        funciones_permitidas = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
            'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
            'log': math.log, 'log10': math.log10, 'log2': math.log2,
            'exp': math.exp, 'sqrt': math.sqrt, 'abs': abs,
            'ceil': math.ceil, 'floor': math.floor,
            'pi': math.pi, 'e': math.e
        }
        
        # Evaluar de forma segura
        resultado = eval(expresion, {"__builtins__": {}}, funciones_permitidas)
        
        return resultado, f"{expresion} = {resultado}"
        
    except Exception as e:
        return None, f"Error al evaluar '{expresion}': {e}"

def main():
    print("=== CALCULADORA CIENTÍFICA ===")
    
    while True:
        print("\n1. Operaciones básicas")
        print("2. Funciones trigonométricas")
        print("3. Funciones trigonométricas inversas")
        print("4. Logaritmos")
        print("5. Funciones exponenciales")
        print("6. Funciones hiperbólicas")
        print("7. Estadísticas básicas")
        print("8. Combinatoria")
        print("9. Evaluar expresión")
        print("10. Constantes matemáticas")
        print("11. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                a = float(input("Primer número: "))
                operacion = input("Operación (+, -, *, /, **, %): ")
                b = float(input("Segundo número: "))
                
                resultado, mensaje = operaciones_basicas(a, b, operacion)
                
                if resultado is not None:
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 2:
                angulo = float(input("Ángulo: "))
                unidad = input("Unidad (grados/radianes): ").lower()
                
                if unidad not in ['grados', 'radianes']:
                    unidad = 'radianes'
                
                resultado, mensaje = funciones_trigonometricas(angulo, unidad)
                
                if resultado:
                    print(f"\n=== FUNCIONES TRIGONOMÉTRICAS ===")
                    print(f"Ángulo: {resultado['conversion']}")
                    print(f"sen({angulo}) = {resultado['seno']:.6f}")
                    print(f"cos({angulo}) = {resultado['coseno']:.6f}")
                    print(f"tan({angulo}) = {resultado['tangente']}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 3:
                valor = float(input("Valor (-1 ≤ valor ≤ 1 para arcsen y arccos): "))
                
                resultado, mensaje = funciones_trigonometricas_inversas(valor)
                
                if resultado:
                    print(f"\n=== FUNCIONES TRIGONOMÉTRICAS INVERSAS ===")
                    print(f"Valor: {valor}")
                    
                    for func, res in resultado.items():
                        if isinstance(res, dict):
                            print(f"{func}({valor}) = {res['radianes']:.6f} rad = {res['grados']:.6f}°")
                        else:
                            print(f"{func}({valor}) = {res}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 4:
                numero = float(input("Número (> 0): "))
                base_personalizada = input("Base personalizada (Enter para omitir): ")
                
                base = None
                if base_personalizada:
                    base = float(base_personalizada)
                
                resultado, mensaje = funciones_logaritmicas(numero, base)
                
                if resultado:
                    print(f"\n=== LOGARITMOS DE {numero} ===")
                    print(f"ln({numero}) = {resultado['ln']:.6f}")
                    print(f"log₁₀({numero}) = {resultado['log10']:.6f}")
                    print(f"log₂({numero}) = {resultado['log2']:.6f}")
                    
                    if base:
                        print(f"log_{base}({numero}) = {resultado[f'log_{base}']:.6f}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 5:
                numero = float(input("Exponente: "))
                
                resultado, mensaje = funciones_exponenciales(numero)
                
                if resultado:
                    print(f"\n=== FUNCIONES EXPONENCIALES ===")
                    print(f"e^{numero} = {resultado['exp']:.6f}")
                    print(f"2^{numero} = {resultado['exp2']:.6f}")
                    print(f"10^{numero} = {resultado['exp10']:.6f}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 6:
                numero = float(input("Número: "))
                
                resultado, mensaje = funciones_hiperbolicas(numero)
                
                if resultado:
                    print(f"\n=== FUNCIONES HIPERBÓLICAS ===")
                    print(f"sinh({numero}) = {resultado['sinh']:.6f}")
                    print(f"cosh({numero}) = {resultado['cosh']:.6f}")
                    print(f"tanh({numero}) = {resultado['tanh']:.6f}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 7:
                entrada = input("Números separados por espacios: ")
                try:
                    numeros = [float(x) for x in entrada.split()]
                    
                    resultado, mensaje = estadisticas_basicas(numeros)
                    
                    if resultado:
                        print(f"\n=== ESTADÍSTICAS BÁSICAS ===")
                        print(f"Datos: {numeros}")
                        print(f"Cantidad: {resultado['cantidad']}")
                        print(f"Suma: {resultado['suma']:.6f}")
                        print(f"Media: {resultado['media']:.6f}")
                        print(f"Mediana: {resultado['mediana']:.6f}")
                        print(f"Mínimo: {resultado['minimo']:.6f}")
                        print(f"Máximo: {resultado['maximo']:.6f}")
                        print(f"Rango: {resultado['rango']:.6f}")
                        print(f"Varianza: {resultado['varianza']:.6f}")
                        print(f"Desviación estándar: {resultado['desviacion_estandar']:.6f}")
                    else:
                        print(f"❌ {mensaje}")
                        
                except ValueError:
                    print("❌ Error: Ingresa solo números válidos")
            
            elif opcion == 8:
                n = int(input("n (total de elementos): "))
                r = int(input("r (elementos a seleccionar): "))
                tipo = input("Tipo (combinacion/permutacion): ").lower()
                
                resultado, formula = combinatoria(n, r, tipo)
                
                if resultado is not None:
                    print(f"✅ {formula}")
                else:
                    print(f"❌ {formula}")
            
            elif opcion == 9:
                expresion = input("Expresión matemática: ")
                print("Funciones disponibles: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh")
                print("                      log, log10, log2, exp, sqrt, abs, ceil, floor")
                print("Constantes: π (pi), e")
                print("Operadores: +, -, *, /, ** (potencia), % (módulo)")
                
                resultado, mensaje = evaluar_expresion(expresion)
                
                if resultado is not None:
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 10:
                print(f"\n=== CONSTANTES MATEMÁTICAS ===")
                print(f"π (pi) = {math.pi:.10f}")
                print(f"e = {math.e:.10f}")
                print(f"φ (phi, razón áurea) = {(1 + math.sqrt(5)) / 2:.10f}")
                print(f"√2 = {math.sqrt(2):.10f}")
                print(f"√3 = {math.sqrt(3):.10f}")
                print(f"ln(2) = {math.log(2):.10f}")
                print(f"ln(10) = {math.log(10):.10f}")
            
            elif opcion == 11:
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
