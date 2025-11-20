import random

# -------------------------
# Proste modele danych
# -------------------------
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        return Position(self.x + dx, self.y + dy)

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


# -------------------------
# Kierunki ruchu
# -------------------------
MOVES = {
    "w": (0, 1),    # góra
    "s": (0, -1),   # dół
    "a": (-1, 0),   # lewo
    "d": (1, 0),    # prawo
}


# -------------------------
# Główna gra
# -------------------------
def play(width=10, height=10):
    print("=== Gra: Znajdź Skarb ===")

    # losowanie pozycji gracza i skarbu
    player = Position(random.randint(0, width - 1), random.randint(0, height - 1))
    treasure = Position(random.randint(0, width - 1), random.randint(0, height - 1))

    # skarb nie może być w tym samym miejscu
    while treasure.x == player.x and treasure.y == player.y:
        treasure = Position(random.randint(0, width - 1), random.randint(0, height - 1))

    print(f"Twoja pozycja startowa: {player}")

    last_distance = player.distance(treasure)
    moves = 0

    # -------------------------
    # pętla gry
    # -------------------------
    while True:
        cmd = input("Podaj kierunek [w a s d]: ").strip().lower()

        if cmd not in MOVES:
            print("Niepoprawny kierunek!")
            continue

        dx, dy = MOVES[cmd]

        # nowa pozycja
        new_pos = player.move(dx, dy)

        # sprawdzenie wyjścia poza planszę
        if not (0 <= new_pos.x < width and 0 <= new_pos.y < height):
            print("Nie możesz wyjść poza planszę!")
            continue

        player = new_pos
        moves += 1

        # sprawdzamy zwycięstwo
        if player.x == treasure.x and player.y == treasure.y:
            print(f"Brawo! Znalazłeś skarb w {moves} ruchach!")
            break

        # obliczanie „ciepło / zimno”
        dist = player.distance(treasure)

        if dist < last_distance:
            print("Ciepło — zbliżasz się!")
        elif dist > last_distance:
            print("Zimno — oddalasz się!")
        else:
            print("Bez zmian.")

        print(f"Twoja pozycja: {player}")
        last_distance = dist


# -------------------------
# Start gry
# -------------------------
if __name__ == "__main__":
    play()
