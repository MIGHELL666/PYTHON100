"""
Proyecto 59: Calculadora Financiera
Herramientas para cálculos financieros: interés, préstamos, inversiones, etc.
"""

import json
import os
from datetime import datetime, timedelta
import math

class CalculadoraFinanciera:
    def __init__(self):
        self.historial_archivo = "historial_financiero.json"
        self.historial = self.cargar_historial()
    
    def cargar_historial(self):
        """Carga el historial de cálculos"""
        try:
            with open(self.historial_archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def guardar_historial(self):
        """Guarda el historial de cálculos"""
        try:
            with open(self.historial_archivo, 'w', encoding='utf-8') as f:
                json.dump(self.historial, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    
    def interes_simple(self, capital, tasa_anual, tiempo_años):
        """Calcula interés simple"""
        interes = capital * (tasa_anual / 100) * tiempo_años
        monto_final = capital + interes
        
        return {
            'capital_inicial': capital,
            'tasa_anual': tasa_anual,
            'tiempo_años': tiempo_años,
            'interes_ganado': round(interes, 2),
            'monto_final': round(monto_final, 2)
        }
    
    def interes_compuesto(self, capital, tasa_anual, tiempo_años, frecuencia_capitalizacion=1):
        """Calcula interés compuesto"""
        # frecuencia_capitalizacion: 1=anual, 2=semestral, 4=trimestral, 12=mensual, 365=diario
        tasa_periodo = tasa_anual / 100 / frecuencia_capitalizacion
        num_periodos = frecuencia_capitalizacion * tiempo_años
        
        monto_final = capital * (1 + tasa_periodo) ** num_periodos
        interes_ganado = monto_final - capital
        
        return {
            'capital_inicial': capital,
            'tasa_anual': tasa_anual,
            'tiempo_años': tiempo_años,
            'frecuencia_capitalizacion': frecuencia_capitalizacion,
            'interes_ganado': round(interes_ganado, 2),
            'monto_final': round(monto_final, 2)
        }
    
    def calcular_prestamo(self, monto_prestamo, tasa_anual, años):
        """Calcula pagos de préstamo (sistema francés)"""
        tasa_mensual = tasa_anual / 100 / 12
        num_pagos = años * 12
        
        if tasa_mensual == 0:
            pago_mensual = monto_prestamo / num_pagos
        else:
            pago_mensual = monto_prestamo * (tasa_mensual * (1 + tasa_mensual) ** num_pagos) / \
                          ((1 + tasa_mensual) ** num_pagos - 1)
        
        total_pagado = pago_mensual * num_pagos
        total_intereses = total_pagado - monto_prestamo
        
        # Generar tabla de amortización (primeros 12 meses)
        tabla_amortizacion = []
        saldo_pendiente = monto_prestamo
        
        for mes in range(min(12, num_pagos)):
            interes_mes = saldo_pendiente * tasa_mensual
            capital_mes = pago_mensual - interes_mes
            saldo_pendiente -= capital_mes
            
            tabla_amortizacion.append({
                'mes': mes + 1,
                'pago_mensual': round(pago_mensual, 2),
                'interes': round(interes_mes, 2),
                'capital': round(capital_mes, 2),
                'saldo_pendiente': round(max(0, saldo_pendiente), 2)
            })
        
        return {
            'monto_prestamo': monto_prestamo,
            'tasa_anual': tasa_anual,
            'años': años,
            'pago_mensual': round(pago_mensual, 2),
            'total_pagado': round(total_pagado, 2),
            'total_intereses': round(total_intereses, 2),
            'tabla_amortizacion': tabla_amortizacion
        }
    
    def valor_presente_neto(self, inversion_inicial, flujos_efectivo,
