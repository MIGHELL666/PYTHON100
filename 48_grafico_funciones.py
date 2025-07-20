"""
Proyecto 48: Graficar funciones matemáticas (usando caracteres ASCII)
"""

import math

def evaluar_funcion(x, funcion):
    """Evalúa una función matemática en un punto x"""
    try:
        # Reemplazar variables y constantes
        expresion = funcion.replace('x', str(x))
        expresion = expresion.replace('π', str(math.pi))
        expresion = expresion.replace('e', str(math.e))
        expresion = expresion.replace('^', '**')
        
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
        
        resultado = eval(expresion, {"__builtins__": {}}, funciones_permitidas)
        return resultado
        
    except:
        return None

def graficar_funcion_ascii(funcion, x_min=-10, x_max=10, y_min=-10, y_max=10, ancho=80, alto=25):
    """Genera un gráfico ASCII de una función"""
    
    # Crear matriz para el gráfico
    grafico = [[' ' for _ in range(ancho)] for _ in range(alto)]
    
    # Calcular escalas
    escala_x = (x_max - x_min) / ancho
    escala_y = (y_max - y_min) / alto
    
    # Dibujar ejes
    # Eje X (y = 0)
    y_cero = int((0 - y_min) / escala_y)
    if 0 <= y_cero < alto:
        for i in range(ancho):
            grafico[alto - 1 - y_cero][i] = '-'
    
    # Eje Y (x = 0)
    x_cero = int((0 - x_min) / escala_x)
    if 0 <= x_cero < ancho:
        for i in range(alto):
            grafico[i][x_cero] = '|'
    
    # Origen
    if 0 <= x_cero < ancho and 0 <= y_cero < alto:
        grafico[alto - 1 - y_cero][x_cero] = '+'
    
    # Evaluar función y dibujar puntos
    puntos_validos = []
    
    for i in range(ancho):
        x = x_min + i * escala_x
        y = evaluar_funcion(x, funcion)
        
        if y is not None and not math.isnan(y) and not math.isinf(y):
            # Convertir a coordenadas de pantalla
            j = int((y - y_min) / escala_y)
            
            if 0 <= j < alto:
                grafico[alto - 1 - j][i] = '*'
                puntos_validos.append((x, y))
    
    return grafico, puntos_validos

def mostrar_grafico(grafico, funcion, x_min, x_max, y_min, y_max):
    """Muestra el gráfico ASCII con etiquetas"""
    print(f"\nGráfico de: f(x) = {funcion}")
    print(f"Dominio: [{x_min}, {x_max}], Rango mostrado: [{y_min}, {y_max}]")
    print("=" * len(grafico[0]))
    
    # Mostrar gráfico
    for i, fila in enumerate(grafico):
        # Etiqueta del eje Y
        if i == 0:
            y_label = f"{y_max:6.1f}"
        elif i == len(grafico) - 1:
            y_label = f"{y_min:6.1f}"
        elif i == len(grafico) // 2:
            y_label = f"{(y_max + y_min) / 2:6.1f}"
        else:
            y_label = "      "
        
        print(f"{y_label} |{''.join(fila)}|")
    
    # Etiquetas del eje X
    print("       " + "+" + "-" * (len(grafico[0]) - 2) + "+")
    print(f"      {x_min:6.1f}" + " " * (len(grafico[0]) - 14) + f"{x_max:6.1f}")

def analizar_funcion(funcion, x_min=-10, x_max=10, paso=0.1):
    """Analiza propiedades de una función"""
    puntos = []
    x = x_min
    
    while x <= x_max:
        y = evaluar_funcion(x, funcion)
        if y is not None and not math.isnan(y) and not math.isinf(y):
            puntos.append((x, y))
        x += paso
    
    if not puntos:
        return None, "No se pudieron evaluar puntos válidos"
    
    # Análisis básico
    valores_y = [y for x, y in puntos]
    
    analisis = {
        'puntos_evaluados': len(puntos),
        'minimo_y': min(valores_y),
        'maximo_y': max(valores_y),
        'rango_y': max(valores_y) - min(valores_y),
        'promedio_y': sum(valores_y) / len(valores_y)
    }
    
    # Buscar ceros aproximados (cambios de signo)
    ceros_aprox = []
    for i in range(len(puntos) - 1):
        y1 = puntos[i][1]
        y2 = puntos[i + 1][1]
        if y1 * y2 < 0:  # Cambio de signo
            x_cero = (puntos[i][0] + puntos[i + 1][0]) / 2
            ceros_aprox.append(x_cero)
    
    analisis['ceros_aproximados'] = ceros_aprox
    
    return analisis, "Análisis completado"

def funciones_predefinidas():
    """Devuelve un diccionario de funciones predefinidas"""
    return {
        '1': ('x', 'Función lineal'),
        '2': ('x**2', 'Parábola'),
        '3': ('x**3', 'Función cúbica'),
        '4': ('sin(x)', 'Función seno'),
        '5': ('cos(x)', 'Función coseno'),
        '6': ('tan(x)', 'Función tangente'),
        '7': ('exp(x)', 'Función exponencial'),
        '8': ('log(x)', 'Logaritmo natural'),
        '9': ('sqrt(abs(x))', 'Raíz cuadrada'),
        '10': ('1/x', 'Función recíproca'),
        '11': ('abs(x)', 'Valor absoluto'),
        '12': ('x**2 - 4', 'Parábola desplazada')
    }

def graficar_multiples_funciones(funciones, x_min=-10, x_max=10, y_min=-10, y_max=10, ancho=80, alto=25):
    """Grafica múltiples funciones en el mismo gráfico"""
    
    # Crear matriz para el gráfico
    grafico = [[' ' for _ in range(ancho)] for _ in range(alto)]
    
    # Calcular escalas
    escala_x = (x_max - x_min) / ancho
    escala_y = (y_max - y_min) / alto
    
    # Dibujar ejes
    y_cero = int((0 - y_min) / escala_y)
    if 0 <= y_cero < alto:
        for i in range(ancho):
            grafico[alto - 1 - y_cero][i] = '-'
    
    # Eje Y (x = 0)
    x_cero = int((0 - x_min) / escala_x)
    if 0 <= x_cero < ancho:
        for i in range(alto):
            grafico[i][x_cero] = '|'
    
    # Origen
    if 0 <= x_cero < ancho and 0 <= y_cero < alto:
        grafico[alto - 1 - y_cero][x_cero] = '+'
    
    # Símbolos para diferentes funciones
    simbolos = ['*', '#', '@', '%', '&', '$', '+', 'o']
    
    # Evaluar cada función
    for idx, funcion in enumerate(funciones):
        simbolo = simbolos[idx % len(simbolos)]
        
        for i in range(ancho):
            x = x_min + i * escala_x
            y = evaluar_funcion(x, funcion)
            
            if y is not None and not math.isnan(y) and not math.isinf(y):
                j = int((y - y_min) / escala_y)
                
                if 0 <= j < alto:
                    # Si ya hay algo en esa posición, usar un símbolo especial
                    if grafico[alto - 1 - j][i] not in [' ', '-', '|']:
                        grafico[alto - 1 - j][i] = 'X'  # Intersección
                    else:
                        grafico[alto - 1 - j][i] = simbolo
    
    return grafico

def main():
    print("=== GRAFICADOR DE FUNCIONES MATEMÁTICAS (ASCII) ===")
    
    while True:
        print("\n1. Graficar función personalizada")
        print("2. Graficar función predefinida")
        print("3. Graficar múltiples funciones")
        print("4. Analizar función")
        print("5. Configurar rango de graficación")
        print("6. Ayuda sobre sintaxis")
        print("7. Salir")
        
        # Configuración por defecto
        x_min, x_max = -10, 10
        y_min, y_max = -10, 10
        ancho, alto = 80, 25
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                funcion = input("Ingresa la función f(x) = ")
                print("Ejemplo: x**2, sin(x), exp(x), log(x), sqrt(x), etc.")
                
                # Probar la función con un valor
                test = evaluar_funcion(0, funcion)
                if test is None:
                    print("❌ Error: No se pudo evaluar la función. Verifica la sintaxis.")
                    continue
                
                grafico, puntos = graficar_funcion_ascii(funcion, x_min, x_max, y_min, y_max, ancho, alto)
                mostrar_grafico(grafico, funcion, x_min, x_max, y_min, y_max)
                
                print(f"\nPuntos válidos evaluados: {len(puntos)}")
                if puntos:
                    print(f"Rango de valores Y: [{min(y for x, y in puntos):.2f}, {max(y for x, y in puntos):.2f}]")
            
            elif opcion == 2:
                funciones_pred = funciones_predefinidas()
                
                print("\nFunciones predefinidas:")
                for key, (func, desc) in funciones_pred.items():
                    print(f"{key:2}. {desc}: f(x) = {func}")
                
                seleccion = input("Selecciona una función (1-12): ")
                
                if seleccion in funciones_pred:
                    funcion, descripcion = funciones_pred[seleccion]
                    
                    grafico, puntos = graficar_funcion_ascii(funcion, x_min, x_max, y_min, y_max, ancho, alto)
                    mostrar_grafico(grafico, funcion, x_min, x_max, y_min, y_max)
                    
                    print(f"\nDescripción: {descripcion}")
                    print(f"Puntos válidos evaluados: {len(puntos)}")
                else:
                    print("❌ Selección no válida")
            
            elif opcion == 3:
                print("Ingresa las funciones a graficar (una por línea, línea vacía para terminar):")
                funciones = []
                
                while True:
                    funcion = input(f"Función {len(funciones) + 1}: ").strip()
                    if not funcion:
                        break
                    
                    # Probar la función
                    test = evaluar_funcion(0, funcion)
                    if test is None:
                        print("❌ Error en la función. Inténtalo de nuevo.")
                        continue
                    
                    funciones.append(funcion)
                
                if not funciones:
                    print("❌ No se ingresaron funciones válidas")
                    continue
                
                grafico = graficar_multiples_funciones(funciones, x_min, x_max, y_min, y_max, ancho, alto)
                
                print(f"\nGráfico de múltiples funciones:")
                print(f"Dominio: [{x_min}, {x_max}], Rango mostrado: [{y_min}, {y_max}]")
                print("=" * ancho)
                
                for fila in grafico:
                    print(f"|{''.join(fila)}|")
                
                print("=" * ancho)
                print("\nLeyenda:")
                simbolos = ['*', '#', '@', '%', '&', '$', '+', 'o']
                for i, funcion in enumerate(funciones):
                    simbolo = simbolos[i % len(simbolos)]
                    print(f"  {simbolo} : f(x) = {funcion}")
                print("  X : Intersección de funciones")
            
            elif opcion == 4:
                funcion = input("Función a analizar f(x) = ")
                
                analisis, mensaje = analizar_funcion(funcion, x_min, x_max)
                
                if analisis:
                    print(f"\n=== ANÁLISIS DE f(x) = {funcion} ===")
                    print(f"Dominio analizado: [{x_min}, {x_max}]")
                    print(f"Puntos evaluados: {analisis['puntos_evaluados']}")
                    print(f"Valor mínimo Y: {analisis['minimo_y']:.4f}")
                    print(f"Valor máximo Y: {analisis['maximo_y']:.4f}")
                    print(f"Rango Y: {analisis['rango_y']:.4f}")
                    print(f"Promedio Y: {analisis['promedio_y']:.4f}")
                    
                    if analisis['ceros_aproximados']:
                        print(f"Ceros aproximados (cambios de signo):")
                        for cero in analisis['ceros_aproximados']:
                            print(f"  x ≈ {cero:.4f}")
                    else:
                        print("No se encontraron ceros en el dominio analizado")
                else:
                    print(f"❌ {mensaje}")
            
            elif opcion == 5:
                print(f"\nConfiguración actual:")
                print(f"Dominio X: [{x_min}, {x_max}]")
                print(f"Rango Y: [{y_min}, {y_max}]")
                print(f"Resolución: {ancho}×{alto}")
                
                try:
                    nuevo_x_min = float(input(f"Nuevo X mínimo ({x_min}): ") or x_min)
                    nuevo_x_max = float(input(f"Nuevo X máximo ({x_max}): ") or x_max)
                    nuevo_y_min = float(input(f"Nuevo Y mínimo ({y_min}): ") or y_min)
                    nuevo_y_max = float(input(f"Nuevo Y máximo ({y_max}): ") or y_max)
                    
                    if nuevo_x_min >= nuevo_x_max or nuevo_y_min >= nuevo_y_max:
                        print("❌ Error: Los valores mínimos deben ser menores que los máximos")
                        continue
                    
                    x_min, x_max = nuevo_x_min, nuevo_x_max
                    y_min, y_max = nuevo_y_min, nuevo_y_max
                    
                    print("✅ Configuración actualizada")
                    
                except ValueError:
                    print("❌ Error: Ingresa números válidos")
            
            elif opcion == 6:
                print("\n=== AYUDA SOBRE SINTAXIS ===")
                print("Variables:")
                print("  x - variable independiente")
                print("  π - pi (3.14159...)")
                print("  e - número de Euler (2.71828...)")
                
                print("\nOperadores:")
                print("  + - * /     - operaciones básicas")
                print("  **  o  ^    - potencia (x**2 o x^2)")
                print("  %           - módulo")
                
                print("\nFunciones trigonométricas:")
                print("  sin(x), cos(x), tan(x)")
                print("  asin(x), acos(x), atan(x)")
                print("  sinh(x), cosh(x), tanh(x)")
                
                print("\nFunciones logarítmicas y exponenciales:")
                print("  exp(x)      - e^x")
                print("  log(x)      - logaritmo natural")
                print("  log10(x)    - logaritmo base 10")
                print("  log2(x)     - logaritmo base 2")
                
                print("\nOtras funciones:")
                print("  sqrt(x)     - raíz cuadrada")
                print("  abs(x)      - valor absoluto")
                print("  ceil(x)     - redondeo hacia arriba")
                print("  floor(x)    - redondeo hacia abajo")
                
                print("\nEjemplos:")
                print("  x**2 + 3*x - 5")
                print("  sin(x) + cos(2*x)")
                print("  exp(-x**2)")
                print("  log(abs(x))")
                print("  sqrt(x**2 + 1)")
            
            elif opcion == 7:
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
