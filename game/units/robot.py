from math import fabs
from random import randint


class Robot:
    def __init__(self, uid: str, coordinates: list, team: int):
        self.uid = uid
        self.symbol = "R"
        self.level = 1
        self.max_level = 3
        self.hp = 15 * self.level
        self.status = "alive"
        self.attackable = True
        self.regenerate_rate = self.level - 1
        self.vision_range = 2
        self.attack_range = 1
        self.min_dmg = 1
        self.max_dmg = 3
        self.critical_chance = 0.05
        self.xp = 0
        self.xp_to_next_level = 10 * self.level
        self.xp_to_earn = 5 * self.level
        self.coordinates = coordinates
        self.actions = 2
        self.max_actions = 2
        self.respawn_time = 7
        self.team = team
        self.orders = ("move", "attack", "defend")

    def move(self, coordinates: list):
        if fabs(coordinates[0] - self.coordinates[0]) <= self.actions and \
           fabs(coordinates[1] - self.coordinates[1]) <= self.actions:
            self.actions -= fabs(coordinates[0] - self.coordinates[0])
            return True
        else:
            return False

    def attack(self):
        self.actions = 0
        dmg = randint(self.min_dmg, self.max_dmg)

        return dmg

    def defend(self):
        pass
