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
                        api.move(unit, [coordinates[0]+randint(-1, 1), coordinates[1]+randint(-1, 1)])
                        if i == 3:
                            api.defend(unit)
                        break
                    except (errors.MoveError, KeyError, IndexError):
                        pass
                    i += 1
