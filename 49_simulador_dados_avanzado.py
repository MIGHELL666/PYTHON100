"""
Proyecto 49: Simulador de dados avanzado con estadísticas
"""

import random
from collections import Counter

class Dado:
    """Clase para representar un dado"""
    
    def __init__(self, caras=6, personalizado=None):
        self.caras = caras
        self.valores = personalizado if personalizado else list(range(1, caras + 1))
        self.historial = []
    
    def lanzar(self):
        """Lanza el dado y registra el resultado"""
        resultado = random.choice(self.valores)
        self.historial.append(resultado)
        return resultado
    
    def lanzar_multiple(self, cantidad):
        """Lanza el dado múltiples veces"""
        resultados = []
        for _ in range(cantidad):
            resultados.append(self.lanzar())
        return resultados
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas del historial de lanzamientos"""
        if not self.historial:
            return None
        
        contador = Counter(self.historial)
        total_lanzamientos = len(self.historial)
        
        estadisticas = {
            'total_lanzamientos': total_lanzamientos,
            'valores_posibles': self.valores,
            'frecuencias': dict(contador),
            'porcentajes': {valor: (freq / total_lanzamientos) * 100 
                          for valor, freq in contador.items()},
            'valor_mas_frecuente': contador.most_common(1)[0],
            'valor_menos_frecuente': contador.most_common()[-1],
            'promedio': sum(self.historial) / total_lanzamientos,
            'minimo': min(self.historial),
            'maximo': max(self.historial)
        }
        
        return estadisticas
    
    def limpiar_historial(self):
        """Limpia el historial de lanzamientos"""
        self.historial = []

def simular_juego_yahtzee():
    """Simula un juego básico de Yahtzee (5 dados de 6 caras)"""
    dados = [Dado(6) for _ in range(5)]
    
    print("=== SIMULADOR DE YAHTZEE ===")
    print("Lanzando 5 dados...")
    
    resultados = [dado.lanzar() for dado in dados]
    print(f"Resultados: {resultados}")
    
    # Analizar combinaciones
    contador = Counter(resultados)
    valores_unicos = len(contador)
    frecuencias = list(contador.values())
    
    # Determinar tipo de jugada
    if 5 in frecuencias:
        jugada = "¡YAHTZEE! (5 iguales)"
    elif 4 in frecuencias:
        jugada = "Poker (4 iguales)"
    elif 3 in frecuencias and 2 in frecuencias:
        jugada = "Full House (3 + 2 iguales)"
    elif 3 in frecuencias:
        jugada = "Trío (3 iguales)"
    elif frecuencias.count(2) == 2:
        jugada = "Doble par"
    elif 2 in frecuencias:
        jugada = "Par"
    elif valores_unicos == 5:
        if set(resultados) in [{1,2,3,4,5}, {2,3,4,5,6}]:
            jugada = "Escalera"
        else:
            jugada = "Nada especial"
    else:
        jugada = "Nada especial"
    
    print(f"Jugada: {jugada}")
    
    return resultados, jugada

def simular_probabilidades_dados(num_dados, caras_por_dado, objetivo, num_simulaciones=10000):
    """Simula probabilidades de obtener una suma específica"""
    
    print(f"Simulando {num_simulaciones} lanzamientos de {num_dados} dados de {caras_por_dado} caras")
    print(f"Objetivo: suma = {objetivo}")
    
    exitos = 0
    sumas = []
    
    for _ in range(num_simulaciones):
        suma = sum(random.randint(1, caras_por_dado) for _ in range(num_dados))
        sumas.append(suma)
        if suma == objetivo:
            exitos += 1
    
    probabilidad_simulada = (exitos / num_simulaciones) * 100
    
    # Estadísticas de las sumas
    contador_sumas = Counter(sumas)
    suma_mas_frecuente = contador_sumas.most_common(1)[0]
    
    resultados = {
        'exitos': exitos,
        'probabilidad': probabilidad_simulada,
        'suma_promedio': sum(sumas) / len(sumas),
        'suma_mas_frecuente': suma_mas_frecuente,
        'distribucion': dict(contador_sumas)
    }
    
    return resultados

def crear_dado_personalizado():
    """Permite crear un dado con valores personalizados"""
    print("=== CREAR DADO PERSONALIZADO ===")
    
    tipo = input("Tipo de dado personalizado:\n1. Valores numéricos\n2. Valores de texto\nSelecciona: ")
    
    if tipo == '1':
        valores_str = input("Ingresa los valores separados por comas (ej: 1,2,3,4,5,6): ")
        try:
            valores = [int(x.strip()) for x in valores_str.split(',')]
        except ValueError:
            print("❌ Error: Ingresa solo números válidos")
            return None
    
    elif tipo == '2':
        valores_str = input("Ingresa los valores de texto separados por comas (ej: Cara,Cruz,Lado): ")
        valores = [x.strip() for x in valores_str.split(',')]
    
    else:
        print("❌ Opción no válida")
        return None
    
    if len(valores) < 2:
        print("❌ Error: El dado debe tener al menos 2 valores")
        return None
    
    dado = Dado(len(valores), valores)
    print(f"✅ Dado personalizado creado con valores: {valores}")
    
    return dado

def mostrar_histograma_ascii(frecuencias, titulo="Histograma"):
    """Muestra un histograma ASCII de las frecuencias"""
    if not frecuencias:
        print("No hay datos para mostrar")
        return
    
    print(f"\n=== {titulo} ===")
    
    # Encontrar el valor máximo para escalar
    max_freq = max(frecuencias.values())
    ancho_max = 50  # Ancho máximo del histograma
    
    # Ordenar por clave
    items_ordenados = sorted(frecuencias.items())
    
    for valor, freq in items_ordenados:
        # Calcular longitud de la barra
        if max_freq > 0:
            longitud_barra = int((freq / max_freq) * ancho_max)
        else:
            longitud_barra = 0
        
        barra = '█' * longitud_barra
        porcentaje = (freq / sum(frecuencias.values())) * 100
        
        print(f"{str(valor):>6} |{barra:<{ancho_max}} {freq:>4} ({porcentaje:5.1f}%)")

def juego_adivinanza_dados():
    """Juego donde el usuario adivina el resultado de los dados"""
    print("=== JUEGO: ADIVINA LA SUMA ===")
    
    try:
        num_dados = int(input("¿Cuántos dados usar? (1-10): "))
        if not 1 <= num_dados <= 10:
            print("❌ Número de dados debe estar entre 1 y 10")
            return
        
        caras = int(input("¿Cuántas caras por dado? (2-20): "))
        if not 2 <= caras <= 20:
            print("❌ Número de caras debe estar entre 2 y 20")
            return
        
        suma_minima = num_dados
        suma_maxima = num_dados * caras
        
        print(f"\nUsando {num_dados} dados de {caras} caras")
        print(f"Suma posible: {suma_minima} - {suma_maxima}")
        
        adivinanza = int(input("¿Cuál crees que será la suma? "))
        
        if not suma_minima <= adivinanza <= suma_maxima:
            print(f"❌ La suma debe estar entre {suma_minima} y {suma_maxima}")
            return
        
        # Lanzar dados
        dados = [Dado(caras) for _ in range(num_dados)]
        resultados = [dado.lanzar() for dado in dados]
        suma_real = sum(resultados)
        
        print(f"\nResultados de los dados: {resultados}")
        print(f"Suma real: {suma_real}")
        print(f"Tu adivinanza: {adivinanza}")
        
        diferencia = abs(suma_real - adivinanza)
        
        if diferencia == 0:
            print("🎉 ¡PERFECTO! Adivinaste exactamente")
        elif diferencia <= 2:
            print("👍 ¡Muy cerca! Diferencia de", diferencia)
        elif diferencia <= 5:
            print("👌 Bastante cerca. Diferencia de", diferencia)
        else:
            print("😅 No tan cerca. Diferencia de", diferencia)
        
    except ValueError:
        print("❌ Error: Ingresa números válidos")

def main():
    print("=== SIMULADOR DE DADOS AVANZADO ===")
    
    # Dados predefinidos
    dados_disponibles = {
        'clasico': Dado(6),
        'personalizado': None
    }
    
    while True:
        print("\n1. Lanzar dado clásico (6 caras)")
        print("2. Lanzar múltiples dados")
        print("3. Crear dado personalizado")
        print("4. Simulador de Yahtzee")
        print("5. Análisis de probabilidades")
        print("6. Ver estadísticas de dado")
        print("7. Juego de adivinanza")
        print("8. Limpiar historial")
        print("9. Salir")
        
        try:
            opcion = int(input("Selecciona una opción: "))
            
            if opcion == 1:
                resultado = dados_disponibles['clasico'].lanzar()
                print(f"🎲 Resultado: {resultado}")
                
                # Mostrar estadísticas básicas
                stats = dados_disponibles['clasico'].obtener_estadisticas()
                if stats and stats['total_lanzamientos'] > 1:
                    print(f"Lanzamientos totales: {stats['total_lanzamientos']}")
                    print(f"Promedio: {stats['promedio']:.2f}")
            
            elif opcion == 2:
                num_dados = int(input("¿Cuántos dados lanzar? "))
                caras = int(input("¿Cuántas caras por dado? (6 por defecto): ") or "6")
                
                if num_dados <= 0 or caras <= 0:
                    print("❌ Los valores deben ser positivos")
                    continue
                
                dados = [Dado(caras) for _ in range(num_dados)]
                resultados = [dado.lanzar() for dado in dados]
                
                print(f"🎲 Resultados: {resultados}")
                print(f"Suma total: {sum(resultados)}")
                print(f"Promedio: {sum(resultados) / len(resultados):.2f}")
                
                # Mostrar frecuencias si hay valores repetidos
                contador = Counter(resultados)
                if len(contador) < len(resultados):
                    print("Frecuencias:")
                    for valor, freq in sorted(contador.items()):
                        print(f"  {valor}: {freq} vez(es)")
            
            elif opcion == 3:
                dado_personalizado = crear_dado_personalizado()
                if dado_personalizado:
                    dados_disponibles['personalizado'] = dado_personalizado
                    
                    # Hacer algunos lanzamientos de prueba
                    print("\nLanzamientos de prueba:")
                    for i in range(5):
                        resultado = dado_personalizado.lanzar()
                        print(f"Lanzamiento {i+1}: {resultado}")
            
            elif opcion == 4:
                resultados, jugada = simular_juego_yahtzee()
                
                # Ofrecer relanzar
                relanzar = input("\n¿Quieres simular otro lanzamiento? (s/n): ").lower() == 's'
                if relanzar:
                    print("\nSegundo lanzamiento:")
                    simular_juego_yahtzee()
            
            elif opcion == 5:
                print("=== ANÁLISIS DE PROBABILIDADES ===")
                
                num_dados = int(input("Número de dados: "))
                caras = int(input("Caras por dado: "))
                objetivo = int(input("Suma objetivo: "))
                simulaciones = int(input("Número de simulaciones (10000 por defecto): ") or "10000")
                
                if num_dados <= 0 or caras <= 0 or simulaciones <= 0:
                    print("❌ Todos los valores deben ser positivos")
                    continue
                
                suma_min = num_dados
                suma_max = num_dados * caras
                
                if not suma_min <= objetivo <= suma_max:
                    print(f"❌ El objetivo debe estar entre {suma_min} y {suma_max}")
                    continue
                
                print(f"\nEjecutando {simulaciones} simulaciones...")
                resultados = simular_probabilidades_dados(num_dados, caras, objetivo, simulaciones)
                
                print(f"\n=== RESULTADOS ===")
                print(f"Éxitos: {resultados['exitos']}")
                print(f"Probabilidad simulada: {resultados['probabilidad']:.2f}%")
                print(f"Suma promedio: {resultados['suma_promedio']:.2f}")
                print(f"Suma más frecuente: {resultados['suma_mas_frecuente'][0]} ({resultados['suma_mas_frecuente'][1]} veces)")
                
                # Mostrar histograma de las sumas más frecuentes
                top_sumas = dict(Counter(resultados['distribucion']).most_common(10))
                mostrar_histograma_ascii(top_sumas, "Top 10 Sumas Más Frecuentes")
            
            elif opcion == 6:
                print("¿De qué dado ver estadísticas?")
                print("1. Dado clásico")
                print("2. Dado personalizado")
                
                tipo_dado = input("Selecciona: ")
                
                if tipo_dado == '1':
                    stats = dados_disponibles['clasico'].obtener_estadisticas()
                    nombre = "Dado Clásico (6 caras)"
                elif tipo_dado == '2' and dados_disponibles['personalizado']:
                    stats = dados_disponibles['personalizado'].obtener_estadisticas()
                    nombre = "Dado Personalizado"
                else:
                    print("❌ Dado no disponible o sin historial")
                    continue
                
                if stats:
                    print(f"\n=== ESTADÍSTICAS: {nombre} ===")
                    print(f"Total de lanzamientos: {stats['total_lanzamientos']}")
                    print(f"Valores posibles: {stats['valores_posibles']}")
                    print(f"Promedio: {stats['promedio']:.2f}")
                    print(f"Mínimo: {stats['minimo']}")
                    print(f"Máximo: {stats['maximo']}")
                    print(f"Más frecuente: {stats['valor_mas_frecuente'][0]} ({stats['valor_mas_frecuente'][1]} veces)")
                    print(f"Menos frecuente: {stats['valor_menos_frecuente'][0]} ({stats['valor_menos_frecuente'][1]} veces)")
                    
                    mostrar_histograma_ascii(stats['frecuencias'], "Distribución de Resultados")
                else:
                    print("❌ No hay estadísticas disponibles (sin lanzamientos)")
            
            elif opcion == 7:
                juego_adivinanza_dados()
            
            elif opcion == 8:
                print("¿Qué historial limpiar?")
                print("1. Dado clásico")
                print("2. Dado personalizado")
                print("3. Ambos")
                
                limpiar = input("Selecciona: ")
                
                if limpiar in ['1', '3']:
                    dados_disponibles['clasico'].limpiar_historial()
                    print("✅ Historial del dado clásico limpiado")
                
                if limpiar in ['2', '3'] and dados_disponibles['personalizado']:
                    dados_disponibles['personalizado'].limpiar_historial()
                    print("✅ Historial del dado personalizado limpiado")
            
            elif opcion == 9:
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
