"""
Proyecto 58: Encriptador de Texto
Sistema de encriptación y desencriptación con múltiples algoritmos.
"""

import base64
import hashlib
import json
import os
from datetime import datetime

class EncriptadorTexto:
    def __init__(self):
        self.historial_archivo = "historial_encriptacion.json"
        self.historial = self.cargar_historial()
    
    def cargar_historial(self):
        """Carga el historial de encriptaciones"""
        try:
            with open(self.historial_archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def guardar_historial(self):
        """Guarda el historial de encriptaciones"""
        try:
            with open(self.historial_archivo, 'w', encoding='utf-8') as f:
                json.dump(self.historial, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    
    def cifrado_cesar(self, texto, desplazamiento, encriptar=True):
        """Implementa el cifrado César"""
        if not encriptar:
            desplazamiento = -desplazamiento
        
        resultado = ""
        for char in texto:
            if char.isalpha():
                # Determinar si es mayúscula o minúscula
                base = ord('A') if char.isupper() else ord('a')
                # Aplicar desplazamiento circular
                nuevo_char = chr((ord(char) - base + desplazamiento) % 26 + base)
                resultado += nuevo_char
            else:
                resultado += char
        
        return resultado
    
    def cifrado_atbash(self, texto):
        """Implementa el cifrado Atbash (A=Z, B=Y, etc.)"""
        resultado = ""
        for char in texto:
            if char.isalpha():
                if char.isupper():
                    # A=0, Z=25 -> A se convierte en Z (25), B en Y (24), etc.
                    nuevo_char = chr(ord('Z') - (ord(char) - ord('A')))
                else:
                    nuevo_char = chr(ord('z') - (ord(char) - ord('a')))
                resultado += nuevo_char
            else:
                resultado += char
        
        return resultado
    
    def cifrado_vigenere(self, texto, clave, encriptar=True):
        """Implementa el cifrado Vigenère"""
        if not clave:
            return texto
        
        clave = clave.upper()
        resultado = ""
        indice_clave = 0
        
        for char in texto:
            if char.isalpha():
                # Obtener el desplazamiento de la clave
                desplazamiento = ord(clave[indice_clave % len(clave)]) - ord('A')
                
                if not encriptar:
                    desplazamiento = -desplazamiento
                
                # Aplicar cifrado César con el desplazamiento de la clave
                base = ord('A') if char.isupper() else ord('a')
                nuevo_char = chr((ord(char) - base + desplazamiento) % 26 + base)
                resultado += nuevo_char
                
                indice_clave += 1
            else:
                resultado += char
        
        return resultado
    
    def cifrado_base64(self, texto, encriptar=True):
        """Codificación/decodificación Base64"""
        try:
            if encriptar:
                # Convertir texto a bytes y luego a base64
                texto_bytes = texto.encode('utf-8')
                resultado = base64.b64encode(texto_bytes).decode('utf-8')
            else:
                # Decodificar de base64 a texto
                texto_bytes = base64.b64decode(texto.encode('utf-8'))
                resultado = texto_bytes.decode('utf-8')
            
            return resultado
        except Exception as e:
            return f"Error en Base64: {str(e)}"
    
    def cifrado_sustitucion(self, texto, alfabeto_sustitucion, encriptar=True):
        """Cifrado por sustitución con alfabeto personalizado"""
        alfabeto_normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        if len(alfabeto_sustitucion) != 26:
            return "Error: El alfabeto de sustitución debe tener 26 caracteres"
        
        resultado = ""
        for char in texto:
            if char.isalpha():
                es_mayuscula = char.isupper()
                char_upper = char.upper()
                
                if encriptar:
                    # Encontrar posición en alfabeto normal y sustituir
                    if char_upper in alfabeto_normal:
                        indice = alfabeto_normal.index(char_upper)
                        nuevo_char = alfabeto_sustitucion[indice]
                    else:
                        nuevo_char = char
                else:
                    # Encontrar posición en alfabeto de sustitución y revertir
                    if char_upper in alfabeto_sustitucion:
                        indice = alfabeto_sustitucion.index(char_upper)
                        nuevo_char = alfabeto_normal[indice]
                    else:
                        nuevo_char = char
                
                # Mantener el caso original
                if not es_mayuscula:
                    nuevo_char = nuevo_char.lower()
                
                resultado += nuevo_char
            else:
                resultado += char
        
        return resultado
    
    def generar_hash(self, texto, algoritmo='sha256'):
        """Genera hash del texto (no reversible)"""
        try:
            texto_bytes = texto.encode('utf-8')
            
            if algoritmo == 'md5':
                hash_obj = hashlib.md5(texto_bytes)
            elif algoritmo == 'sha1':
                hash_obj = hashlib.sha1(texto_bytes)
            elif algoritmo == 'sha256':
                hash_obj = hashlib.sha256(texto_bytes)
            elif algoritmo == 'sha512':
                hash_obj = hashlib.sha512(texto_bytes)
            else:
                return "Algoritmo de hash no soportado"
            
            return hash_obj.hexdigest()
        except Exception as e:
            return f"Error generando hash: {str(e)}"
    
    def cifrado_rail_fence(self, texto, rieles, encriptar=True):
        """Implementa el cifrado Rail Fence (Zigzag)"""
        if rieles <= 1:
            return texto
        
        if encriptar:
            # Crear matriz para los rieles
            fence = [[] for _ in range(rieles)]
            riel = 0
            direccion = 1
            
            # Colocar caracteres en zigzag
            for char in texto:
                fence[riel].append(char)
                riel += direccion
                
                # Cambiar dirección en los extremos
                if riel == rieles - 1 or riel == 0:
                    direccion = -direccion
            
            # Leer por filas
            resultado = ""
            for fila in fence:
                resultado += "".join(fila)
            
            return resultado
        else:
            # Desencriptar: reconstruir el patrón zigzag
            # Calcular longitudes de cada riel
            longitudes = [0] * rieles
            riel = 0
            direccion = 1
            
            for _ in texto:
                longitudes[riel] += 1
                riel += direccion
                if riel == rieles - 1 or riel == 0:
                    direccion = -direccion
            
            # Llenar los rieles con los caracteres
            fence = []
            indice = 0
            for i in range(rieles):
                fence.append(list(texto[indice:indice + longitudes[i]]))
                indice += longitudes[i]
            
            # Reconstruir el texto original
            resultado = ""
            riel = 0
            direccion = 1
            indices = [0] * rieles
            
            for _ in texto:
                resultado += fence[riel][indices[riel]]
                indices[riel] += 1
                riel += direccion
                if riel == rieles - 1 or riel == 0:
                    direccion = -direccion
            
            return resultado
    
    def procesar_encriptacion(self, texto, metodo, parametros, encriptar=True):
        """Procesa la encriptación según el método seleccionado"""
        accion = "Encriptación" if encriptar else "Desencriptación"
        
        try:
            if metodo == "cesar":
                desplazamiento = parametros.get('desplazamiento', 3)
                resultado = self.cifrado_cesar(texto, desplazamiento, encriptar)
            
            elif metodo == "atbash":
                resultado = self.cifrado_atbash(texto)
            
            elif metodo == "vigenere":
                clave = parametros.get('clave', '')
                resultado = self.cifrado_vigenere(texto, clave, encriptar)
            
            elif metodo == "base64":
                resultado = self.cifrado_base64(texto, encriptar)
            
            elif metodo == "sustitucion":
                alfabeto = parametros.get('alfabeto', 'ZYXWVUTSRQPONMLKJIHGFEDCBA')
                resultado = self.cifrado_sustitucion(texto, alfabeto, encriptar)
            
            elif metodo == "rail_fence":
                rieles = parametros.get('rieles', 3)
                resultado = self.cifrado_rail_fence(texto, rieles, encriptar)
            
            elif metodo == "hash":
                if not encriptar:
                    return "Error: Los hashes no se pueden desencriptar"
                algoritmo = parametros.get('algoritmo', 'sha256')
                resultado = self.generar_hash(texto, algoritmo)
            
            else:
                return "Método de encriptación no reconocido"
            
            # Guardar en historial
            registro = {
                'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'accion': accion,
                'metodo': metodo,
                'parametros': parametros,
                'texto_original': texto[:50] + "..." if len(texto) > 50 else texto,
                'resultado': resultado[:50] + "..." if len(resultado) > 50 else resultado
            }
            
            self.historial.append(registro)
            self.guardar_historial()
            
            return resultado
            
        except Exception as e:
            return f"Error en {accion.lower()}: {str(e)}"
    
    def mostrar_metodos_disponibles(self):
        """Muestra información sobre los métodos disponibles"""
        print("\n=== MÉTODOS DE ENCRIPTACIÓN DISPONIBLES ===")
        
        metodos = {
            "César": "Desplaza cada letra un número fijo de posiciones",
            "Atbash": "Sustituye A por Z, B por Y, etc.",
            "Vigenère": "Usa una palabra clave para el desplazamiento",
            "Base64": "Codificación estándar (no es encriptación real)",
            "Sustitución": "Reemplaza el alfabeto por otro personalizado",
            "Rail Fence": "Escribe el texto en zigzag y lee por filas",
            "Hash": "Genera hash irreversible (MD5, SHA1, SHA256, SHA512)"
        }
        
        for i, (nombre, descripcion) in enumerate(metodos.items(), 1):
            print(f"{i}. {nombre}: {descripcion}")
    
    def mostrar_historial(self, limite=10):
        """Muestra el historial de operaciones"""
        if not self.historial:
            print("No hay operaciones en el historial.")
            return
        
        print(f"\n=== HISTORIAL DE OPERACIONES (últimas {limite}) ===")
        for operacion in self.historial[-limite:]:
            print(f"\n[{operacion['fecha']}] {operacion['accion']}")
            print(f"Método: {operacion['metodo'].title()}")
            if operacion['parametros']:
                print(f"Parámetros: {operacion['parametros']}")
            print(f"Texto: {operacion['texto_original']}")
            print(f"Resultado: {operacion['resultado']}")
            print("-" * 50)

def main():
    encriptador = EncriptadorTexto()
    
    while True:
        print("\n=== ENCRIPTADOR DE TEXTO ===")
        print("1. Encriptar texto")
        print("2. Desencriptar texto")
        print("3. Generar hash")
        print("4. Ver métodos disponibles")
        print("5. Ver historial")
        print("6. Salir")
        
        opcion = input("\nSelecciona una opción (1-6): ").strip()
        
        if opcion in ["1", "2"]:
            encriptar = opcion == "1"
            accion = "encriptar" if encriptar else "desencriptar"
            
            texto = input(f"Ingresa el texto a {accion}: ").strip()
            if not texto:
                print("El texto no puede estar vacío.")
                continue
            
            print(f"\nMétodos disponibles:")
            metodos = ["cesar", "atbash", "vigenere", "base64", "sustitucion", "rail_fence"]
            for i, metodo in enumerate(metodos, 1):
                print(f"{i}. {metodo.title()}")
            
            try:
                seleccion = int(input("Selecciona un método (1-6): ")) - 1
                if not 0 <= seleccion < len(metodos):
                    print("Selección inválida.")
                    continue
                
                metodo = metodos[seleccion]
                parametros = {}
                
                # Obtener parámetros específicos del método
                if metodo == "cesar":
                    try:
                        desplazamiento = int(input("Desplazamiento (default: 3): ") or "3")
                        parametros['desplazamiento'] = desplazamiento
                    except ValueError:
                        parametros['desplazamiento'] = 3
                
                elif metodo == "vigenere":
                    clave = input("Palabra clave: ").strip()
                    if not clave:
                        print("La clave no puede estar vacía para Vigenère.")
                        continue
                    parametros['clave'] = clave
                
                elif metodo == "sustitucion":
                    alfabeto = input("Alfabeto de sustitución (26 letras, default: ZYXWVUTSRQPONMLKJIHGFEDCBA): ").strip()
                    if not alfabeto:
                        alfabeto = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
                    parametros['alfabeto'] = alfabeto.upper()
                
                elif metodo == "rail_fence":
                    try:
                        rieles = int(input("Número de rieles (default: 3): ") or "3")
                        parametros['rieles'] = max(2, rieles)
                    except ValueError:
                        parametros['rieles'] = 3
                
                # Procesar
                resultado = encriptador.procesar_encriptacion(texto, metodo, parametros, encriptar)
                
                print(f"\n=== RESULTADO ===")
                print(f"Método: {metodo.title()}")
                print(f"Texto original: {texto}")
                print(f"Resultado: {resultado}")
                
                # Opción de guardar en archivo
                guardar = input("\n¿Guardar resultado en archivo? (s/n): ").strip().lower()
                if guardar == 's':
                    nombre_archivo = input("Nombre del archivo (sin extensión): ").strip()
                    if nombre_archivo:
                        try:
                            with open(f"{nombre_archivo}.txt", 'w', encoding='utf-8') as f:
                                f.write(f"Método: {metodo.title()}\n")
                                f.write(f"Parámetros: {parametros}\n")
                                f.write(f"Texto original: {texto}\n")
                                f.write(f"Resultado: {resultado}\n")
                                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            print(f"Resultado guardado en {nombre_archivo}.txt")
                        except Exception as e:
                            print(f"Error al guardar archivo: {e}")
                
            except ValueError:
                print("Selección inválida.")
        
        elif opcion == "3":
            texto = input("Ingresa el texto para generar hash: ").strip()
            if not texto:
                print("El texto no puede estar vacío.")
                continue
            
            print("Algoritmos disponibles:")
            algoritmos = ["md5", "sha1", "sha256", "sha512"]
            for i, alg in enumerate(algoritmos, 1):
                print(f"{i}. {alg.upper()}")
            
            try:
                seleccion = int(input("Selecciona un algoritmo (1-4): ")) - 1
                if not 0 <= seleccion < len(algoritmos):
                    print("Selección inválida.")
                    continue
                
                algoritmo = algoritmos[seleccion]
                parametros = {'algoritmo': algoritmo}
                
                resultado = encriptador.procesar_encriptacion(texto, "hash", parametros, True)
                
                print(f"\n=== HASH GENERADO ===")
                print(f"Algoritmo: {algoritmo.upper()}")
                print(f"Texto original: {texto}")
                print(f"Hash: {resultado}")
                
            except ValueError:
                print("Selección inválida.")
        
        elif opcion == "4":
            encriptador.mostrar_metodos_disponibles()
        
        elif opcion == "5":
            try:
                limite = int(input("Número de operaciones a mostrar (default: 10): ") or "10")
                encriptador.mostrar_historial(limite)
            except ValueError:
                encriptador.mostrar_historial()
        
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
