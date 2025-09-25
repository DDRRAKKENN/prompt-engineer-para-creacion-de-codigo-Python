import random
import os

class TresEnRaya:
    def __init__(self, dificultad=10):
        self.tablero = [' ' for _ in range(9)]
        self.jugador_humano = 'X'
        self.jugador_ia = 'O'
        self.dificultad = dificultad  # 0 = Muy fácil, 10 = Imposible

    def mostrar_tablero(self):
        """Muestra el tablero actual con formato visual"""
        os.system('clear' if os.name == 'posix' else 'cls')  # Limpiar pantalla
        print("\n=== TRES EN RAYA ===")
        print(f"Dificultad de la IA: {self.dificultad}/10 {self.obtener_descripcion_dificultad()}")
        print("Posiciones:")
        print(" 1 | 2 | 3 ")
        print("-----------")
        print(" 4 | 5 | 6 ")
        print("-----------")
        print(" 7 | 8 | 9 ")
        print("\nTablero actual:")
        print(f" {self.tablero[0]} | {self.tablero[1]} | {self.tablero[2]} ")
        print("-----------")
        print(f" {self.tablero[3]} | {self.tablero[4]} | {self.tablero[5]} ")
        print("-----------")
        print(f" {self.tablero[6]} | {self.tablero[7]} | {self.tablero[8]} ")
        print()

    def obtener_descripcion_dificultad(self):
        """Devuelve una descripción de la dificultad actual"""
        descripciones = {
            0: "(🐣 Principiante)",
            1: "(😊 Muy Fácil)", 2: "(😊 Muy Fácil)",
            3: "(🙂 Fácil)", 4: "(🙂 Fácil)",
            5: "(😐 Normal)", 6: "(😐 Normal)",
            7: "(😤 Difícil)", 8: "(😤 Difícil)",
            9: "(😈 Muy Difícil)",
            10: "(🤖 Imposible)"
        }
        return descripciones.get(self.dificultad, "")

    def movimiento_valido(self, posicion):
        """Verifica si el movimiento es válido"""
        return 0 <= posicion <= 8 and self.tablero[posicion] == ' '

    def hacer_movimiento(self, posicion, jugador):
        """Realiza un movimiento en el tablero"""
        if self.movimiento_valido(posicion):
            self.tablero[posicion] = jugador
            return True
        return False

    def verificar_ganador(self):
        """Verifica si hay un ganador"""
        # Combinaciones ganadoras
        combinaciones = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]

        for combo in combinaciones:
            if (self.tablero[combo[0]] == self.tablero[combo[1]] == 
                self.tablero[combo[2]] != ' '):
                return self.tablero[combo[0]]
        return None

    def tablero_lleno(self):
        """Verifica si el tablero está lleno"""
        return ' ' not in self.tablero

    def obtener_movimientos_disponibles(self):
        """Obtiene lista de posiciones disponibles"""
        return [i for i in range(9) if self.tablero[i] == ' ']

    def minimax(self, es_maximizando):
        """Algoritmo Minimax para la IA"""
        ganador = self.verificar_ganador()

        # Casos base
        if ganador == self.jugador_ia:
            return 1
        elif ganador == self.jugador_humano:
            return -1
        elif self.tablero_lleno():
            return 0

        if es_maximizando:
            mejor_puntuacion = -float('inf')
            for posicion in self.obtener_movimientos_disponibles():
                self.tablero[posicion] = self.jugador_ia
                puntuacion = self.minimax(False)
                self.tablero[posicion] = ' '
                mejor_puntuacion = max(puntuacion, mejor_puntuacion)
            return mejor_puntuacion
        else:
            mejor_puntuacion = float('inf')
            for posicion in self.obtener_movimientos_disponibles():
                self.tablero[posicion] = self.jugador_humano
                puntuacion = self.minimax(True)
                self.tablero[posicion] = ' '
                mejor_puntuacion = min(puntuacion, mejor_puntuacion)
            return mejor_puntuacion

    def obtener_mejor_movimiento_ia(self):
        """Obtiene el mejor movimiento para la IA usando Minimax con dificultad ajustable"""
        movimientos_disponibles = self.obtener_movimientos_disponibles()

        # Calcular probabilidad de usar estrategia óptima basada en dificultad
        # Dificultad 0 = 10% óptima, Dificultad 10 = 100% óptima
        probabilidad_optima = (self.dificultad * 10) / 100

        # Decidir si jugar de forma óptima o aleatoria
        if random.random() <= probabilidad_optima:
            # Usar estrategia óptima (Minimax)
            mejor_puntuacion = -float('inf')
            mejor_movimiento = None

            for posicion in movimientos_disponibles:
                self.tablero[posicion] = self.jugador_ia
                puntuacion = self.minimax(False)
                self.tablero[posicion] = ' '

                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    mejor_movimiento = posicion

            return mejor_movimiento
        else:
            # Hacer movimiento aleatorio (error de la IA)
            return random.choice(movimientos_disponibles)

    def jugar(self):
        """Función principal del juego"""
        print("¡Bienvenido al Tres en Raya!")
        print("Tú eres 'X' y la IA es 'O'")
        print("Ingresa un número del 1-9 para hacer tu movimiento")

        while True:
            self.mostrar_tablero()

            # Verificar si hay ganador
            ganador = self.verificar_ganador()
            if ganador:
                if ganador == self.jugador_humano:
                    print("🎉 ¡Felicidades! ¡Has ganado!")
                else:
                    print("🤖 La IA ha ganado. ¡Mejor suerte la próxima vez!")
                break

            if self.tablero_lleno():
                print("🤝 ¡Empate! Buen juego.")
                break

            # Turno del jugador humano
            try:
                movimiento = int(input("Tu movimiento (1-9): ")) - 1
                if not self.movimiento_valido(movimiento):
                    print("❌ Movimiento inválido. Intenta de nuevo.")
                    input("Presiona Enter para continuar...")
                    continue

                self.hacer_movimiento(movimiento, self.jugador_humano)

            except ValueError:
                print("❌ Por favor ingresa un número válido.")
                input("Presiona Enter para continuar...")
                continue

            # Verificar ganador después del movimiento del jugador
            ganador = self.verificar_ganador()
            if ganador or self.tablero_lleno():
                continue

            # Turno de la IA
            print("🤖 La IA está pensando...")
            movimiento_ia = self.obtener_mejor_movimiento_ia()
            self.hacer_movimiento(movimiento_ia, self.jugador_ia)
            print(f"La IA eligió la posición {movimiento_ia + 1}")
            input("Presiona Enter para continuar...")

def seleccionar_dificultad():
    """Permite al jugador seleccionar la dificultad de la IA"""
    print("\n" + "="*40)
    print("        SELECCIONAR DIFICULTAD")
    print("="*40)
    print("0  - 🐣 Principiante    (IA hace muchos errores)")
    print("1-2- 😊 Muy Fácil       (IA comete errores frecuentes)")
    print("3-4- 🙂 Fácil           (IA comete algunos errores)")
    print("5-6- 😐 Normal          (IA juega decentemente)")
    print("7-8- 😤 Difícil         (IA juega muy bien)")
    print("9  - 😈 Muy Difícil     (IA casi nunca se equivoca)")
    print("10 - 🤖 Imposible       (IA perfecta, nunca pierde)")
    print("-"*40)

    while True:
        try:
            dificultad = int(input("Selecciona dificultad (0-10): "))
            if 0 <= dificultad <= 10:
                return dificultad
            else:
                print("❌ Por favor ingresa un número entre 0 y 10")
        except ValueError:
            print("❌ Por favor ingresa un número válido")

def main():
    """Función principal con menú"""
    while True:
        print("\n" + "="*30)
        print("    TRES EN RAYA CON IA")
        print("="*30)
        print("1. Jugar nueva partida")
        print("2. Salir")

        opcion = input("\nSelecciona una opción (1-2): ")

        if opcion == '1':
            # Seleccionar dificultad antes de empezar
            dificultad = seleccionar_dificultad()

            print(f"\n🎮 Iniciando partida en dificultad {dificultad}/10")
            input("Presiona Enter para comenzar...")

            juego = TresEnRaya(dificultad)
            juego.jugar()

            # Preguntar si quiere jugar de nuevo
            jugar_otra = input("\n¿Quieres jugar otra partida? (s/n): ").lower()
            if jugar_otra != 's':
                break

        elif opcion == '2':
            print("¡Gracias por jugar! 👋")
            break
        else:
            print("❌ Opción inválida. Por favor selecciona 1 o 2.")

if __name__ == "__main__":
    main()
