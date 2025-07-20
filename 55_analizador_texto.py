"""
Proyecto 55: Analizador de Texto Avanzado
Analiza textos con estadísticas detalladas, legibilidad y más.
"""

import re
import json
import os
from collections import Counter
from datetime import datetime

class AnalizadorTexto:
    def __init__(self):
        self.historial_archivo = "historial_analisis.json"
        self.historial = self.cargar_historial()
        
        # Palabras comunes en español para filtrar
        self.palabras_comunes = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se',
            'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para',
            'al', 'del', 'los', 'las', 'una', 'pero', 'sus', 'me', 'si', 'o',
            'como', 'ya', 'muy', 'más', 'todo', 'todos', 'esta', 'este', 'está'
        }
    
    def cargar_historial(self):
        """Carga el historial de análisis"""
        try:
            with open(self.historial_archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def guardar_historial(self):
        """Guarda el historial de análisis"""
        try:
            with open(self.historial_archivo, 'w', encoding='utf-8') as f:
                json.dump(self.historial, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    
    def limpiar_texto(self, texto):
        """Limpia el texto para análisis"""
        # Convertir a minúsculas y eliminar caracteres especiales
        texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
        return texto_limpio
    
    def contar_estadisticas_basicas(self, texto):
        """Cuenta estadísticas básicas del texto"""
        # Caracteres
        total_caracteres = len(texto)
        caracteres_sin_espacios = len(texto.replace(' ', ''))
        
        # Palabras
        palabras = texto.split()
        total_palabras = len(palabras)
        
        # Oraciones (aproximado)
        oraciones = re.split(r'[.!?]+', texto)
        oraciones = [o.strip() for o in oraciones if o.strip()]
        total_oraciones = len(oraciones)
        
        # Párrafos
        paragrafos = [p.strip() for p in texto.split('\n') if p.strip()]
        total_paragrafos = len(paragrafos)
        
        return {
            'caracteres_total': total_caracteres,
            'caracteres_sin_espacios': caracteres_sin_espacios,
            'palabras': total_palabras,
            'oraciones': total_oraciones,
            'paragrafos': total_paragrafos
        }
    
    def analizar_palabras(self, texto):
        """Analiza las palabras del texto"""
        texto_limpio = self.limpiar_texto(texto)
        palabras = texto_limpio.split()
        
        # Contar frecuencia de palabras
        contador_palabras = Counter(palabras)
        
        # Palabras únicas
        palabras_unicas = len(contador_palabras)
        
        # Palabras más comunes (excluyendo palabras comunes)
        palabras_significativas = {
            palabra: freq for palabra, freq in contador_palabras.items()
            if palabra not in self.palabras_comunes and len(palabra) > 2
        }
        
        palabras_frecuentes = Counter(palabras_significativas).most_common(10)
        
        # Longitud promedio de palabras
        if palabras:
            longitud_promedio = sum(len(palabra) for palabra in palabras) / len(palabras)
        else:
            longitud_promedio = 0
        
        return {
            'palabras_unicas': palabras_unicas,
            'palabras_frecuentes': palabras_frecuentes,
            'longitud_promedio_palabra': round(longitud_promedio, 2)
        }
    
    def calcular_legibilidad(self, texto):
        """Calcula índices de legibilidad"""
        estadisticas = self.contar_estadisticas_basicas(texto)
        
        if estadisticas['oraciones'] == 0 or estadisticas['palabras'] == 0:
            return {'error': 'Texto insuficiente para calcular legibilidad'}
        
        # Promedio de palabras por oración
        palabras_por_oracion = estadisticas['palabras'] / estadisticas['oraciones']
        
        # Promedio de caracteres por palabra
        if estadisticas['palabras'] > 0:
            caracteres_por_palabra = estadisticas['caracteres_sin_espacios'] / estadisticas['palabras']
        else:
            caracteres_por_palabra = 0
        
        # Índice de legibilidad simplificado (basado en Flesch)
        # Fórmula adaptada: 206.835 - (1.015 × palabras/oración) - (84.6 × sílabas/palabra)
        # Aproximamos sílabas usando caracteres por palabra
        silabas_aprox = caracteres_por_palabra / 2.5
        
        indice_flesch = 206.835 - (1.015 * palabras_por_oracion) - (84.6 * silabas_aprox)
        
        # Clasificar legibilidad
        if indice_flesch >= 90:
            nivel = "Muy fácil"
        elif indice_flesch >= 80:
            nivel = "Fácil"
        elif indice_flesch >= 70:
            nivel = "Bastante fácil"
        elif indice_flesch >= 60:
            nivel = "Normal"
        elif indice_flesch >= 50:
            nivel = "Bastante difícil"
        elif indice_flesch >= 30:
            nivel = "Difícil"
        else:
            nivel = "Muy difícil"
        
        return {
            'palabras_por_oracion': round(palabras_por_oracion, 2),
            'caracteres_por_palabra': round(caracteres_por_palabra, 2),
            'indice_flesch': round(indice_flesch, 2),
            'nivel_legibilidad': nivel
        }
    
    def analizar_sentimientos_basico(self, texto):
        """Análisis básico de sentimientos usando palabras clave"""
        palabras_positivas = {
            'bueno', 'excelente', 'fantástico', 'genial', 'increíble', 'maravilloso',
            'perfecto', 'hermoso', 'alegre', 'feliz', 'contento', 'satisfecho',
            'amor', 'éxito', 'victoria', 'ganar', 'logro', 'triunfo'
        }
        
        palabras_negativas = {
            'malo', 'terrible', 'horrible', 'pésimo', 'desastroso', 'awful',
            'triste', 'deprimido', 'enojado', 'furioso', 'odio', 'fracaso',
            'perder', 'derrota', 'problema', 'error', 'difícil', 'imposible'
        }
        
        texto_limpio = self.limpiar_texto(texto)
        palabras = texto_limpio.split()
        
        positivas_encontradas = sum(1 for palabra in palabras if palabra in palabras_positivas)
        negativas_encontradas = sum(1 for palabra in palabras if palabra in palabras_negativas)
        
        total_palabras = len(palabras)
        if total_palabras == 0:
            return {'error': 'No hay palabras para analizar'}
        
        porcentaje_positivo = (positivas_encontradas / total_palabras) * 100
        porcentaje_negativo = (negativas_encontradas / total_palabras) * 100
        
        # Determinar sentimiento general
        if positivas_encontradas > negativas_encontradas:
            sentimiento = "Positivo"
        elif negativas_encontradas > positivas_encontradas:
            sentimiento = "Negativo"
        else:
            sentimiento = "Neutral"
        
        return {
            'palabras_positivas': positivas_encontradas,
            'palabras_negativas': negativas_encontradas,
            'porcentaje_positivo': round(porcentaje_positivo, 2),
            'porcentaje_negativo': round(porcentaje_negativo, 2),
            'sentimiento_general': sentimiento
        }
    
    def generar_reporte_completo(self, texto, titulo=""):
        """Genera un reporte completo del análisis"""
        if not texto.strip():
            return None
        
        # Realizar todos los análisis
        estadisticas = self.contar_estadisticas_basicas(texto)
        analisis_palabras = self.analizar_palabras(texto)
        legibilidad = self.calcular_legibilidad(texto)
        sentimientos = self.analizar_sentimientos_basico(texto)
        
        reporte = {
            'titulo': titulo or f"Análisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'estadisticas_basicas': estadisticas,
            'analisis_palabras': analisis_palabras,
            'legibilidad': legibilidad,
            'sentimientos': sentimientos,
            'texto_original': texto[:200] + "..." if len(texto) > 200 else texto
        }
        
        return reporte
    
    def mostrar_reporte(self, reporte):
        """Muestra un reporte de análisis formateado"""
        print(f"\n{'='*60}")
        print(f"REPORTE DE ANÁLISIS DE TEXTO")
        print(f"{'='*60}")
        print(f"Título: {reporte['titulo']}")
        print(f"Fecha: {reporte['fecha']}")
        
        # Estadísticas básicas
        print(f"\n--- ESTADÍSTICAS BÁSICAS ---")
        stats = reporte['estadisticas_basicas']
        print(f"Caracteres totales: {stats['caracteres_total']:,}")
        print(f"Caracteres sin espacios: {stats['caracteres_sin_espacios']:,}")
        print(f"Palabras: {stats['palabras']:,}")
        print(f"Oraciones: {stats['oraciones']:,}")
        print(f"Párrafos: {stats['paragrafos']:,}")
        
        # Análisis de palabras
        print(f"\n--- ANÁLISIS DE PALABRAS ---")
        palabras = reporte['analisis_palabras']
        print(f"Palabras únicas: {palabras['palabras_unicas']:,}")
        print(f"Longitud promedio de palabra: {palabras['longitud_promedio_palabra']} caracteres")
        
        if palabras['palabras_frecuentes']:
            print(f"\nPalabras más frecuentes:")
            for i, (palabra, freq) in enumerate(palabras['palabras_frecuentes'][:5], 1):
                print(f"  {i}. {palabra}: {freq} veces")
        
        # Legibilidad
        print(f"\n--- LEGIBILIDAD ---")
        leg = reporte['legibilidad']
        if 'error' not in leg:
            print(f"Palabras por oración: {leg['palabras_por_oracion']}")
            print(f"Caracteres por palabra: {leg['caracteres_por_palabra']}")
            print(f"Índice Flesch: {leg['indice_flesch']}")
            print(f"Nivel de legibilidad: {leg['nivel_legibilidad']}")
        else:
            print(f"Error: {leg['error']}")
        
        # Sentimientos
        print(f"\n--- ANÁLISIS DE SENTIMIENTOS ---")
        sent = reporte['sentimientos']
        if 'error' not in sent:
            print(f"Sentimiento general: {sent['sentimiento_general']}")
            print(f"Palabras positivas: {sent['palabras_positivas']} ({sent['porcentaje_positivo']}%)")
            print(f"Palabras negativas: {sent['palabras_negativas']} ({sent['porcentaje_negativo']}%)")
        else:
            print(f"Error: {sent['error']}")
        
        print(f"\n{'='*60}")
    
    def guardar_reporte(self, reporte, nombre_archivo=None):
        """Guarda el reporte en un archivo"""
        if not nombre_archivo:
            nombre_archivo = f"reporte_{reporte['titulo']}.json"
        
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump(reporte, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar reporte: {e}")
            return False
    
    def agregar_al_historial(self, reporte):
        """Agrega un reporte al historial"""
        # Guardar solo información resumida en el historial
        resumen = {
            'titulo': reporte['titulo'],
            'fecha': reporte['fecha'],
            'palabras': reporte['estadisticas_basicas']['palabras'],
            'caracteres': reporte['estadisticas_basicas']['caracteres_total'],
            'sentimiento': reporte['sentimientos'].get('sentimiento_general', 'N/A'),
            'legibilidad': reporte['legibilidad'].get('nivel_legibilidad', 'N/A')
        }
        
        self.historial.append(resumen)
        self.guardar_historial()
    
    def mostrar_historial(self):
        """Muestra el historial de análisis"""
        if not self.historial:
            print("No hay análisis en el historial.")
            return
        
        print("\n=== HISTORIAL DE ANÁLISIS ===")
        for i, analisis in enumerate(self.historial[-10:], 1):
            print(f"\n{i}. {analisis['titulo']}")
            print(f"   Fecha: {analisis['fecha']}")
            print(f"   Palabras: {analisis['palabras']:,}")
            print(f"   Caracteres: {analisis['caracteres']:,}")
            print(f"   Sentimiento: {analisis['sentimiento']}")
            print(f"   Legibilidad: {analisis['legibilidad']}")

def main():
    analizador = AnalizadorTexto()
    
    while True:
        print("\n=== ANALIZADOR DE TEXTO AVANZADO ===")
        print("1. Analizar texto ingresado")
        print("2. Analizar archivo de texto")
        print("3. Ver historial de análisis")
        print("4. Ejemplo de análisis")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            print("\nIngresa el texto a analizar (presiona Enter dos veces para terminar):")
            lineas = []
            while True:
                linea = input()
                if linea == "" and lineas and lineas[-1] == "":
                    break
                lineas.append(linea)
            
            texto = '\n'.join(lineas[:-1])  # Remover última línea vacía
            
            if texto.strip():
                titulo = input("Título del análisis (opcional): ").strip()
                reporte = analizador.generar_reporte_completo(texto, titulo)
                
                if reporte:
                    analizador.mostrar_reporte(reporte)
                    analizador.agregar_al_historial(reporte)
                    
                    guardar = input("\n¿Guardar reporte en archivo? (s/n): ").strip().lower()
                    if guardar == 's':
                        nombre = input("Nombre del archivo (sin extensión): ").strip()
                        if nombre:
                            if analizador.guardar_reporte(reporte, f"{nombre}.json"):
                                print(f"Reporte guardado en {nombre}.json")
            else:
                print("No se ingresó texto para analizar.")
        
        elif opcion == "2":
            archivo = input("Nombre del archivo de texto: ").strip()
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    texto = f.read()
                
                if texto.strip():
                    titulo = input("Título del análisis (opcional): ").strip() or archivo
                    reporte = analizador.generar_reporte_completo(texto, titulo)
                    
                    if reporte:
                        analizador.mostrar_reporte(reporte)
                        analizador.agregar_al_historial(reporte)
                        
                        guardar = input("\n¿Guardar reporte en archivo? (s/n): ").strip().lower()
                        if guardar == 's':
                            nombre = input("Nombre del archivo (sin extensión): ").strip()
                            if nombre:
                                if analizador.guardar_reporte(reporte, f"{nombre}.json"):
                                    print(f"Reporte guardado en {nombre}.json")
                else:
                    print("El archivo está vacío.")
                    
            except FileNotFoundError:
                print("Archivo no encontrado.")
            except Exception as e:
                print(f"Error al leer archivo: {e}")
        
        elif opcion == "3":
            analizador.mostrar_historial()
        
        elif opcion == "4":
            texto_ejemplo = """
            La inteligencia artificial es una tecnología fascinante que está transformando nuestro mundo.
            Desde asistentes virtuales hasta vehículos autónomos, la IA está presente en muchos aspectos de nuestra vida diaria.
            
            Sin embargo, también presenta desafíos importantes. La privacidad, la seguridad y el impacto en el empleo
            son temas que debemos abordar cuidadosamente. Es fundamental que desarrollemos esta tecnología de manera
            responsable y ética.
            
            El futuro de la IA es prometedor, pero requiere la colaboración entre tecnólogos, reguladores y la sociedad
            en general para asegurar que beneficie a toda la humanidad.
            """
            
            print("Analizando texto de ejemplo...")
            reporte = analizador.generar_reporte_completo(texto_ejemplo, "Ejemplo - IA")
            if reporte:
                analizador.mostrar_reporte(reporte)
        
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
