"""
Proyecto 50: Juego del Ahorcado
"""

import random

class JuegoAhorcado:
    """Clase para manejar el juego del ahorcado"""
    
    def __init__(self):
        self.palabras_por_categoria = {
            'animales': ['perro', 'gato', 'elefante', 'jirafa', 'leon', 'tigre', 'oso', 'lobo', 'zorro', 'conejo'],
            'frutas': ['manzana', 'banana', 'naranja', 'uva', 'fresa', 'piña', 'mango', 'pera', 'durazno', 'sandia'],
            'paises': ['argentina', 'brasil', 'chile', 'colombia', 'mexico', 'españa', 'francia', 'italia', 'japon', 'china'],
            'colores': ['rojo', 'azul', 'verde', 'amarillo', 'morado', 'naranja', 'rosa', 'negro', 'blanco', 'gris'],
            'deportes': ['futbol', 'basquet', 'tenis', 'natacion', 'atletismo', 'boxeo', 'golf', 'hockey', 'rugby', 'voleibol'],
            'profesiones': ['doctor', 'maestro', 'ingeniero', 'abogado', 'chef', 'piloto', 'artista', 'musico', 'escritor', 'programador']
        }
        
        self.dibujos_ahorcado = [
            """
   +---+
   |   |
       |
       |
       |
       |
=========
""",
            """
   +---+
   |   |
   O   |
       |
       |
       |
=========
""",
            """
   +---+
   |   |
   O   |
   |   |
       |
       |
=========
""",
            """
   +---+
   |   |
   O   |
  /|   |
       |
       |
=========
""",
            """
   +---+
   |   |
   O   |
  /|\\  |
       |
       |
=========
""",
            """
   +---+
   |   |
   O   |
  /|\\  |
  /    |
       |
=========
""",
            """
   +---+
   |   |
   O   |
  /|\\  |
  / \\  |
       |
=========
"""
        ]
        
        self.reiniciar_juego()
    
    def reiniciar_juego(self):
        """Reinicia el estado del juego"""
        self.palabra_secreta = ""
        self.categoria = ""
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.intentos_restantes = 6
        self.juego_terminado = False
        self.ganado = False
    
    def seleccionar_palabra(self, categoria=None, palabra_personalizada=None):
        """Selecciona una palabra para el juego"""
        if palabra_personalizada:
            self.palabra_secreta = palabra_personalizada.lower()
            self.categoria = "personalizada"
        elif categoria and categoria in self.palabras_por_categoria:
            self.palabra_secreta = random.choice(self.palabras_por_categoria[categoria])
            self.categoria = categoria
        else:
            # Seleccionar categoría aleatoria
            self.categoria = random.choice(list(self.palabras_por_categoria.keys()))
            self.palabra_secreta = random.choice(self.palabras_por_categoria[self.categoria])
    
    def obtener_palabra_mostrada(self):
        """Devuelve la palabra con las letras adivinadas y guiones para las no adivinadas"""
        palabra_mostrada = ""
        for letra in self.palabra_secreta:
            if letra in self.letras_adivinadas:
                palabra_mostrada += letra + " "
            else:
                palabra_mostrada += "_ "
        return palabra_mostrada.strip()
    
    def adivinar_letra(self, letra):
        """Procesa un intento de adivinar una letra"""
        letra = letra.lower()
        
        # Validar entrada
        if len(letra) != 1 or not letra.isalpha():
            return "Error: Ingresa solo una letra"
        
        if letra in self.letras_adivinadas or letra in self.letras_incorrectas:
            return f"Ya intentaste la letra '{letra}'"
        
        # Procesar intento
        if letra in self.palabra_secreta:
            self.letras_adivinadas.add(letra)
            mensaje = f"¡Correcto! La letra '{letra}' está en la palabra"
            
            # Verificar si ganó
            if all(letra in self.letras_adivinadas for letra in self.palabra_secreta):
                self.juego_terminado = True
                self.ganado = True
                mensaje += "\n🎉 ¡FELICIDADES! ¡Adivinaste la palabra!"
        else:
            self.letras_incorrectas.add(letra)
            self.intentos_restantes -= 1
            mensaje = f"❌ La letra '{letra}' no está en la palabra"
            
            # Verificar si perdió
            if self.intentos_restantes == 0:
                self.juego_terminado = True
                self.ganado = False
                mensaje += f"\n💀 ¡Perdiste! La palabra era: '{self.palabra_secreta}'"
        
        return mensaje
    
    def adivinar_palabra_completa(self, palabra):
        """Permite adivinar la palabra completa"""
        palabra = palabra.lower().strip()
        
        if palabra == self.palabra_secreta:
            self.juego_terminado = True
            self.ganado = True
            return "🎉 ¡CORRECTO! ¡Adivinaste la palabra completa!"
        else:
            self.intentos_restantes -= 1
            if self.intentos_restantes == 0:
                self.juego_terminado = True
                self.ganado = False
                return f"❌ Palabra incorrecta. 💀 ¡Perdiste! La palabra era: '{self.palabra_secreta}'"
            else:
                return f"❌ Palabra incorrecta. Te quedan {self.intentos_restantes} intentos"
    
    def obtener_estado_juego(self):
        """Devuelve el estado actual del juego"""
        return {
            'palabra_mostrada': self.obtener_palabra_mostrada(),
            'categoria': self.categoria,
            'letras_adivinadas': sorted(list(self.letras_adivinadas)),
            'letras_incorrectas': sorted(list(self.letras_incorrectas)),
            'intentos_restantes': self.intentos_restantes,
            'dibujo': self.dibujos_ahorcado[6 - self.intentos_restantes],
            'juego_terminado': self.juego_terminado,
            'ganado': self.ganado
        }
    
    def obtener_pista(self):
        """Proporciona una pista sobre la palabra"""
        if self.categoria == "personalizada":
            return f"La palabra tiene {len(self.palabra_secreta)} letras"
        
        pistas = {
            'animales': "Es un ser vivo que puede moverse y respirar",
            'frutas': "Es algo dulce que crece en plantas y es bueno para la salud",
            'paises': "Es un territorio con gobierno propio en el mundo",
            'colores': "Es algo que puedes ver y que hace que las cosas se vean diferentes",
            'deportes': "Es una actividad física que se practica siguiendo reglas",
            'profesiones': "Es un trabajo que las personas hacen para ganarse la vida"
        }
        
        pista_categoria = pistas.get(self.categoria, "No hay pista disponible")
        return f"Categoría: {self.categoria.title()}\nPista: {pista_categoria}\nLongitud: {len(self.palabra_secreta)} letras"

def mostrar_estadisticas_juego(victorias, derrotas, palabras_adivinadas):
    """Muestra estadísticas del jugador"""
    total_juegos = victorias + derrotas
    
    if total_juegos == 0:
        print("No has jugado ninguna partida aún")
        return
    
    porcentaje_victorias = (victorias / total_juegos) * 100
    
    print(f"\n=== ESTADÍSTICAS ===")
    print(f"Partidas jugadas: {total_juegos}")
    print(f"Victorias: {victorias}")
    print(f"Derrotas: {derrotas}")
    print(f"Porcentaje de victorias: {porcentaje_victorias:.1f}%")
    
    if palabras_adivinadas:
        print(f"\nPalabras adivinadas ({len(palabras_adivinadas)}):")
        for i, palabra in enumerate(palabras_adivinadas[-10:], 1):  # Últimas 10
            print(f"  {i}. {palabra}")
        
        if len(palabras_adivinadas) > 10:
            print(f"  ... y {len(palabras_adivinadas) - 10} más")

def juego_multijugador():
    """Modo multijugador donde un jugador ingresa la palabra"""
    print("=== MODO MULTIJUGADOR ===")
    print("Un jugador ingresará una palabra secreta para que el otro adivine")
    
    # Limpiar pantalla (simulado)
    print("\n" * 3)
    print("Jugador 1: Ingresa la palabra secreta")
    print("(Jugador 2: ¡No mires!)")
    
    palabra_secreta = input("Palabra secreta: ").strip()
    
    if not palabra_secreta or not palabra_secreta.isalpha():
        print("❌ Error: La palabra debe contener solo letras")
        return
    
    # Limpiar pantalla
    print("\n" * 20)
    print("¡Palabra ingresada! Jugador 2, es tu turno de adivinar")
    
    juego = JuegoAhorcado()
    juego.seleccionar_palabra(palabra_personalizada=palabra_secreta)
    
    return juego

def main():
    print("🎮 ¡Bienvenido al Juego del Ahorcado! 🎮")
    
    # Estadísticas del jugador
    victorias = 0
    derrotas = 0
    palabras_adivinadas = []
    
    while True:
        print("\n" + "="*50)
        print("1. Jugar (categoría aleatoria)")
        print("2. Jugar (elegir categoría)")
        print("3. Jugar (palabra personalizada)")
        print("4. Modo multijugador")
        print("5. Ver estadísticas")
        print("6. Ver categorías disponibles")
        print("7. Salir")
        
        try:
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == '1':
                # Juego con categoría aleatoria
                juego = JuegoAhorcado()
                juego.seleccionar_palabra()
                
            elif opcion == '2':
                # Juego eligiendo categoría
                juego = JuegoAhorcado()
                
                print("\nCategorías disponibles:")
                categorias = list(juego.palabras_por_categoria.keys())
                for i, cat in enumerate(categorias, 1):
                    print(f"{i}. {cat.title()}")
                
                try:
                    seleccion = int(input("Selecciona una categoría: ")) - 1
                    if 0 <= seleccion < len(categorias):
                        categoria_elegida = categorias[seleccion]
                        juego.seleccionar_palabra(categoria_elegida)
                    else:
                        print("❌ Selección no válida")
                        continue
                except ValueError:
                    print("❌ Ingresa un número válido")
                    continue
            
            elif opcion == '3':
                # Juego con palabra personalizada
                palabra = input("Ingresa una palabra personalizada: ").strip()
                if not palabra or not palabra.isalpha():
                    print("❌ Error: La palabra debe contener solo letras")
                    continue
                
                juego = JuegoAhorcado()
                juego.seleccionar_palabra(palabra_personalizada=palabra)
            
            elif opcion == '4':
                # Modo multijugador
                juego = juego_multijugador()
                if not juego:
                    continue
            
            elif opcion == '5':
                # Ver estadísticas
                mostrar_estadisticas_juego(victorias, derrotas, palabras_adivinadas)
                continue
            
            elif opcion == '6':
                # Ver categorías
                juego_temp = JuegoAhorcado()
                print("\n=== CATEGORÍAS DISPONIBLES ===")
                for categoria, palabras in juego_temp.palabras_por_categoria.items():
                    print(f"\n{categoria.title()} ({len(palabras)} palabras):")
                    print(f"  Ejemplos: {', '.join(palabras[:5])}")
                continue
            
            elif opcion == '7':
                print("¡Gracias por jugar! 👋")
                break
            
            else:
                print("❌ Opción no válida")
                continue
            
            # Iniciar el juego
            print(f"\n🎯 ¡Comienza el juego!")
            estado = juego.obtener_estado_juego()
            print(f"Categoría: {estado['categoria'].title()}")
            
            # Bucle principal del juego
            while not juego.juego_terminado:
                estado = juego.obtener_estado_juego()
                
                # Mostrar estado actual
                print("\n" + "="*40)
                print(estado['dibujo'])
                print(f"Palabra: {estado['palabra_mostrada']}")
                print(f"Intentos restantes: {estado['intentos_restantes']}")
                
                if estado['letras_adivinadas']:
                    print(f"Letras correctas: {', '.join(estado['letras_adivinadas'])}")
                
                if estado['letras_incorrectas']:
                    print(f"Letras incorrectas: {', '.join(estado['letras_incorrectas'])}")
                
                # Opciones del jugador
                print("\nOpciones:")
                print("- Ingresa una letra")
                print("- Escribe 'palabra' para adivinar la palabra completa")
                print("- Escribe 'pista' para obtener una pista")
                print("- Escribe 'salir' para abandonar el juego")
                
                entrada = input("\nTu elección: ").strip().lower()
                
                if entrada == 'salir':
                    print("Abandonaste el juego")
                    break
                elif entrada == 'pista':
                    print(f"\n💡 {juego.obtener_pista()}")
                elif entrada == 'palabra':
                    palabra_completa = input("Ingresa la palabra completa: ").strip()
                    if palabra_completa:
                        mensaje = juego.adivinar_palabra_completa(palabra_completa)
                        print(f"\n{mensaje}")
                elif len(entrada) == 1 and entrada.isalpha():
                    mensaje = juego.adivinar_letra(entrada)
                    print(f"\n{mensaje}")
                else:
                    print("❌ Entrada no válida. Ingresa una letra, 'palabra', 'pista' o 'salir'")
            
            # Resultado final
            if juego.juego_terminado:
                estado_final = juego.obtener_estado_juego()
                
                if estado_final['ganado']:
                    victorias += 1
                    palabras_adivinadas.append(juego.palabra_secreta)
                    print(f"\n🎉 ¡VICTORIA! 🎉")
                else:
                    derrotas += 1
                    print(f"\n💀 Derrota 💀")
                    print(estado_final['dibujo'])
                
                print(f"La palabra era: '{juego.palabra_secreta.upper()}'")
                
                # Mostrar estadísticas rápidas
                total = victorias + derrotas
                if total > 0:
                    porcentaje = (victorias / total) * 100
                    print(f"Tu récord: {victorias}W - {derrotas}L ({porcentaje:.1f}%)")
        
        except KeyboardInterrupt:
            print("\n¡Hasta luego! 👋")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
