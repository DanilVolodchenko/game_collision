import random

from interfaces import IMovingObj

def check_collision(obj_1: IMovingObj, obj_2: IMovingObj) -> bool:
    """Псевдо функция, которая возвращает инфу о том, произошла ли коллизия между объектами?"""

    return random.choice([True, False])