from random import randint


class Turret:
    def __init__(self, uid: str, coordinates: list, team: int):
        self.uid = uid
        self.symbol = "T"
        self.hp = 150
        self.status = "alive"
        self.after_death_symbol = "+"
        self.attackable = True
        self.regenerate_rate = 1.5
        self.vision_range = 5
        self.attack_range = 3
        self.min_dmg = 7
        self.max_dmg = 10
        self.xp_to_earn = 50
        self.coordinates = coordinates
        self.actions = 1
        self.max_actions = 1
        self.team = team
        self.orders = "attack"

    def attack(self):
        dmg = randint(self.min_dmg, self.max_dmg)

        return dmg
