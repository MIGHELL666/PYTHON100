"""
Herramienta para medir el tiempo de ejecución de scripts y funciones
Autor: Tu nombre
Descripción: Decoradores y clases para benchmarking y análisis de rendimiento
"""

import time
import functools
import statistics
from datetime import datetime
import json
import csv

class ExecutionTimer:
    """Clase para medir tiempos de ejecución con múltiples funcionalidades"""
    
    def __init__(self):
        self.results = []
    
    def __enter__(self):
        """Permite usar 'with ExecutionTimer() as timer'"""
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, *args):
        """Se ejecuta automáticamente al salir del bloque 'with'"""
        self.end_time = time.perf_counter()
        self.execution_time = self.end_time - self.start_time
        print(f"⏱️  Tiempo de ejecución: {self.execution_time:.6f} segundos")
    
    def start(self):
        """Inicia el cronómetro manualmente"""
        self.start_time = time.perf_counter()
        print("🚀 Cronómetro iniciado...")
    
    def stop(self):
        """Detiene el cronómetro y muestra el resultado"""
        if not hasattr(self, 'start_time'):
            print("❌ Error: No se ha iniciado el cronómetro")
            return None
        
        self.end_time = time.perf_counter()
        self.execution_time = self.end_time - self.start_time
        print(f"🏁 Tiempo transcurrido: {self.execution_time:.6f} segundos")
        return self.execution_time
    
    def measure_function(self, func, *args, **kwargs):
        """Mide el tiempo de ejecución de una función específica"""
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        execution_time = end - start
        
        measurement = {
            'function': func.__name__,
            'args': str(args),
            'kwargs': str(kwargs),
            'execution_time': execution_time,
            'timestamp': datetime.now().isoformat()
        }
        
        self.results.append(measurement)
        print(f"📊 {func.__name__}(): {execution_time:.6f} segundos")
        return result, execution_time
    
    def benchmark(self, func, iterations=100, *args, **kwargs):
        """Ejecuta una función múltiples veces y calcula estadísticas"""
        print(f"🔄 Ejecutando benchmark de {func.__name__}() ({iterations} iteraciones)")
        times = []
        
        for i in range(iterations):
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)
            
            if (i + 1) % 10 == 0:
                print(f"   Progreso: {i + 1}/{iterations}")
        
        stats = {
            'function': func.__name__,
            'iterations': iterations,
            'total_time': sum(times),
            'average': statistics.mean(times),
            'median': statistics.median(times),
            'min': min(times),
            'max': max(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0,
            'timestamp': datetime.now().isoformat()
        }
        
        self.results.append(stats)
        self.print_benchmark_results(stats)
        return stats
    
    def print_benchmark_results(self, stats):
        """Imprime los resultados del benchmark de forma legible"""
        print(f"\n📈 Resultados del Benchmark - {stats['function']}()")
        print("=" * 50)
        print(f"Iteraciones:     {stats['iterations']}")
        print(f"Tiempo total:    {stats['total_time']:.6f} segundos")
        print(f"Promedio:        {stats['average']:.6f} segundos")
        print(f"Mediana:         {stats['median']:.6f} segundos")
        print(f"Mínimo:          {stats['min']:.6f} segundos")
        print(f"Máximo:          {stats['max']:.6f} segundos")
        print(f"Desv. estándar:  {stats['stdev']:.6f} segundos")
        print("=" * 50)
    
    def export_results(self, filename=None, format='json'):
        """Exporta los resultados a un archivo"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}"
        
        if format.lower() == 'json':
            filename += '.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
        elif format.lower() == 'csv':
            filename += '.csv'
            if self.results:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                    writer.writeheader()
                    writer.writerows(self.results)
        
        print(f"💾 Resultados exportados: {filename}")

def timing_decorator(func):
    """Decorador para medir automáticamente el tiempo de ejecución"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"⏱️  {func.__name__}() ejecutado en {end - start:.6f} segundos")
        return result
    return wrapper

def compare_functions(*functions):
    """Compara el tiempo de ejecución de múltiples funciones"""
    timer = ExecutionTimer()
    results = {}
    
    print("🏆 Comparación de funciones:")
    print("-" * 30)
    
    for func in functions:
        if callable(func):
            start = time.perf_counter()
            func()
            end = time.perf_counter()
            execution_time = end - start
            results[func.__name__] = execution_time
            print(f"{func.__name__}(): {execution_time:.6f} segundos")
    
    if results:
        fastest = min(results, key=results.get)
        slowest = max(results, key=results.get)
        print(f"\n🥇 Más rápida: {fastest}")
        print(f"🐌 Más lenta: {slowest}")
        improvement = results[slowest] / results[fastest]
        print(f"💡 {fastest} es {improvement:.2f}x más rápida que {slowest}")
    
    return results

# Ejemplos de uso y funciones de prueba
@timing_decorator
def ejemplo_rapido():
    """Función rápida para testing"""
    return sum(range(1000))

@timing_decorator
def ejemplo_lento():
    """Función más lenta para testing"""
    time.sleep(0.1)
    return sum(range(10000))

def ejemplo_cpu_intensivo():
    """Función que consume CPU"""
    return sum(i**2 for i in range(100000))

def ejemplo_sleep():
    """Función con sleep"""
    time.sleep(0.05)

if __name__ == "__main__":
    print("⏱️  Herramienta de Medición de Tiempo")
    print("=" * 40)
    
    # Ejemplo 1: Usar como context manager
    print("\n1. Usando context manager:")
    with ExecutionTimer() as timer:
        resultado = ejemplo_rapido()
    
    # Ejemplo 2: Usar manualmente
    print("\n2. Uso manual del cronómetro:")
    timer = ExecutionTimer()
    timer.start()
    ejemplo_lento()
    timer.stop()
    
    # Ejemplo 3: Medir función específica
    print("\n3. Midiendo función específica:")
    timer.measure_function(ejemplo_cpu_intensivo)
    
    # Ejemplo 4: Benchmark completo
    print("\n4. Benchmark con múltiples iteraciones:")
    timer.benchmark(ejemplo_cpu_intensivo, iterations=50)
    
    # Ejemplo 5: Comparar funciones
    print("\n5. Comparando funciones:")
    compare_functions(ejemplo_cpu_intensivo, ejemplo_sleep)
    
    # Exportar resultados
    timer.export_results("mi_benchmark", "json")