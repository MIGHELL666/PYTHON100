import random
import time
import os
import sys
from enum import Enum

class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

class SnakeGame:
    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.reset_game()
        self.high_score = self.load_high_score()
        
    def reset_game(self):
        """Reiniciar el juego"""
        # Posición inicial de la serpiente (centro del tablero)
        start_row = self.height // 2
        start_col = self.width // 2
        
        self.snake = [(start_row, start_col)]
        self.direction = Direction.RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.paused = False
        
    def generate_food(self):
        """Generar comida en posición aleatoria"""
        while True:
            food_pos = (
                random.randint(0, self.height - 1),
                random.randint(0, self.width - 1)
            )
            if food_pos not in self.snake:
                return food_pos
    
    def move_snake(self):
        """Mover la serpiente"""
        if self.game_over or self.paused:
            return
            
        head = self.snake[0]
        new_head = (
            head[0] + self.direction.value[0],
            head[1] + self.direction.value[1]
        )
        
        # Verificar colisiones con paredes
        if (new_head[0] < 0 or new_head[0] >= self.height or
            new_head[1] < 0 or new_head[1] >= self.width):
            self.game_over = True
            return
        
        # Verificar colisión con el cuerpo
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Agregar nueva cabeza
        self.snake.insert(0, new_head)
        
        # Verificar si comió la comida
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            # Remover cola si no comió
            self.snake.pop()
    
    def change_direction(self, new_direction):
        """Cambiar dirección de la serpiente"""
        # No permitir movimiento en dirección opuesta
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction
    
    def draw_board(self):
        """Dibujar el tablero del juego"""
        # Limpiar pantalla
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("🐍 SNAKE GAME 🐍")
        print(f"Puntuación: {self.score} | Récord: {self.high_score}")
        
        if self.paused:
            print("⏸️  JUEGO PAUSADO")
        
        print("+" + "-" * (self.width * 2) + "+")
        
        for row in range(self.height):
            print("|", end="")
            for col in range(self.width):
                pos = (row, col)
                
                if pos == self.snake[0]:  # Cabeza
                    print("🟢", end="")
                elif pos in self.snake:   # Cuerpo
                    print("🟩", end="")
                elif pos == self.food:    # Comida
                    print("🍎", end="")
                else:                     # Espacio vacío
                    print("  ", end="")
            print("|")
        
        print("+" + "-" * (self.width * 2) + "+")
        
        if self.game_over:
            print("💀 GAME OVER! 💀")
            if self.score > self.high_score:
                print("🎉 ¡NUEVO RÉCORD! 🎉")
        
        print("\nControles:")
        print("W/↑ - Arriba | S/↓ - Abajo | A/← - Izquierda | D/→ - Derecha")
        print("P - Pausar | Q - Salir | R - Reiniciar")
    
    def get_input(self):
        """Obtener entrada del usuario (simulado para consola)"""
        # En un juego real, usarías una librería como keyboard o pygame
        # Para este ejemplo, usaremos input() con timeout simulado
        print("Ingresa comando (w/a/s/d/p/q/r): ", end="", flush=True)
        
        # Simular timeout con threading
        import threading
        import queue
        
        def input_thread(q):
            try:
                q.put(input().lower().strip())
            except:
                q.put('')
        
        q = queue.Queue()
        t = threading.Thread(target=input_thread, args=(q,))
        t.daemon = True
        t.start()
        t.join(timeout=0.5)  # Timeout de 0.5 segundos
        
        try:
            return q.get_nowait()
        except queue.Empty:
            return ''
    
    def load_high_score(self):
        """Cargar puntuación más alta"""
        try:
            with open('snake_high_score.txt', 'r') as f:
                return int(f.read().strip())
        except:
            return 0
    
    def save_high_score(self):
        """Guardar puntuación más alta"""
        try:
            with open('snake_high_score.txt', 'w') as f:
                f.write(str(self.high_score))
        except:
            pass
    
    def play(self):
        """Bucle principal del juego"""
        print("🐍 ¡Bienvenido a Snake Game! 🐍")
        print("Presiona Enter para comenzar...")
        input()
        
        while True:
            self.draw_board()
            
            if self.game_over:
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                
                print("\n¿Jugar de nuevo? (s/n): ", end="")
                if input().lower().startswith('s'):
                    self.reset_game()
                    continue
                else:
                    break
            
            # Obtener entrada del usuario
            user_input = self.get_input()
            
            if user_input == 'q':
                break
            elif user_input == 'r':
                self.reset_game()
                continue
            elif user_input == 'p':
                self.paused = not self.paused
                continue
            elif user_input in ['w', '↑']:
                self.change_direction(Direction.UP)
            elif user_input in ['s', '↓']:
                self.change_direction(Direction.DOWN)
            elif user_input in ['a', '←']:
                self.change_direction(Direction.LEFT)
            elif user_input in ['d', '→']:
                self.change_direction(Direction.RIGHT)
            
            # Mover serpiente
            self.move_snake()
            
            # Pequeña pausa para controlar velocidad
            time.sleep(0.3)
        
        print("¡Gracias por jugar Snake! 🐍")

class SnakeGameAdvanced:
    """Versión avanzada con más características"""
    
    def __init__(self, width=25, height=20):
        self.width = width
        self.height = height
        self.difficulty = 'normal'
        self.power_ups = []
        self.obstacles = []
        self.reset_game()
        self.stats = self.load_stats()
    
    def reset_game(self):
        """Reiniciar juego avanzado"""
        start_row = self.height // 2
        start_col = self.width // 2
        
        self.snake = [(start_row, start_col)]
        self.direction = Direction.RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.speed = self.get_speed()
        self.power_ups = []
        self.obstacles = []
        
        # Generar obstáculos según el nivel
        self.generate_obstacles()
        
        # Generar power-ups ocasionalmente
        if random.random() < 0.3:
            self.generate_power_up()
    
    def get_speed(self):
        """Obtener velocidad según dificultad y nivel"""
        base_speeds = {
            'easy': 0.4,
            'normal': 0.3,
            'hard': 0.2
        }
        
        base_speed = base_speeds.get(self.difficulty, 0.3)
        # Aumentar velocidad cada 5 niveles
        speed_increase = (self.level - 1) // 5 * 0.05
        return max(0.1, base_speed - speed_increase)
    
    def generate_obstacles(self):
        """Generar obstáculos según el nivel"""
        num_obstacles = min(self.level // 3, 10)
        
        for _ in range(num_obstacles):
            while True:
                obstacle_pos = (
                    random.randint(1, self.height - 2),
                    random.randint(1, self.width - 2)
                )
                
                # No colocar obstáculos cerca de la serpiente o comida
                if (obstacle_pos not in self.snake and 
                    obstacle_pos != self.food and
                    obstacle_pos not in self.obstacles):
                    
                    # Verificar que no esté muy cerca de la serpiente inicial
                    snake_head = self.snake[0]
                    distance = abs(obstacle_pos[0] - snake_head[0]) + abs(obstacle_pos[1] - snake_head[1])
                    
                    if distance > 3:
                        self.obstacles.append(obstacle_pos)
                        break
    
    def generate_power_up(self):
        """Generar power-up"""
        power_up_types = ['speed_boost', 'score_multiplier', 'shrink', 'extra_life']
        
        while True:
            power_up_pos = (
                random.randint(0, self.height - 1),
                random.randint(0, self.width - 1)
            )
            
            if (power_up_pos not in self.snake and 
                power_up_pos != self.food and
                power_up_pos not in self.obstacles and
                power_up_pos not in [pu['pos'] for pu in self.power_ups]):
                
                power_up = {
                    'pos': power_up_pos,
                    'type': random.choice(power_up_types),
                    'duration': 100  # Duración en movimientos
                }
                self.power_ups.append(power_up)
                break
    
    def generate_food(self):
        """Generar comida evitando obstáculos"""
        while True:
            food_pos = (
                random.randint(0, self.height - 1),
                random.randint(0, self.width - 1)
            )
            
            if (food_pos not in self.snake and 
                food_pos not in self.obstacles and
                food_pos not in [pu['pos'] for pu in self.power_ups]):
                return food_pos
    
    def move_snake(self):
        """Mover serpiente con lógica avanzada"""
        if self.game_over or self.paused:
            return
            
        head = self.snake[0]
        new_head = (
            head[0] + self.direction.value[0],
            head[1] + self.direction.value[1]
        )
        
        # Verificar colisiones con paredes
        if (new_head[0] < 0 or new_head[0] >= self.height or
            new_head[1] < 0 or new_head[1] >= self.width):
            self.game_over = True
            return
        
        # Verificar colisión con obstáculos
        if new_head in self.obstacles:
            self.game_over = True
            return
        
        # Verificar colisión con el cuerpo
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Agregar nueva cabeza
        self.snake.insert(0, new_head)
        
        # Verificar si comió la comida
        if new_head == self.food:
            points = 10 * self.level
            self.score += points
            self.food = self.generate_food()
            
            # Subir de nivel cada 100 puntos
            new_level = (self.score // 100) + 1
            if new_level > self.level:
                self.level = new_level
                self.speed = self.get_speed()
                self.generate_obstacles()
                
                # Generar power-up al subir de nivel
                if random.random() < 0.5:
                    self.generate_power_up()
        else:
            # Remover cola si no comió
            self.snake.pop()
        
        # Verificar power-ups
        for power_up in self.power_ups[:]:
            if new_head == power_up['pos']:
                self.apply_power_up(power_up)
                self.power_ups.remove(power_up)
        
        # Reducir duración de power-ups activos
        for power_up in self.power_ups[:]:
            power_up['duration'] -= 1
            if power_up['duration'] <= 0:
                self.power_ups.remove(power_up)
    
    def apply_power_up(self, power_up):
        """Aplicar efecto de power-up"""
        if power_up['type'] == 'speed_boost':
            self.speed = max(0.05, self.speed - 0.1)
        elif power_up['type'] == 'score_multiplier':
            self.score += 50
        elif power_up['type'] == 'shrink':
            if len(self.snake) > 1:
                self.snake.pop()
        elif power_up['type'] == 'extra_life':
            # En este caso, simplemente dar puntos extra
            self.score += 100
    
    def draw_board_advanced(self):
        """Dibujar tablero avanzado"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("🐍 SNAKE GAME ADVANCED 🐍")
        print(f"Puntuación: {self.score} | Nivel: {self.level} | Dificultad: {self.difficulty.title()}")
        print(f"Velocidad: {1/self.speed:.1f} | Power-ups activos: {len(self.power_ups)}")
        
        if self.paused:
            print("⏸️  JUEGO PAUSADO")
        
        print("+" + "-" * (self.width * 2) + "+")
        
        for row in range(self.height):
            print("|", end="")
            for col in range(self.width):
                pos = (row, col)
                
                if pos == self.snake[0]:  # Cabeza
                    print("🟢", end="")
                elif pos in self.snake:   # Cuerpo
                    print("🟩", end="")
                elif pos == self.food:    # Comida
                    print("🍎", end="")
                elif pos in self.obstacles:  # Obstáculos
                    print("🧱", end="")
                elif pos in [pu['pos'] for pu in self.power_ups]:  # Power-ups
                    power_up = next(pu for pu in self.power_ups if pu['pos'] == pos)
                    power_up_icons = {
                        'speed_boost': '⚡',
                        'score_multiplier': '💎',
                        'shrink': '🔸',
                        'extra_life': '❤️'
                    }
                    print(power_up_icons.get(power_up['type'], '⭐'), end="")
                else:                     # Espacio vacío
                    print("  ", end="")
            print("|")
        
        print("+" + "-" * (self.width * 2) + "+")
        
        if self.game_over:
            print("💀 GAME OVER! 💀")
            print(f"Nivel alcanzado: {self.level}")
        
        # Mostrar leyenda de power-ups
        print("\nPower-ups: ⚡Speed ⭐Score 🔸Shrink ❤️Life")
        print("Controles: WASD - Mover | P - Pausar | Q - Salir | R - Reiniciar")
    
    def load_stats(self):
        """Cargar estadísticas"""
        try:
            with open('snake_stats.json', 'r') as f:
                return json.load(f)
        except:
            return {
                'games_played': 0,
                'high_score': 0,
                'max_level': 1,
                'total_score': 0
            }
    
    def save_stats(self):
        """Guardar estadísticas"""
        try:
            self.stats['games_played'] += 1
            self.stats['high_score'] = max(self.stats['high_score'], self.score)
            self.stats['max_level'] = max(self.stats['max_level'], self.level)
            self.stats['total_score'] += self.score
            
            with open('snake_stats.json', 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass
    
    def show_stats(self):
        """Mostrar estadísticas"""
        print("\n=== ESTADÍSTICAS ===")
        print(f"Partidas jugadas: {self.stats['games_played']}")
        print(f"Puntuación más alta: {self.stats['high_score']}")
        print(f"Nivel máximo: {self.stats['max_level']}")
        print(f"Puntuación total: {self.stats['total_score']}")
        
        if self.stats['games_played'] > 0:
            avg_score = self.stats['total_score'] / self.stats['games_played']
            print(f"Puntuación promedio: {avg_score:.1f}")

def main():
    while True:
        print("\n=== SNAKE GAME ===")
        print("1. Juego clásico")
        print("2. Juego avanzado")
        print("3. Ver estadísticas")
        print("4. Configurar dificultad")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            game = SnakeGame()
            game.play()
            
        elif opcion == "2":
            game = SnakeGameAdvanced()
            
            print("\nSelecciona dificultad:")
            print("1. Fácil")
            print("2. Normal")
            print("3. Difícil")
            
            diff_choice = input("Dificultad (1-3): ")
            difficulties = {"1": "easy", "2": "normal", "3": "hard"}
            game.difficulty = difficulties.get(diff_choice, "normal")
            
            game.play_advanced()
            
        elif opcion == "3":
            game = SnakeGameAdvanced()
            game.show_stats()
            
        elif opcion == "4":
            print("Configuración guardada para la próxima partida avanzada")
            
        elif opcion == "5":
            print("¡Gracias por jugar Snake! 🐍")
            break
        else:
            print("Opción no válida")

# Agregar método play_advanced a SnakeGameAdvanced
def play_advanced(self):
    """Bucle principal del juego avanzado"""
    print("🐍 ¡Bienvenido a Snake Game Advanced! 🐍")
    print("Presiona Enter para comenzar...")
    input()
    
    while True:
        self.draw_board_advanced()
        
        if self.game_over:
            self.save_stats()
            
            print(f"\n🎯 Puntuación final: {self.score}")
            print(f"🏆 Nivel alcanzado: {self.level}")
            
            if self.score > self.stats['high_score']:
                print("🎉 ¡NUEVO RÉCORD! 🎉")
            
            print("\n¿Jugar de nuevo? (s/n): ", end="")
            if input().lower().startswith('s'):
                self.reset_game()
                continue
            else:
                break
        
        # Obtener entrada del usuario (simplificado)
        user_input = input("Comando: ").lower().strip()
        
        if user_input == 'q':
            break
        elif user_input == 'r':
            self.reset_game()
            continue
        elif user_input == 'p':
            self.paused = not self.paused
            continue
        elif user_input in ['w']:
            self.change_direction(Direction.UP)
        elif user_input in ['s']:
            self.change_direction(Direction.DOWN)
        elif user_input in ['a']:
            self.change_direction(Direction.LEFT)
        elif user_input in ['d']:
            self.change_direction(Direction.RIGHT)
        
        # Mover serpiente
        self.move_snake()
        
        # Pausa según velocidad
        time.sleep(self.speed)
    
    print("¡Gracias por jugar Snake Advanced! 🐍")

# Agregar el método a la clase
SnakeGameAdvanced.play_advanced = play_advanced

if __name__ == "__main__":
    main()
