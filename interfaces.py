import abc

from dto import Point, Velocity


class ICommand(abc.ABC):
    """Интерфейс команд."""

    @abc.abstractmethod
    def execute(self) -> None:
        """Метод для взаимодействия с командой."""


class IMovingObj(abc.ABC):
    """Интерфейс для движущихся объектов."""

    @property
    @abc.abstractmethod
    def location(self) -> Point:
        """Возвращает местоположение объекта."""

    @location.setter
    @abc.abstractmethod
    def location(self, new_location: Point) -> None:
        """Изменяет местоположение объекта."""

    @property
    @abc.abstractmethod
    def velocity(self) -> Velocity:
        """Возвращает скорость объекта."""
