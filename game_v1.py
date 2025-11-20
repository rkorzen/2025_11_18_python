import random

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


p = Position(9, 9)
s = Position(1, 1)

print(p.distance(s)
