"""
Proyecto 54: Generador de Códigos QR
Genera códigos QR para texto, URLs, contactos y más usando ASCII art.
"""

import json
import os
from datetime import datetime

class GeneradorQR:
    def __init__(self):
        self.historial_archivo = "historial_qr.json"
        self.historial = self.cargar_historial()
    
    def cargar_historial(self):
        """Carga el historial de códigos QR generados"""
        try:
            with open(self.historial_archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def guardar_historial(self):
        """Guarda el historial de códigos QR"""
        try:
            with open(self.historial_archivo, 'w', encoding='utf-8') as f:
                json.dump(self.historial, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    
    def texto_a_binario(self, texto):
        """Convierte texto a representación binaria"""
        return ''.join(format(ord(char), '08b') for char in texto)
    
    def generar_patron_qr(self, datos, tamaño=21):
        """Genera un patrón QR simplificado usando ASCII"""
        # Crear matriz base
        matriz = [['0' for _ in range(tamaño)] for _ in range(tamaño)]
        
        # Agregar patrones de posición (esquinas)
        self.agregar_patron_posicion(matriz, 0, 0)
        self.agregar_patron_posicion(matriz, 0, tamaño-7)
        self.agregar_patron_posicion(matriz, tamaño-7, 0)
        
        # Agregar patrón de tiempo
        self.agregar_patron_tiempo(matriz, tamaño)
        
        # Simular datos (patrón basado en hash del texto)
        self.agregar_datos_simulados(matriz, datos, tamaño)
        
        return matriz
    
    def agregar_patron_posicion(self, matriz, fila, col):
        """Agrega patrón de posición 7x7"""
        patron = [
            [1,1,1,1,1,1,1],
            [1,0,0,0,0,0,1],
            [1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1],
            [1,0,1,1,1,0,1],
            [1,0,0,0,0,0,1],
            [1,1,1,1,1,1,1]
        ]
        
        for i in range(7):
            for j in range(7):
                if fila + i < len(matriz) and col + j < len(matriz[0]):
                    matriz[fila + i][col + j] = str(patron[i][j])
    
    def agregar_patron_tiempo(self, matriz, tamaño):
        """Agrega patrones de tiempo"""
        # Línea horizontal
        for i in range(8, tamaño-8):
            matriz[6][i] = str(i % 2)
        
        # Línea vertical
        for i in range(8, tamaño-8):
            matriz[i][6] = str(i % 2)
    
    def agregar_datos_simulados(self, matriz, datos, tamaño):
        """Agrega datos simulados basados en el contenido"""
        hash_datos = hash(datos) % 1000
        
        # Llenar áreas disponibles con patrón basado en hash
        for i in range(tamaño):
            for j in range(tamaño):
                if matriz[i][j] == '0' and not self.es_area_reservada(i, j, tamaño):
                    # Usar hash para determinar el patrón
                    valor = (hash_datos + i * j) % 2
                    matriz[i][j] = str(valor)
    
    def es_area_reservada(self, fila, col, tamaño):
        """Verifica si un área está reservada para patrones especiales"""
        # Patrones de posición
        if (fila < 9 and col < 9) or \
           (fila < 9 and col >= tamaño-8) or \
           (fila >= tamaño-8 and col < 9):
            return True
        
        # Patrones de tiempo
        if fila == 6 or col == 6:
            return True
        
        return False
    
    def matriz_a_ascii(self, matriz, usar_bloques=True):
        """Convierte la matriz QR a ASCII art"""
        if usar_bloques:
            char_lleno = '██'
            char_vacio = '  '
        else:
            char_lleno = '##'
            char_vacio = '  '
        
        ascii_art = []
        for fila in matriz:
            linea = ''
            for celda in fila:
                if celda == '1':
                    linea += char_lleno
                else:
                    linea += char_vacio
            ascii_art.append(linea)
        
        return '\n'.join(ascii_art)
    
    def generar_qr_texto(self, texto):
        """Genera QR para texto simple"""
        if not texto.strip():
            return None
        
        matriz = self.generar_patron_qr(texto)
        return self.matriz_a_ascii(matriz)
    
    def generar_qr_url(self, url):
        """Genera QR para URL"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        matriz = self.generar_patron_qr(url)
        return self.matriz_a_ascii(matriz)
    
    def generar_qr_contacto(self, nombre, telefono, email=""):
        """Genera QR para contacto (formato vCard)"""
        vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{nombre}\nTEL:{telefono}"
        if email:
            vcard += f"\nEMAIL:{email}"
        vcard += "\nEND:VCARD"
        
        matriz = self.generar_patron_qr(vcard)
        return self.matriz_a_ascii(matriz)
    
    def generar_qr_wifi(self, ssid, password, security="WPA"):
        """Genera QR para conexión WiFi"""
        wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};;"
        matriz = self.generar_patron_qr(wifi_string)
        return self.matriz_a_ascii(matriz)
    
    def guardar_qr_archivo(self, qr_ascii, nombre_archivo):
        """Guarda el código QR en un archivo de texto"""
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write(qr_ascii)
            return True
        except Exception as e:
            print(f"Error al guardar archivo: {e}")
            return False
    
    def agregar_al_historial(self, tipo, contenido, datos_extra=None):
        """Agrega una entrada al historial"""
        entrada = {
            "tipo": tipo,
            "contenido": contenido,
            "datos_extra": datos_extra or {},
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.historial.append(entrada)
        self.guardar_historial()
    
    def mostrar_historial(self):
        """Muestra el historial de códigos QR generados"""
        if not self.historial:
            print("No hay códigos QR en el historial.")
            return
        
        print("\n=== HISTORIAL DE CÓDIGOS QR ===")
        for i, entrada in enumerate(self.historial[-10:], 1):
            print(f"\n{i}. Tipo: {entrada['tipo']}")
            print(f"   Fecha: {entrada['fecha']}")
            print(f"   Contenido: {entrada['contenido'][:50]}...")
            if entrada.get('datos_extra'):
                for key, value in entrada['datos_extra'].items():
                    print(f"   {key}: {value}")
    
    def menu_interactivo(self):
        """Menú interactivo para generar códigos QR"""
        while True:
            print("\n=== GENERADOR DE CÓDIGOS QR ===")
            print("1. Texto simple")
            print("2. URL/Sitio web")
            print("3. Contacto (vCard)")
            print("4. WiFi")
            print("5. Ver historial")
            print("6. Salir")
            
            opcion = input("\nSelecciona una opción (1-6): ").strip()
            
            if opcion == "1":
                texto = input("Ingresa el texto: ").strip()
                if texto:
                    qr = self.generar_qr_texto(texto)
                    if qr:
                        print(f"\n=== CÓDIGO QR PARA TEXTO ===")
                        print(qr)
                        
                        guardar = input("\n¿Guardar en archivo? (s/n): ").strip().lower()
                        if guardar == 's':
                            nombre = input("Nombre del archivo (sin extensión): ").strip()
                            if nombre:
                                if self.guardar_qr_archivo(qr, f"{nombre}.txt"):
                                    print(f"QR guardado en {nombre}.txt")
                        
                        self.agregar_al_historial("Texto", texto)
            
            elif opcion == "2":
                url = input("Ingresa la URL: ").strip()
                if url:
                    qr = self.generar_qr_url(url)
                    if qr:
                        print(f"\n=== CÓDIGO QR PARA URL ===")
                        print(qr)
                        
                        guardar = input("\n¿Guardar en archivo? (s/n): ").strip().lower()
                        if guardar == 's':
                            nombre = input("Nombre del archivo (sin extensión): ").strip()
                            if nombre:
                                if self.guardar_qr_archivo(qr, f"{nombre}.txt"):
                                    print(f"QR guardado en {nombre}.txt")
                        
                        self.agregar_al_historial("URL", url)
            
            elif opcion == "3":
                nombre = input("Nombre del contacto: ").strip()
                telefono = input("Teléfono: ").strip()
                email = input("Email (opcional): ").strip()
                
                if nombre and telefono:
                    qr = self.generar_qr_contacto(nombre, telefono, email)
                    if qr:
                        print(f"\n=== CÓDIGO QR PARA CONTACTO ===")
                        print(qr)
                        
                        guardar = input("\n¿Guardar en archivo? (s/n): ").strip().lower()
                        if guardar == 's':
                            archivo = input("Nombre del archivo (sin extensión): ").strip()
                            if archivo:
                                if self.guardar_qr_archivo(qr, f"{archivo}.txt"):
                                    print(f"QR guardado en {archivo}.txt")
                        
                        self.agregar_al_historial("Contacto", nombre, {
                            "telefono": telefono,
                            "email": email
                        })
                else:
                    print("Nombre y teléfono son obligatorios.")
            
            elif opcion == "4":
                ssid = input("Nombre de la red WiFi (SSID): ").strip()
                password = input("Contraseña: ").strip()
                security = input("Tipo de seguridad (WPA/WEP/nopass) [WPA]: ").strip() or "WPA"
                
                if ssid:
                    qr = self.generar_qr_wifi(ssid, password, security)
                    if qr:
                        print(f"\n=== CÓDIGO QR PARA WIFI ===")
                        print(qr)
                        
                        guardar = input("\n¿Guardar en archivo? (s/n): ").strip().lower()
                        if guardar == 's':
                            archivo = input("Nombre del archivo (sin extensión): ").strip()
                            if archivo:
                                if self.guardar_qr_archivo(qr, f"{archivo}.txt"):
                                    print(f"QR guardado en {archivo}.txt")
                        
                        self.agregar_al_historial("WiFi", ssid, {
                            "security": security
                        })
                else:
                    print("El nombre de la red es obligatorio.")
            
            elif opcion == "5":
                self.mostrar_historial()
            
            elif opcion == "6":
                print("¡Hasta luego!")
                break
            
            else:
                print("Opción no válida. Intenta de nuevo.")

def main():
    generador = GeneradorQR()
    
    print("=== GENERADOR DE CÓDIGOS QR ===")
    print("Genera códigos QR en formato ASCII para diferentes tipos de contenido.")
    print("Nota: Estos son códigos QR simulados para demostración.")
    
    generador.menu_interactivo()

if __name__ == "__main__":
    main()
