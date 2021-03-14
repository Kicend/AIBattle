from random import randint
from api import errors


class API:
    def __init__(self, game_instance, units_info: list, team: int):
        self.__game = game_instance
        self.__units_info = units_info
        self.__team = team
        self.__units_registry = {}
        self.units_list = []
        self.__create_registry()

    def __create_registry(self):
        if not self.__units_registry:
            for unit in self.__units_info:
                self.__units_registry[unit.uid] = unit
                self.units_list.append(unit.uid)

    def team(self):
        return self.__team

    def units_list(self):
        return self.__units_registry

    def unit_info(self, uid: str):
        return self.__units_registry[uid].__dict__

    def unit_orders(self, uid: str):
        return self.__units_registry[uid].orders

    def scan(self, coordinates: list, scope: int):
        return self.__game.scan(coordinates, scope)

    def move(self, uid: str, coordinates: list):
        if self.__game.check_field(coordinates) and coordinates[0] > -1 and coordinates[1] > -1:
            if self.__units_registry[uid].move(coordinates):
                self.__game.map[self.__units_registry[uid].coordinates[0]][self.__units_registry[uid].coordinates[1]] \
                    = "-"
                self.__game.map[coordinates[0]][coordinates[1]] = self.__units_registry[uid]
            else:
                raise errors.MoveError(1, coordinates)
        else:
            raise errors.MoveError(0, coordinates)

    def attack(self, uid: str, coordinates: list):
        if not self.__game.check_field(coordinates):
            attacker = self.__units_registry[uid]
            target = self.__game.get_field_info(coordinates)
            if target.team != self.__team and \
               self.__game.get_distance(attacker.coordinates, target.coordinates) <= attacker.attack_range:
                if not randint(0, 99) <= target.miss_chance:
                    target.hp -= self.__units_registry[uid].attack() * (1 - target.defence/100)
                if target.hp <= 0:
                    target.status = "dead"
                    if hasattr(target, "after_death_symbol"):
                        self.__game.map[coordinates[0]][coordinates[1]] = target.after_death_symbol
                    else:
                        self.__game.map[coordinates[0]][coordinates[1]] = "-"
                    if hasattr(target, "respawn_time"):
                        self.__game.respawn_list[target.uid] = target.respawn_time
                    attacker.xp += target.xp_to_earn
                    if attacker.xp >= attacker.xp_to_next_level and attacker.level <= attacker.max_level:
                        attacker.xp -= attacker.xp_to_next_level
                        attacker.level += 1
            elif target.team == self.__team:
                raise errors.AttackError(0)
            else:
                raise errors.AttackError(1)

    def defend(self, uid: str):
        self.__units_registry[uid].defend()
