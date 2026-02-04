from typing import Type
from unittest.mock import Mock

import pytest

from interfaces import IMovingObj
from dto import Point, Velocity
from macro_commands import MacroCommand
from commands import MoveCommand, UpdateNeighborhoodCommand, CheckCollisionCommand
from field import GameField


class TestMoveCommand:

    def test_move_from_12_5__with_velocity_minus_7_3(self) -> None:
        """Движение объекта с точки 12,5 и скорость -7,3 в точку 5,8."""

        movable_mock_obj = Mock(location=Point(12, 5), velocity=Velocity(-7, 3))

        result_before_move = movable_mock_obj.location
        MoveCommand(movable_mock_obj).execute()
        result_after_move = movable_mock_obj.location

        expected_result_before_move = Point(12, 5)
        expected_result_after_move = Point(5, 8)

        assert result_before_move == expected_result_before_move, f'Ожидаемый результат: {expected_result_before_move}, полученный результат: {result_before_move}'
        assert result_after_move == expected_result_after_move, f'Ожидаемый результат: {expected_result_after_move}, полученный результат: {result_after_move}'

    def test_move_obj_without_location(self, moving_mock_obj_without_location: Type[IMovingObj]) -> None:
        """Попытка выполнить движение без возможности получения положения в пространстве."""

        with pytest.raises(TypeError):
            moving_mock_obj = moving_mock_obj_without_location()
            MoveCommand(moving_mock_obj).execute()

    def test_move_obj_without_velocity(self, moving_mock_obj_without_velocity: Type[IMovingObj]) -> None:
        """Попытка выполнить движение без возможности получения мгновенной скорости."""

        with pytest.raises(TypeError):
            moving_mock_obj = moving_mock_obj_without_velocity()
            MoveCommand(moving_mock_obj).execute()

    def test_move_obj_without_set_velocity(
            self, moving_mock_obj_without_ability_set_location: Type[IMovingObj]
    ) -> None:
        """Попытка выполнить движение без возможности изменения положения в пространстве."""

        with pytest.raises(AttributeError):
            moving_mock_obj = moving_mock_obj_without_ability_set_location()
            MoveCommand(moving_mock_obj).execute()


class TestMacroCommand:

    def test_execute_all_commands_in_order(self) -> None:
        """Макрокоманда должна выполнить все команды по порядку."""

        cmd1 = Mock()
        cmd2 = Mock()
        cmd3 = Mock()

        macro = MacroCommand([cmd1, cmd2, cmd3])
        macro.execute()

        cmd1.execute.assert_called_once()
        cmd2.execute.assert_called_once()
        cmd3.execute.assert_called_once()

    def test_execute_empty_macro_command(self) -> None:
        """Пустая макрокоманда не должна падать."""

        macro = MacroCommand([])
        macro.execute()


class TestGameField:

    def test_object_added_to_correct_cell(self) -> None:
        """Объект должен добавляться в корректную окрестность."""

        field = GameField(cell_size=10)
        obj = Mock(spec=IMovingObj)
        obj.location = Point(12, 7)

        field.add_obj(obj)
        cell = field.get_cell(obj.location)

        assert obj in field.get_objects_in_cell(cell)

    def test_object_removed_from_cell(self) -> None:
        """Объект должен удаляться из окрестности."""

        field = GameField(cell_size=10)
        obj = Mock(spec=IMovingObj)
        obj.location = Point(5, 5)

        cell = field.get_cell(obj.location)
        field.add_obj(obj)
        field.remove_obj(obj, cell)

        assert obj not in field.get_objects_in_cell(cell)

    def test_get_empty_cell_returns_empty_set(self) -> None:
        """Пустая окрестность должна возвращать пустой set."""

        field = GameField(cell_size=10)
        assert field.get_objects_in_cell((100, 100)) == set()


class TestUpdateNeighborhoodCommand:

    def test_add_object_to_field_and_create_macro(self) -> None:
        """Объект должен быть добавлен в окрестность и получить макрокоманду."""

        field = GameField(cell_size=10)
        macros: dict[IMovingObj, MacroCommand] = {}

        obj = Mock(spec=IMovingObj)
        obj.location = Point(1, 1)

        cmd = UpdateNeighborhoodCommand(obj, field, macros)
        cmd.execute()

        cell = field.get_cell(obj.location)

        assert obj in field.get_objects_in_cell(cell)
        assert obj in macros
        assert isinstance(macros[obj], MacroCommand)

    def test_macro_contains_collision_commands_for_same_cell(self) -> None:
        """Макрокоманда должна содержать команды проверки коллизий."""

        field = GameField(cell_size=10)
        macros: dict[IMovingObj, MacroCommand] = {}

        obj1 = Mock(spec=IMovingObj)
        obj1.location = Point(1, 1)

        obj2 = Mock(spec=IMovingObj)
        obj2.location = Point(2, 2)

        UpdateNeighborhoodCommand(obj1, field, macros).execute()
        UpdateNeighborhoodCommand(obj2, field, macros).execute()

        macro = macros[obj2]

        assert len(macro.commands) == 1

    def test_object_moves_to_new_cell_rebuilds_macro(self) -> None:
        """При смене окрестности макрокоманда должна пересоздаваться."""

        field = GameField(cell_size=10)
        macros: dict[IMovingObj, MacroCommand] = {}

        obj = Mock(spec=IMovingObj)
        obj.location = Point(1, 1)

        cmd = UpdateNeighborhoodCommand(obj, field, macros)
        cmd.execute()

        old_macro = macros[obj]

        obj.location = Point(50, 50)
        cmd.execute()

        new_macro = macros[obj]

        assert old_macro is not new_macro


class TestCheckCollisionCommand:

    def test_execute_does_not_raise(self) -> None:
        """Команда проверки коллизии не должна выбрасывать исключений."""

        obj1 = Mock(spec=IMovingObj)
        obj2 = Mock(spec=IMovingObj)

        cmd = CheckCollisionCommand(obj1, obj2)
        cmd.execute()
