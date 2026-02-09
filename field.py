from dto import CellKey, Point
from interfaces import IMovingObj


class GameField:

    def __init__(self, cell_size: float, offset_x: float = 0, offset_y: float = 0) -> None:
        self.cell_size = cell_size
        self.offset_x = offset_x
        self.offset_y = offset_y

        self._cells: dict[CellKey, set[IMovingObj]] = {}

    def get_cell(self, point: Point) -> CellKey:
        x = int((point.x + self.offset_x) // self.cell_size)
        y = int((point.y + self.offset_y) // self.cell_size)
        return x, y

    def add_obj(self, obj: IMovingObj) -> CellKey:
        """Добавляет объект в окрестность."""

        cell = self.get_cell(obj.location)

        if cell not in self._cells:
            self._cells[cell] = set()

        self._cells[cell].add(obj)

        return cell

    def remove_obj(self, obj: IMovingObj, cell: CellKey) -> None:
        """Удаляет объект с окрестности и саму окрестность если необходимо."""

        if cell in self._cells:
            self._cells[cell].discard(obj)

            if not self._cells[cell]:
                del self._cells[cell]

    def get_objects_in_cell(self, cell: CellKey) -> set[IMovingObj]:
        """Возвращает все объект в окрестности."""
        return self._cells.get(cell, set())