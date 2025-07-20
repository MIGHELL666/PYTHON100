"""
Proyecto 57: Simulador de Clima
Simula condiciones climáticas y genera pronósticos con datos realistas.
"""

import random
import json
import os
from datetime import datetime, timedelta

class SimuladorClima:
    def __init__(self):
        self.historial_archivo = "historial_clima.json"
        self.historial = self.cargar_historial()
        
        # Configuraciones base por estación
        self.estaciones = {
            'primavera': {
                'temp_min': 15, 'temp_max': 25,
                'humedad_min': 40, 'humedad_max': 70,
                'presion_min': 1010, 'presion_max': 1025,
                'probabilidad_lluvia': 0.3
            },
            'verano': {
                'temp_min': 25, 'temp_max': 35,
                'humedad_min': 30, 'humedad_max': 60,
                'presion_min': 1005, 'presion_max': 1020,
                'probabilidad_lluvia': 0.2
            },
            'otoño': {
                'temp_min': 10, 'temp_max': 20,
                'humedad_min': 50, 'humedad_max': 80,
                'presion_min': 1015, 'presion_max': 1030,
                'probabilidad_lluvia': 0.4
            },
            'invierno': {
                'temp_min': 0, 'temp_max': 15,
                'humedad_min': 60, 'humedad_max': 90,
                'presion_min': 1020, 'presion_max': 1035,
                'probabilidad_lluvia': 0.5
            }
        }
        
        self.tipos_clima = [
            'Soleado', 'Parcialmente nublado', 'Nublado', 'Lluvioso',
            'Tormentoso', 'Nevado', 'Ventoso', 'Brumoso'
        ]
        
        self.direcciones_viento = [
            'Norte', 'Noreste', 'Este', 'Sureste',
            'Sur', 'Suroeste', 'Oeste', 'Noroeste'
        ]
    
    def cargar_historial(self):
        """Carga el historial de simulaciones"""
        try:
            with open(self.historial_archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def guardar_historial(self):
        """Guarda el historial de simulaciones"""
        try:
            with open(self.historial_archivo, 'w', encoding='utf-8') as f:
                json.dump(self.historial, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    
    def obtener_estacion_actual(self, fecha=None):
        """Determina la estación del año basada en la fecha"""
        if not fecha:
            fecha = datetime.now()
        
        mes = fecha.month
        
        if mes in [12, 1, 2]:
            return 'invierno'
        elif mes in [3, 4, 5]:
            return 'primavera'
        elif mes in [6, 7, 8]:
            return 'verano'
        else:
            return 'otoño'
    
    def generar_condiciones_base(self, estacion):
        """Genera condiciones climáticas base para una estación"""
        config = self.estaciones[estacion]
        
        temperatura = random.uniform(config['temp_min'], config['temp_max'])
        humedad = random.uniform(config['humedad_min'], config['humedad_max'])
        presion = random.uniform(config['presion_min'], config['presion_max'])
        
        # Velocidad del viento (km/h)
        velocidad_viento = random.uniform(5, 30)
        direccion_viento = random.choice(self.direcciones_viento)
        
        # Determinar si llueve
        llueve = random.random() < config['probabilidad_lluvia']
        precipitacion = random.uniform(0.1, 15.0) if llueve else 0.0
        
        return {
            'temperatura': round(temperatura, 1),
            'humedad': round(humedad, 1),
            'presion': round(presion, 1),
            'velocidad_viento': round(velocidad_viento, 1),
            'direccion_viento': direccion_viento,
            'precipitacion': round(precipitacion, 1),
            'llueve': llueve
        }
    
    def determinar_tipo_clima(self, condiciones):
        """Determina el tipo de clima basado en las condiciones"""
        temp = condiciones['temperatura']
        humedad = condiciones['humedad']
        precipitacion = condiciones['precipitacion']
        viento = condiciones['velocidad_viento']
        
        if precipitacion > 10:
            return 'Tormentoso'
        elif precipitacion > 0.5:
            if temp < 2:
                return 'Nevado'
            else:
                return 'Lluvioso'
        elif humedad > 85:
            return 'Brumoso'
        elif viento > 25:
            return 'Ventoso'
        elif humedad > 70:
            return 'Nublado'
        elif humedad > 50:
            return 'Parcialmente nublado'
        else:
            return 'Soleado'
    
    def calcular_sensacion_termica(self, temperatura, humedad, viento):
        """Calcula la sensación térmica"""
        # Fórmula simplificada de sensación térmica
        if temperatura < 10:
            # Factor de enfriamiento por viento
            sensacion = temperatura - (viento * 0.5)
        else:
            # Factor de calor por humedad
            factor_humedad = (humedad - 40) * 0.1
            sensacion = temperatura + factor_humedad
        
        return round(sensacion, 1)
    
    def calcular_indice_uv(self, tipo_clima, hora=12):
        """Calcula un índice UV aproximado"""
        base_uv = 8  # Valor base al mediodía
        
        # Ajustar por hora del día
        if hora < 6 or hora > 18:
            base_uv = 0
        elif hora < 10 or hora > 16:
            base_uv *= 0.5
        elif 10 <= hora <= 14:
            base_uv *= 1.2
        
        # Ajustar por tipo de clima
        if tipo_clima in ['Soleado']:
            multiplicador = 1.0
        elif tipo_clima in ['Parcialmente nublado']:
            multiplicador = 0.8
        elif tipo_clima in ['Nublado', 'Brumoso']:
            multiplicador = 0.5
        else:
            multiplicador = 0.3
        
        indice = base_uv * multiplicador
        return max(0, round(indice, 1))
    
    def generar_clima_completo(self, fecha=None, ubicacion="Ciudad"):
        """Genera un reporte climático completo"""
        if not fecha:
            fecha = datetime.now()
        
        estacion = self.obtener_estacion_actual(fecha)
        condiciones = self.generar_condiciones_base(estacion)
        tipo_clima = self.determinar_tipo_clima(condiciones)
        
        sensacion_termica = self.calcular_sensacion_termica(
            condiciones['temperatura'],
            condiciones['humedad'],
            condiciones['velocidad_viento']
        )
        
        indice_uv = self.calcular_indice_uv(tipo_clima, fecha.hour)
        
        # Visibilidad (km)
        if tipo_clima == 'Brumoso':
            visibilidad = random.uniform(0.5, 3.0)
        elif tipo_clima in ['Lluvioso', 'Tormentoso']:
            visibilidad = random.uniform(2.0, 8.0)
        else:
            visibilidad = random.uniform(8.0, 20.0)
        
        reporte = {
            'fecha': fecha.strftime("%Y-%m-%d"),
            'hora': fecha.strftime("%H:%M"),
            'ubicacion': ubicacion,
            'estacion': estacion.capitalize(),
            'tipo_clima': tipo_clima,
            'temperatura': condiciones['temperatura'],
            'sensacion_termica': sensacion_termica,
            'humedad': condiciones['humedad'],
            'presion': condiciones['presion'],
            'viento': {
                'velocidad': condiciones['velocidad_viento'],
                'direccion': condiciones['direccion_viento']
            },
            'precipitacion': condiciones['precipitacion'],
            'visibilidad': round(visibilidad, 1),
            'indice_uv': indice_uv
        }
        
        return reporte
    
    def generar_pronostico(self, dias=7, ubicacion="Ciudad"):
        """Genera un pronóstico extendido"""
        pronostico = []
        fecha_actual = datetime.now()
        
        for i in range(dias):
            fecha = fecha_actual + timedelta(days=i)
            
            # Generar clima para diferentes horas del día
            clima_dia = {}
            
            # Mañana (8:00)
            fecha_mañana = fecha.replace(hour=8, minute=0)
            clima_dia['mañana'] = self.generar_clima_completo(fecha_mañana, ubicacion)
            
            # Tarde (14:00)
            fecha_tarde = fecha.replace(hour=14, minute=0)
            clima_dia['tarde'] = self.generar_clima_completo(fecha_tarde, ubicacion)
            
            # Noche (20:00)
            fecha_noche = fecha.replace(hour=20, minute=0)
            clima_dia['noche'] = self.generar_clima_completo(fecha_noche, ubicacion)
            
            # Resumen del día
            temperaturas = [
                clima_dia['mañana']['temperatura'],
                clima_dia['tarde']['temperatura'],
                clima_dia['noche']['temperatura']
            ]
            
            resumen = {
                'fecha': fecha.strftime("%Y-%m-%d"),
                'dia_semana': fecha.strftime("%A"),
                'temp_min': min(temperaturas),
                'temp_max': max(temperaturas),
                'clima_predominante': clima_dia['tarde']['tipo_clima'],
                'precipitacion_total': sum([
                    clima_dia['mañana']['precipitacion'],
                    clima_dia['tarde']['precipitacion'],
                    clima_dia['noche']['precipitacion']
                ]),
                'detalle': clima_dia
            }
            
            pronostico.append(resumen)
        
        return pronostico
    
    def mostrar_clima_actual(self, ubicacion="Ciudad"):
        """Muestra el clima actual"""
        clima = self.generar_clima_completo(ubicacion=ubicacion)
        
        print(f"\n{'='*60}")
        print(f"CLIMA ACTUAL - {clima['ubicacion'].upper()}")
        print(f"{'='*60}")
        print(f"Fecha: {clima['fecha']} | Hora: {clima['hora']}")
        print(f"Estación: {clima['estacion']}")
        print(f"\n🌤️  Condición: {clima['tipo_clima']}")
        print(f"🌡️  Temperatura: {clima['temperatura']}°C (Sensación: {clima['sensacion_termica']}°C)")
        print(f"💧 Humedad: {clima['humedad']}%")
        print(f"📊 Presión: {clima['presion']} hPa")
        print(f"💨 Viento: {clima['viento']['velocidad']} km/h {clima['viento']['direccion']}")
        
        if clima['precipitacion'] > 0:
            print(f"🌧️  Precipitación: {clima['precipitacion']} mm")
        
        print(f"👁️  Visibilidad: {clima['visibilidad']} km")
        print(f"☀️  Índice UV: {clima['indice_uv']}")
        
        # Recomendaciones
        self.mostrar_recomendaciones(clima)
        
        return clima
    
    def mostrar_recomendaciones(self, clima):
        """Muestra recomendaciones basadas en el clima"""
        print(f"\n📋 RECOMENDACIONES:")
        
        temp = clima['temperatura']
        tipo = clima['tipo_clima']
        uv = clima['indice_uv']
        viento = clima['viento']['velocidad']
        
        if temp < 5:
            print("• Abrígate bien, hace mucho frío")
        elif temp < 15:
            print("• Usa chaqueta o suéter")
        elif temp > 30:
            print("• Mantente hidratado y busca sombra")
        
        if tipo in ['Lluvioso', 'Tormentoso']:
            print("• Lleva paraguas o impermeable")
        
        if uv > 7:
            print("• Usa protector solar y lentes de sol")
        
        if viento > 20:
            print("• Cuidado con objetos que puedan volar")
        
        if clima['visibilidad'] < 5:
            print("• Conduce con precaución, visibilidad reducida")
    
    def mostrar_pronostico(self, dias=7, ubicacion="Ciudad"):
        """Muestra el pronóstico extendido"""
        pronostico = self.generar_pronostico(dias, ubicacion)
        
        print(f"\n{'='*80}")
        print(f"PRONÓSTICO EXTENDIDO - {ubicacion.upper()} ({dias} días)")
        print(f"{'='*80}")
        
        for dia in pronostico:
            print(f"\n📅 {dia['fecha']} ({dia['dia_semana']})")
            print(f"🌡️  {dia['temp_min']}°C - {dia['temp_max']}°C")
            print(f"🌤️  {dia['clima_predominante']}")
            
            if dia['precipitacion_total'] > 0:
                print(f"🌧️  Precipitación: {dia['precipitacion_total']:.1f} mm")
            
            print("   Detalle por horario:")
            print(f"   Mañana: {dia['detalle']['mañana']['temperatura']}°C, {dia['detalle']['mañana']['tipo_clima']}")
            print(f"   Tarde:  {dia['detalle']['tarde']['temperatura']}°C, {dia['detalle']['tarde']['tipo_clima']}")
            print(f"   Noche:  {dia['detalle']['noche']['temperatura']}°C, {dia['detalle']['noche']['tipo_clima']}")
        
        return pronostico
    
    def agregar_al_historial(self, reporte):
        """Agrega un reporte al historial"""
        self.historial.append(reporte)
        # Mantener solo los últimos 100 registros
        if len(self.historial) > 100:
            self.historial = self.historial[-100:]
        self.guardar_historial()
    
    def mostrar_historial(self, limite=10):
        """Muestra el historial de simulaciones"""
        if not self.historial:
            print("No hay registros en el historial.")
            return
        
        print(f"\n=== HISTORIAL DE CLIMA (últimos {limite}) ===")
        for reporte in self.historial[-limite:]:
            print(f"{reporte['fecha']} {reporte['hora']} - {reporte['ubicacion']}")
            print(f"  {reporte['tipo_clima']}, {reporte['temperatura']}°C")

def main():
    simulador = SimuladorClima()
    
    while True:
        print("\n=== SIMULADOR DE CLIMA ===")
        print("1. Ver clima actual")
        print("2. Generar pronóstico extendido")
        print("3. Simular clima para fecha específica")
        print("4. Comparar climas de diferentes ubicaciones")
        print("5. Ver historial")
        print("6. Salir")
        
        opcion = input("\nSelecciona una opción (1-6): ").strip()
        
        if opcion == "1":
            ubicacion = input("Ubicación (opcional): ").strip() or "Ciudad"
            clima = simulador.mostrar_clima_actual(ubicacion)
            simulador.agregar_al_historial(clima)
        
        elif opcion == "2":
            ubicacion = input("Ubicación (opcional): ").strip() or "Ciudad"
            try:
                dias = int(input("Número de días (1-14, default: 7): ") or "7")
                dias = max(1, min(14, dias))
            except ValueError:
                dias = 7
            
            simulador.mostrar_pronostico(dias, ubicacion)
        
        elif opcion == "3":
            try:
                fecha_str = input("Fecha (YYYY-MM-DD): ").strip()
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
                ubicacion = input("Ubicación (opcional): ").strip() or "Ciudad"
                
                clima = simulador.generar_clima_completo(fecha, ubicacion)
                
                print(f"\n=== CLIMA SIMULADO ===")
                print(f"Fecha: {clima['fecha']}")
                print(f"Ubicación: {clima['ubicacion']}")
                print(f"Tipo: {clima['tipo_clima']}")
                print(f"Temperatura: {clima['temperatura']}°C")
                print(f"Humedad: {clima['humedad']}%")
                print(f"Viento: {clima['viento']['velocidad']} km/h {clima['viento']['direccion']}")
                
                simulador.agregar_al_historial(clima)
                
            except ValueError:
                print("Formato de fecha inválido. Use YYYY-MM-DD")
        
        elif opcion == "4":
            ubicaciones = []
            print("Ingresa hasta 3 ubicaciones para comparar:")
            for i in range(3):
                ubicacion = input(f"Ubicación {i+1} (Enter para terminar): ").strip()
                if not ubicacion:
                    break
                ubicaciones.append(ubicacion)
            
            if len(ubicaciones) < 2:
                print("Se necesitan al menos 2 ubicaciones para comparar.")
                continue
            
            print(f"\n=== COMPARACIÓN DE CLIMAS ===")
            climas = []
            for ubicacion in ubicaciones:
                clima = simulador.generar_clima_completo(ubicacion=ubicacion)
                climas.append(clima)
                simulador.agregar_al_historial(clima)
            
            # Mostrar comparación
            print(f"{'Ubicación':<15} {'Clima':<20} {'Temp':<8} {'Humedad':<10} {'Viento':<15}")
            print("-" * 70)
            
            for clima in climas:
                print(f"{clima['ubicacion']:<15} {clima['tipo_clima']:<20} {clima['temperatura']}°C{'':<3} {clima['humedad']}%{'':<6} {clima['viento']['velocidad']} km/h")
        
        elif opcion == "5":
            try:
                limite = int(input("Número de registros a mostrar (default: 10): ") or "10")
                simulador.mostrar_historial(limite)
            except ValueError:
                simulador.mostrar_historial()
        
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
