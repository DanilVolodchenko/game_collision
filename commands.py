from interfaces import ICommand, IMovingObj
from utils import check_collision
from field import GameField
from macro_commands import MacroCommand


class MoveCommand(ICommand):
    """Команда для выполнения движения."""

    def __init__(self, obj: IMovingObj) -> None:
        self.obj = obj

    def execute(self) -> None:
        self.obj.location = self.obj.location.move_to(self.obj.velocity)


class CheckCollisionCommand(ICommand):
    def __init__(self, obj_1: IMovingObj, obj_2: IMovingObj) -> None:
        self.obj_1 = obj_1
        self.obj_2 = obj_2

    def execute(self) -> None:
        check_collision(self.obj_1, self.obj_2)


class UpdateNeighborhoodCommand(ICommand):
    """Команда для создания макрокоманд проверки коллизий."""

    def __init__(
            self,
            obj: IMovingObj,
            field: GameField,
            collision_macro: dict[IMovingObj, MacroCommand],
    ) -> None:
        self.obj = obj
        self.field = field
        self.collision_macro = collision_macro
        self._current_cell: tuple[int, int] | None = None

    def execute(self) -> None:
        new_cell = self.field.get_cell(self.obj.location)

        if self._current_cell == new_cell:
            return

        if self._current_cell is not None:
            self.field.remove_obj(self.obj, self._current_cell)

        self.field.add_obj(self.obj)

        commands: list[ICommand] = []

        for other_obj in self.field.get_objects_in_cell(new_cell):
            if other_obj is not self.obj:
                commands.append(CheckCollisionCommand(self.obj, other_obj))

        macro = MacroCommand(commands)

        self.collision_macro[self.obj] = macro

        self._current_cell = new_cell
