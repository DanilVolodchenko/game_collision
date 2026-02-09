from typing import TypeAlias
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def move_to(self, velocity: 'Velocity') -> 'Point':
        return Point(self.x + velocity.dx, self.y + velocity.dy)


@dataclass
class Velocity:
    dx: float
    dy: float


CellKey: TypeAlias = tuple[int, int]
