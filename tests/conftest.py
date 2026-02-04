from typing import Type
from unittest.mock import Mock

import pytest

from interfaces import IMovingObj
from dto import Velocity


@pytest.fixture
def moving_mock_obj_without_location() -> Type[IMovingObj]:
    class MockMovingObj(IMovingObj):  # noqa
        @property
        def velocity(self) -> Mock:
            return Mock()

    return MockMovingObj


@pytest.fixture
def moving_mock_obj_without_velocity() -> Type[IMovingObj]:
    class MockMovingObj(IMovingObj):  # noqa
        @property
        def location(self) -> Mock:
            return Mock()

        @location.setter
        def location(self, new_value: Velocity) -> None:
            self.location = new_value

    return MockMovingObj


@pytest.fixture
def moving_mock_obj_without_ability_set_location() -> Type[IMovingObj]:
    class MockMovingObj(IMovingObj):  # noqa
        @property
        def location(self) -> Mock:
            return Mock()

        @property
        def velocity(self) -> Mock:
            return Mock()

    return MockMovingObj
