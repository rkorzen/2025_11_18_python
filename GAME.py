import random
from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ============================================================
# Direction – enum reprezentujący kierunek ruchu gracza
# ============================================================
class Direction(Enum):
    # Każdy kierunek jest mapowany na zmianę współrzędnych (dx, dy)
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @staticmethod
    def from_input(value: str) -> "Direction":
        """
        Zamienia pojedynczą literę (w,a,s,d) na obiekt Direction.
        Dzięki temu UI może używać prostych znaków, a logika gry używa typów.
        """
        mapping = {
            "w": Direction.UP,
            "s": Direction.DOWN,
            "a": Direction.LEFT,
            "d": Direction.RIGHT,
        }
        v = value.strip().lower()
        if v in mapping:
            return mapping[v]
        raise ValueError(f"Invalid direction: {value}. Choices are: w, a, s, d")


# ============================================================
# Position – immutable model opisujący punkt na planszy
# ============================================================
@dataclass(frozen=True)
class Position:
    """
    Reprezentuje pozycję na planszy.
    Dzięki frozen=True instancje są niezmienne, łatwe do testowania
    i mogą być kluczami w słownikach.
    """
    x: int
    y: int

    def move(self, direction: Direction) -> "Position":
        """Zwraca nową pozycję przesuniętą o dx,dy zgodnie z kierunkiem."""
        dx, dy = direction.value
        return Position(self.x + dx, self.y + dy)

    def distance(self, other: "Position") -> int:
        """Zwraca dystans Manhattanowski do innej pozycji."""
        return abs(self.x - other.x) + abs(self.y - other.y)


# ============================================================
# Board – logika planszy (rozmiar, walidacja ruchów, losowanie pozycji)
# ============================================================
class Board:
    def __init__(self, width: int, height: int):
        if width < 0 or height < 0:
            raise ValueError("Width and height must be non-negative")
        self.width = width
        self.height = height

    def is_valid(self, pos: Position) -> bool:
        """Sprawdza czy pozycja mieści się na planszy."""
        return (
                0 <= pos.x < self.width
                and 0 <= pos.y < self.height
        )

    def random_position(self, exclude: Optional[Position] = None) -> Position:
        """
        Losuje pozycję na planszy. Jeśli podano exclude – nie wraca tej pozycji.
        Używane do rozmieszczania gracza i skarbu.
        """
        while True:
            pos_x = random.randint(0, self.width - 1)
            pos_y = random.randint(0, self.height - 1)
            pos = Position(pos_x, pos_y)
            if pos != exclude:
                return pos


# ============================================================
# Player – stan i logika ruchu gracza
# ============================================================
class Player:
    """Reprezentuje gracza i liczbę wykonanych ruchów."""

    def __init__(self, poistion: Position):
        self.position = poistion  # pozycja startowa
        self.moves = 0            # liczba wykonanych ruchów

    def caluclate_new_position(self, direction: Direction) -> Position:
        """Zwraca pozycję po przesunięciu (bez zmiany obiektu gracza)."""
        return self.position.move(direction)

    def move(self, board: Board, direction: Direction) -> bool:
        """
        Przesuwa gracza, jeśli ruch mieści się w planszy.
        Inkrementuje licznik ruchów.
        """
        new_position = self.caluclate_new_position(direction)

        # Sprawdzenie, czy ruch jest dozwolony
        if not board.is_valid(new_position):
            raise ValueError("Invalid move. You can't move outside the board.")

        # Zatwierdzenie ruchu
        self.position = new_position
        self.moves += 1


# ============================================================
# Treasure – obiekt skarbu ukrytego na planszy
# ============================================================
class Treasure:
    """Reprezentuje skarb i sygnalizuje, czy został znaleziony."""

    def __init__(self, position: Position):
        self.position = position
        self.found = False

    def is_at(self, position: Position) -> bool:
        """Czy skarb znajduje się na podanej pozycji?"""
        return self.position == position

    def mark_as_found(self):
        """Ustawia informację, że skarb został odnaleziony."""
        self.found = True


# ============================================================
# GameState – DTO reprezentujące pełny stan gry
# ============================================================
@dataclass(frozen=True)
class GameState:
    """
    Obiekt DTO zwracany do Widoku. Rozdziela logikę od prezentacji.
    Widok zna tylko GameState, nie zna szczegółów klas Game/Board/Player.
    """
    width: int
    height: int
    player: Position
    treasure: Position
    treasure_found: bool
    moves: int


# ============================================================
# Game – główna logika gry (model + logika rozgrywki)
# ============================================================
class Game:
    def __init__(self, width: int, height: int, debug: bool = False):
        self.debug = debug
        self.board = Board(width, height)

        # Losowanie pozycji startowej gracza i skarbu
        self.player = Player(self.board.random_position())
        self.treasure = Treasure(self.board.random_position(exclude=self.player.position))

        # Początkowy dystans gracza od skarbu
        self.last_distance = self.player.position.distance(self.treasure.position)

    def state(self) -> GameState:
        """Zwraca aktualny stan gry w formie DTO."""
        return GameState(
            width=self.board.width,
            height=self.board.height,
            player=self.player.position,
            treasure=self.treasure.position,
            treasure_found=self.treasure.found,
            moves=self.player.moves,
        )

    def step(self, direction: Direction) -> dict:
        """
        Wykonuje jeden krok gry:
        - przesuwa gracza
        - sprawdza czy znalazł skarb
        - generuje komunikat ciepło/zimno
        """
        before = self.player.position
        self.player.move(self.board, direction)
        after = self.player.position

        # Czy gracz znalazł skarb?
        if self.treasure.is_at(after):
            self.treasure.mark_as_found()
            msg = f"Gratulacje! Znalazles skarb po {self.player.moves} ruchach."
            return {"message": msg, "found": True}

        # Obliczenie czy zrobiło się "ciepło" czy "zimno"
        current_distance = after.distance(self.treasure.position)
        if current_distance < self.last_distance:
            msg = "Ciepło. Zbliżyłeś się do Skarbu"
        elif current_distance > self.last_distance:
            msg = "Zimno. Oddaliłeś sie od Skarbu"
        else:
            msg = "Bez zmian"

        # Aktualizacja dystansu
        self.last_distance = current_distance
        return {"message": msg, "found": False}

    def size(self) -> tuple[int, int]:
        """Zwraca wymiary planszy (na potrzeby UI)."""
        return self.board.width, self.board.height


# ============================================================
# GameView – warstwa abstrakcyjna widoku (konsola, GUI, web)
# ============================================================
class GameView:
    """Abstrakcyjna klasa widoku. Może być implementowana różnie."""

    def display_board(self, state: dict, debug: bool = False) -> None:
        raise NotImplementedError

    def get_direction(self) -> Direction:
        raise NotImplementedError

    def show_info(self, message: str) -> None:
        raise NotImplementedError


# ============================================================
# BoardRenderer – czysta logika rysowania planszy (bez I/O)
# ============================================================
class BoardRenderer:
    """
    Klasa odpowiedzialna tylko za tworzenie reprezentacji ASCII planszy.
    Dzięki temu ConsoleView nie musi znać logiki rysowania.
    """

    def render(self, state: GameState, debug: bool = False) -> list[list[str]]:
        board = []

        # Iteracja od górnego rzędu do dolnego, aby plansza wyglądała naturalnie
        for y in reversed(range(state.height)):
            row = []
            for x in range(state.width):
                pos = Position(x, y)

                if pos == state.player:
                    row.append("P")
                elif debug and pos == state.treasure:
                    row.append("T")
                else:
                    row.append(".")
            board.append(row)

        return board


# ============================================================
# ConsoleView – implementacja widoku w konsoli
# ============================================================
class ConsoleView(GameView):
    def __init__(self, renderer: BoardRenderer):
        self.renderer = renderer  # injekcja renderera (zasada SRP + testowalność)

    def display_board(self, state: GameState, debug: bool = False):
        """
        Wyświetla planszę w konsoli na podstawie danych dostarczonych przez renderer.
        """
        rows = self.renderer.render(state, debug)
        for row in rows:
            print(" ".join(row))
        print()

    def get_direction(self) -> Direction:
        """Wczytuje ruch użytkownika (w a s d) i konwertuje go na Direction."""
        raw = input("Podaj kierunek [w a s d]: ").strip().lower()
        return Direction.from_input(raw)

    def show_info(self, message: str) -> None:
        """Wyświetla komunikaty (ciepło/zimno, znaleziono skarb itd.)."""
        print(message)


# ============================================================
# GameController – pętla sterująca całym przebiegiem gry
# ============================================================
class GameController:
    def __init__(self, game: Game, view: GameView):
        self.game = game
        self.view = view

    def play(self):
        """
        Główna pętla gry:
        - wyświetlanie planszy
        - pobieranie ruchu od użytkownika
        - wykonanie kroku gry
        - obsługa zwycięstwa
        """
        w, h = self.game.size()

        print("Plansza o wymiarach:", w, "x", h)
        print(f"Start: pozycja gracza: {self.game.player.position}")

        if self.game.debug:
            print(f"DEBUG: pozycja skarbu: {self.game.treasure.position}")

        # Pętla trwa do znalezienia skarbu
        while True:
            self.view.display_board(self.game.state(), self.game.debug)
            direction = self.view.get_direction()
            result = self.game.step(direction)

            if result["found"]:
                # ostatni raz pokazujemy planszę
                self.view.display_board(self.game.state(), self.game.debug)
                self.view.show_info(result["message"])
                break
            else:
                self.view.show_info(result["message"])
                self.view.show_info(f"Twoja pozycja: {self.game.player.position}")


# ============================================================
# Program główny – uruchomienie gry w trybie konsoli
# ============================================================
if __name__ == "__main__":
    game = Game(10, 10, debug=True)                     # logika gry
    view = ConsoleView(renderer=BoardRenderer())        # widok konsolowy
    controller = GameController(game, view)             # pętla gry
    controller.play()                                   # start gry
