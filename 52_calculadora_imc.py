"""
Proyecto 52: Calculadora de IMC (Índice de Masa Corporal)
Calcula el IMC y proporciona recomendaciones de salud.
"""

import json
from datetime import datetime

class CalculadoraIMC:
    def __init__(self):
        self.historial_archivo = "historial_imc.json"
        self.historial = self.cargar_historial()
    
    def cargar_historial(self):
        """Carga el historial de cálculos IMC"""
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
    
    def calcular_imc(self, peso, altura):
        """Calcula el IMC"""
        return peso / (altura ** 2)
    
    def clasificar_imc(self, imc):
        """Clasifica el IMC según los estándares de la OMS"""
        if imc < 18.5:
            return "Bajo peso", "Puede indicar desnutrición. Consulta a un profesional de la salud."
        elif 18.5 <= imc < 25:
            return "Peso normal", "¡Excelente! Mantén un estilo de vida saludable."
        elif 25 <= imc < 30:
            return "Sobrepeso", "Considera una dieta balanceada y ejercicio regular."
        elif 30 <= imc < 35:
            return "Obesidad grado I", "Es recomendable consultar a un profesional de la salud."
        elif 35 <= imc < 40:
            return "Obesidad grado II", "Es importante buscar ayuda médica profesional."
        else:
            return "Obesidad grado III", "Busca atención médica inmediata."
    
    def calcular_peso_ideal(self, altura):
        """Calcula el rango de peso ideal para una altura"""
        peso_min = 18.5 * (altura ** 2)
        peso_max = 24.9 * (altura ** 2)
        return peso_min, peso_max
    
    def obtener_recomendaciones(self, categoria):
        """Proporciona recomendaciones específicas según la categoría"""
        recomendaciones = {
            "Bajo peso": [
                "Aumenta la ingesta calórica con alimentos nutritivos",
                "Incluye proteínas en cada comida",
                "Considera suplementos vitamínicos",
                "Consulta a un nutricionista"
            ],
            "Peso normal": [
                "Mantén una dieta equilibrada",
                "Realiza ejercicio regularmente",
                "Mantén buenos hábitos de sueño",
                "Hidrátate adecuadamente"
            ],
            "Sobrepeso": [
                "Reduce las porciones gradualmente",
                "Aumenta la actividad física",
                "Limita alimentos procesados",
                "Incluye más frutas y verduras"
            ],
            "Obesidad grado I": [
                "Consulta a un profesional de la salud",
                "Planifica un programa de pérdida de peso",
                "Considera terapia nutricional",
                "Aumenta la actividad física gradualmente"
            ],
            "Obesidad grado II": [
                "Busca ayuda médica profesional",
                "Considera programas supervisados de pérdida de peso",
                "Evalúa opciones de tratamiento médico",
                "Incluye apoyo psicológico si es necesario"
            ],
            "Obesidad grado III": [
                "Busca atención médica inmediata",
                "Considera opciones de cirugía bariátrica",
                "Requiere supervisión médica constante",
                "Programa integral de tratamiento"
            ]
        }
        return recomendaciones.get(categoria, [])
    
    def guardar_calculo(self, nombre, peso, altura, imc, categoria):
        """Guarda un cálculo en el historial"""
        registro = {
            "nombre": nombre,
            "peso": peso,
            "altura": altura,
            "imc": round(imc, 2),
            "categoria": categoria,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.historial.append(registro)
        self.guardar_historial()
    
    def mostrar_historial(self, nombre=None):
        """Muestra el historial de cálculos"""
        if not self.historial:
            print("No hay registros en el historial.")
            return
        
        registros = self.historial
        if nombre:
            registros = [r for r in self.historial if r['nombre'].lower() == nombre.lower()]
            if not registros:
                print(f"No se encontraron registros para {nombre}.")
                return
        
        print("\n=== HISTORIAL DE CÁLCULOS IMC ===")
        for registro in registros[-10:]:  # Mostrar últimos 10
            print(f"\nNombre: {registro['nombre']}")
            print(f"Fecha: {registro['fecha']}")
            print(f"Peso: {registro['peso']} kg")
            print(f"Altura: {registro['altura']} m")
            print(f"IMC: {registro['imc']}")
            print(f"Categoría: {registro['categoria']}")
            print("-" * 40)
    
    def realizar_calculo_completo(self):
        """Realiza un cálculo completo de IMC con recomendaciones"""
        print("\n=== CALCULADORA DE IMC ===")
        
        # Obtener datos del usuario
        nombre = input("Nombre (opcional): ").strip() or "Usuario"
        
        try:
            peso = float(input("Ingresa tu peso en kg: "))
            if peso <= 0:
                print("El peso debe ser mayor que 0.")
                return
            
            altura = float(input("Ingresa tu altura en metros (ej: 1.75): "))
            if altura <= 0:
                print("La altura debe ser mayor que 0.")
                return
            
        except ValueError:
            print("Por favor, ingresa valores numéricos válidos.")
            return
        
        # Calcular IMC
        imc = self.calcular_imc(peso, altura)
        categoria, descripcion = self.clasificar_imc(imc)
        
        # Mostrar resultados
        print(f"\n=== RESULTADOS PARA {nombre.upper()} ===")
        print(f"Peso: {peso} kg")
        print(f"Altura: {altura} m")
        print(f"IMC: {imc:.2f}")
        print(f"Categoría: {categoria}")
        print(f"Descripción: {descripcion}")
        
        # Peso ideal
        peso_min, peso_max = self.calcular_peso_ideal(altura)
        print(f"\nPeso ideal para tu altura: {peso_min:.1f} - {peso_max:.1f} kg")
        
        # Recomendaciones
        recomendaciones = self.obtener_recomendaciones(categoria)
        if recomendaciones:
            print(f"\n=== RECOMENDACIONES ===")
            for i, rec in enumerate(recomendaciones, 1):
                print(f"{i}. {rec}")
        
        # Guardar en historial
        self.guardar_calculo(nombre, peso, altura, imc, categoria)
        print(f"\nCálculo guardado en el historial.")

def main():
    calculadora = CalculadoraIMC()
    
    while True:
        print("\n=== CALCULADORA DE IMC ===")
        print("1. Calcular IMC")
        print("2. Ver historial completo")
        print("3. Ver historial por nombre")
        print("4. Información sobre IMC")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            calculadora.realizar_calculo_completo()
        
        elif opcion == "2":
            calculadora.mostrar_historial()
        
        elif opcion == "3":
            nombre = input("Ingresa el nombre: ").strip()
            if nombre:
                calculadora.mostrar_historial(nombre)
        
        elif opcion == "4":
            print("\n=== INFORMACIÓN SOBRE IMC ===")
            print("El Índice de Masa Corporal (IMC) es una medida que relaciona")
            print("el peso y la altura para evaluar si una persona tiene un peso saludable.")
            print("\nCategorías según la OMS:")
            print("• Bajo peso: IMC < 18.5")
            print("• Peso normal: IMC 18.5 - 24.9")
            print("• Sobrepeso: IMC 25.0 - 29.9")
            print("• Obesidad grado I: IMC 30.0 - 34.9")
            print("• Obesidad grado II: IMC 35.0 - 39.9")
            print("• Obesidad grado III: IMC ≥ 40.0")
            print("\nNota: El IMC es una herramienta de evaluación general.")
            print("Consulta siempre a un profesional de la salud.")
        
        elif opcion == "5":
            print("¡Cuida tu salud!")
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
