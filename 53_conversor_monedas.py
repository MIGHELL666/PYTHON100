"""
Proyecto 53: Conversor de Monedas
Convierte entre diferentes monedas con tasas de cambio actualizables.
"""

import json
import os
from datetime import datetime, timedelta

class ConversorMonedas:
    def __init__(self):
        self.archivo_tasas = "tasas_cambio.json"
        self.tasas = self.cargar_tasas()
        self.monedas_disponibles = {
            'USD': 'Dólar Estadounidense',
            'EUR': 'Euro',
            'GBP': 'Libra Esterlina',
            'JPY': 'Yen Japonés',
            'CAD': 'Dólar Canadiense',
            'AUD': 'Dólar Australiano',
            'CHF': 'Franco Suizo',
            'CNY': 'Yuan Chino',
            'MXN': 'Peso Mexicano',
            'BRL': 'Real Brasileño',
            'ARS': 'Peso Argentino',
            'COP': 'Peso Colombiano',
            'CLP': 'Peso Chileno',
            'PEN': 'Sol Peruano'
        }
    
    def cargar_tasas(self):
        """Carga las tasas de cambio desde archivo"""
        try:
            with open(self.archivo_tasas, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.obtener_tasas_predeterminadas()
    
    def obtener_tasas_predeterminadas(self):
        """Proporciona tasas de cambio predeterminadas (base USD)"""
        return {
            'fecha_actualizacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'base': 'USD',
            'tasas': {
                'USD': 1.0,
                'EUR': 0.85,
                'GBP': 0.73,
                'JPY': 110.0,
                'CAD': 1.25,
                'AUD': 1.35,
                'CHF': 0.92,
                'CNY': 6.45,
                'MXN': 20.0,
                'BRL': 5.2,
                'ARS': 350.0,
                'COP': 4000.0,
                'CLP': 800.0,
                'PEN': 3.8
            }
        }
    
    def guardar_tasas(self):
        """Guarda las tasas de cambio en archivo"""
        try:
            with open(self.archivo_tasas, 'w', encoding='utf-8') as f:
                json.dump(self.tasas, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar tasas: {e}")
    
    def convertir(self, cantidad, moneda_origen, moneda_destino):
        """Convierte una cantidad de una moneda a otra"""
        if moneda_origen not in self.tasas['tasas'] or moneda_destino not in self.tasas['tasas']:
            return None
        
        # Convertir a USD primero (moneda base)
        if moneda_origen != 'USD':
            cantidad_usd = cantidad / self.tasas['tasas'][moneda_origen]
        else:
            cantidad_usd = cantidad
        
        # Convertir de USD a moneda destino
        if moneda_destino != 'USD':
            resultado = cantidad_usd * self.tasas['tasas'][moneda_destino]
        else:
            resultado = cantidad_usd
        
        return resultado
    
    def mostrar_monedas_disponibles(self):
        """Muestra todas las monedas disponibles"""
        print("\n=== MONEDAS DISPONIBLES ===")
        for codigo, nombre in self.monedas_disponibles.items():
            tasa = self.tasas['tasas'].get(codigo, 'N/A')
            print(f"{codigo}: {nombre} (Tasa: {tasa})")
    
    def actualizar_tasa(self, moneda, nueva_tasa):
        """Actualiza la tasa de cambio de una moneda"""
        if moneda in self.tasas['tasas']:
            self.tasas['tasas'][moneda] = nueva_tasa
            self.tasas['fecha_actualizacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.guardar_tasas()
            return True
        return False
    
    def obtener_tabla_conversion(self, moneda_base, cantidad=1):
        """Genera una tabla de conversión para una moneda base"""
        print(f"\n=== TABLA DE CONVERSIÓN ({cantidad} {moneda_base}) ===")
        print(f"Actualizado: {self.tasas['fecha_actualizacion']}")
        print("-" * 50)
        
        for codigo, nombre in self.monedas_disponibles.items():
            if codigo != moneda_base:
                resultado = self.convertir(cantidad, moneda_base, codigo)
                if resultado is not None:
                    print(f"{codigo}: {resultado:.4f} ({nombre})")
    
    def calcular_conversion_inversa(self, cantidad, moneda_origen, moneda_destino):
        """Calcula cuánto se necesita en moneda origen para obtener cantidad en destino"""
        resultado = self.convertir(cantidad, moneda_destino, moneda_origen)
        return resultado
    
    def mostrar_tendencias(self):
        """Muestra información sobre las tasas (simulado)"""
        print("\n=== INFORMACIÓN DE TASAS ===")
        print(f"Última actualización: {self.tasas['fecha_actualizacion']}")
        print(f"Moneda base: {self.tasas['base']}")
        print("\nTasas más altas:")
        
        # Ordenar por tasa (excluyendo USD que es 1.0)
        tasas_ordenadas = sorted(
            [(k, v) for k, v in self.tasas['tasas'].items() if k != 'USD'],
            key=lambda x: x[1],
            reverse=True
        )
        
        for i, (moneda, tasa) in enumerate(tasas_ordenadas[:5]):
            nombre = self.monedas_disponibles.get(moneda, moneda)
            print(f"{i+1}. {moneda} ({nombre}): {tasa}")
    
    def realizar_conversion_interactiva(self):
        """Realiza una conversión interactiva"""
        print("\n=== CONVERSIÓN DE MONEDAS ===")
        
        # Mostrar monedas disponibles
        print("Monedas disponibles:")
        codigos = list(self.monedas_disponibles.keys())
        for i, codigo in enumerate(codigos):
            print(f"{i+1}. {codigo} - {self.monedas_disponibles[codigo]}")
        
        try:
            # Seleccionar moneda origen
            print(f"\nSelecciona moneda origen (1-{len(codigos)}):")
            indice_origen = int(input()) - 1
            if not 0 <= indice_origen < len(codigos):
                print("Selección inválida.")
                return
            moneda_origen = codigos[indice_origen]
            
            # Seleccionar moneda destino
            print(f"\nSelecciona moneda destino (1-{len(codigos)}):")
            indice_destino = int(input()) - 1
            if not 0 <= indice_destino < len(codigos):
                print("Selección inválida.")
                return
            moneda_destino = codigos[indice_destino]
            
            # Obtener cantidad
            cantidad = float(input(f"\nCantidad en {moneda_origen}: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor que 0.")
                return
            
            # Realizar conversión
            resultado = self.convertir(cantidad, moneda_origen, moneda_destino)
            
            if resultado is not None:
                print(f"\n=== RESULTADO ===")
                print(f"{cantidad:,.2f} {moneda_origen} = {resultado:,.4f} {moneda_destino}")
                
                # Mostrar tasa de cambio
                tasa = resultado / cantidad
                print(f"Tasa de cambio: 1 {moneda_origen} = {tasa:.4f} {moneda_destino}")
                
                # Conversión inversa
                inversa = self.calcular_conversion_inversa(1, moneda_origen, moneda_destino)
                if inversa:
                    print(f"Tasa inversa: 1 {moneda_destino} = {inversa:.4f} {moneda_origen}")
            else:
                print("Error en la conversión.")
                
        except ValueError:
            print("Por favor, ingresa valores numéricos válidos.")
        except Exception as e:
            print(f"Error: {e}")

def main():
    conversor = ConversorMonedas()
    
    while True:
        print("\n=== CONVERSOR DE MONEDAS ===")
        print("1. Convertir monedas")
        print("2. Ver monedas disponibles")
        print("3. Tabla de conversión")
        print("4. Actualizar tasa de cambio")
        print("5. Ver información de tasas")
        print("6. Salir")
        
        opcion = input("\nSelecciona una opción (1-6): ").strip()
        
        if opcion == "1":
            conversor.realizar_conversion_interactiva()
        
        elif opcion == "2":
            conversor.mostrar_monedas_disponibles()
        
        elif opcion == "3":
            print("Monedas disponibles:")
            for i, codigo in enumerate(conversor.monedas_disponibles.keys()):
                print(f"{i+1}. {codigo}")
            
            try:
                indice = int(input("Selecciona moneda base: ")) - 1
                codigos = list(conversor.monedas_disponibles.keys())
                if 0 <= indice < len(codigos):
                    moneda = codigos[indice]
                    cantidad = float(input(f"Cantidad base (default 1): ") or "1")
                    conversor.obtener_tabla_conversion(moneda, cantidad)
            except (ValueError, IndexError):
                print("Selección inválida.")
        
        elif opcion == "4":
            conversor.mostrar_monedas_disponibles()
            moneda = input("\nCódigo de moneda a actualizar: ").upper().strip()
            if moneda in conversor.monedas_disponibles:
                try:
                    nueva_tasa = float(input(f"Nueva tasa para {moneda} (base USD): "))
                    if conversor.actualizar_tasa(moneda, nueva_tasa):
                        print(f"Tasa de {moneda} actualizada a {nueva_tasa}")
                    else:
                        print("Error al actualizar la tasa.")
                except ValueError:
                    print("Tasa inválida.")
            else:
                print("Moneda no encontrada.")
        
        elif opcion == "5":
            conversor.mostrar_tendencias()
        
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
