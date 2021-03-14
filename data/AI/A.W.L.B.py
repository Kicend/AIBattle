from api import errors
from random import randint


def main(api):
    for unit in api.units_list:
        if "move" in api.unit_orders(unit):
            if api.unit_info(unit)["actions"] > 0:
                coordinates = api.unit_info(unit)["coordinates"]
                i = 0
                while True:
                    try:
                        if i >= 3:
                            api.defend(unit)
                        else:
                            x = randint(-2, 2)
                            y = randint(-2, 2)
                            api.move(unit, [coordinates[0]+x, coordinates[1]+y])
                        break
                    except (errors.MoveError, KeyError, IndexError):
                        pass
                    i += 1
