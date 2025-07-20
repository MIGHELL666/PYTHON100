"""
Script para tomar capturas de pantalla automáticas
Autor: Tu nombre
Descripción: Herramienta para capturar pantalla completa o área específica
"""

import pyautogui
import os
from datetime import datetime
import argparse

class ScreenshotTool:
    def __init__(self):
        """Inicializa la herramienta de capturas"""
        # Crear directorio para capturas si no existe
        self.screenshots_dir = "capturas"
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)
    
    def capture_full_screen(self, filename=None):
        """Captura la pantalla completa"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captura_completa_{timestamp}.png"
        
        filepath = os.path.join(self.screenshots_dir, filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        print(f"✅ Captura guardada: {filepath}")
        return filepath
    
    def capture_region(self, x, y, width, height, filename=None):
        """Captura una región específica de la pantalla"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captura_region_{timestamp}.png"
        
        filepath = os.path.join(self.screenshots_dir, filename)
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot.save(filepath)
        print(f"✅ Captura de región guardada: {filepath}")
        return filepath
    
    def capture_with_delay(self, delay=3, filename=None):
        """Captura con retraso (útil para preparar la pantalla)"""
        print(f"⏰ Captura en {delay} segundos...")
        pyautogui.sleep(delay)
        return self.capture_full_screen(filename)
    
    def get_screen_size(self):
        """Obtiene las dimensiones de la pantalla"""
        size = pyautogui.size()
        print(f"📏 Resolución de pantalla: {size.width}x{size.height}")
        return size

def main():
    """Función principal con interfaz de línea de comandos"""
    parser = argparse.ArgumentParser(description="Herramienta de capturas de pantalla")
    parser.add_argument("--tipo", choices=["completa", "region", "delay"], 
                       default="completa", help="Tipo de captura")
    parser.add_argument("--delay", type=int, default=3, 
                       help="Segundos de retraso para captura con delay")
    parser.add_argument("--x", type=int, default=0, help="Coordenada X para región")
    parser.add_argument("--y", type=int, default=0, help="Coordenada Y para región")
    parser.add_argument("--width", type=int, default=800, help="Ancho de región")
    parser.add_argument("--height", type=int, default=600, help="Alto de región")
    parser.add_argument("--filename", help="Nombre del archivo de salida")
    
    args = parser.parse_args()
    
    tool = ScreenshotTool()
    tool.get_screen_size()
    
    if args.tipo == "completa":
        tool.capture_full_screen(args.filename)
    elif args.tipo == "region":
        tool.capture_region(args.x, args.y, args.width, args.height, args.filename)
    elif args.tipo == "delay":
        tool.capture_with_delay(args.delay, args.filename)

if __name__ == "__main__":
    # Ejemplo de uso interactivo si se ejecuta directamente
    print("🖼️  Herramienta de Capturas de Pantalla")
    print("=" * 40)
    
    tool = ScreenshotTool()
    
    while True:
        print("\nOpciones:")
        print("1. Captura completa")
        print("2. Captura con retraso")
        print("3. Captura de región")
        print("4. Ver tamaño de pantalla")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            tool.capture_full_screen()
        elif opcion == "2":
            delay = int(input("Segundos de retraso (default 3): ") or "3")
            tool.capture_with_delay(delay)
        elif opcion == "3":
            print("Ingresa las coordenadas de la región:")
            x = int(input("X: ") or "0")
            y = int(input("Y: ") or "0")
            width = int(input("Ancho: ") or "800")
            height = int(input("Alto: ") or "600")
            tool.capture_region(x, y, width, height)
        elif opcion == "4":
            tool.get_screen_size()
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida")

# Requisitos:
# pip install pyautogui