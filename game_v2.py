import random
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Optional

from GAME import BoardRenderer


class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @staticmethod
    def from_input(value: str) -> "Direction":

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


# DTO - Immutable
@dataclass(frozen=True)
class Position:
    x: int
    y: int


    def move(self, direction: Direction) -> "Position":
        dx, dy = direction.value
        return Position(self.x + dx, self.y + dy)

    def distance(self, other: "Position") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class Board:

    def __init__(self, width: int, height: int):

        if width < 2 or height < 2:
            raise ValueError("Width and height must be greater than 2")
        self.width = width
        self.height = height

    def is_valid(self, pos: Position) -> bool:
        return (0 <= pos.x < self.width) and (0 <= pos.y < self.height)

    def random_position(self, exclude: Optional[Position] = None) -> Position:
        while True:
            pos = Position(
                x=random.randint(1, self.width - 1),
                y=random.randint(1, self.height - 1),
            )
            if pos != exclude:
                return pos

class Player:

    def __init__(self, position: Position):
        self.position = position
        self.moves = 0

    def move(self, board: Board, direction: Direction):
        new_position = self.position.move(direction)
        if board.is_valid(new_position):
            self.position = new_position
            self.moves += 1

class Treasure:
    def __init__(self, position: Position):
        self.position = position
        self.found = False

    def is_at(self, position: Position) -> bool:
        return self.position == position

    def mark_as_found(self):
        self.found = True

@dataclass(frozen=True)
class GameState:
    width: int
    height: int
    player: Position
    treasure: Position
    treasure_found: bool
    moves: int



class Game:
    def __init__(self, width: int, height: int, debug: bool = False):
        self.debug = debug
        self.board = Board(width, height)

        self.player = Player(self.board.random_position())
        self.treasure = Treasure(self.board.random_position(exclude=self.player.position))

        self.last_distance = self.player.position.distance(self.treasure.position)

    def state(self) -> GameState:
        return GameState(
            width=self.board.width,
            height=self.board.height,
            player=self.player.position,
            treasure=self.treasure.position,
            treasure_found=self.treasure.found,
            moves=self.player.moves,
        )

    def step(self, direction: Direction) -> dict:
        self.player.move(self.board, direction)
        after = self.player.position

        # czy gracz znalazl skarb
        if self.treasure.is_at(after):
            self.treasure.mark_as_found()
            msg = f"Gratulacje! Znalazles skarb po {self.player.moves} ruchach."
            return {"message": msg, "found": True}

        # cieplo czy zimno?
        current_distance = after.distance(self.treasure.position)
        if current_distance < self.last_distance:
            msg = "Ciepło"
        else:
            msg = "Zimno"

        self.last_distance = current_distance
        return {"message": msg, "found": False}

    def size(self) -> tuple[int, int]:
        return self.board.width, self.board.height

class GameView(ABC):

    @abstractmethod
    def display_board(self, state: GameState, debug: bool = False):
        raise NotImplementedError

    @abstractmethod
    def get_direction(self) -> Direction:
        raise NotImplementedError

    @abstractmethod
    def show_info(self, message: str) -> None:
        raise NotImplementedError


class BoardRenderer:

    def render(self, state: GameState, debug: bool = False) -> list[list[str]]:
        board = []
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

class ConsoleView(GameView):

    def __init__(self, renderer: BoardRenderer):
        self.renderer = renderer

    def display_board(self, state: GameState, debug: bool = False):
        rows = self.renderer.render(state, debug)
        for row in rows:
            print(" ".join(row))
        print()

    def get_direction(self) -> Direction:
        raw = input("Podaj kierunek [w a s d]: ").strip().lower()
        return Direction.from_input(raw)

    def show_info(self, message: str) -> None:
        print(message)

class GameController:
    def __init__(self, game: Game, view: GameView):
        self.game = game
        self.view = view


    def play(self):

        w, h = self.game.size()
        print("Plansza o wymiarach: ", w, h)
        print("Pozycja gracza: ", self.game.player.position)

        if self.game.debug:
            print("DEBUG: pozycja skarbu: ", self.game.treasure.position)

        while True:
            self.view.display_board(self.game.state(), self.game.debug)
            direction = self.view.get_direction()
            result = self.game.step(direction)

            if result["found"]:
                self.view.display_board(self.game.state(), self.game.debug)
                self.view.show_info(result["message"])
                break
            else:
                self.view.show_info(result["message"])
                self.view.show_info(f"Twoja pozycja: {self.game.player.position}")

if __name__ == "__main__":
    game = Game(10, 10, debug=True)
    view = ConsoleView(renderer=BoardRenderer())
    controller = GameController(game, view)
    controller.play()