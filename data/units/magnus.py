class Magnus:
    def __init__(self, uid: str, coordinates: list, team: int):
        self.uid = uid
        self.symbol = "M"
        self.hp = 200
        self.status = "alive"
        self.attackable = True
        self.regenerate_rate = 2
        self.vision_range = 5
        self.xp_to_earn = 100
        self.coordinates = coordinates
        self.respawn_time = 21
        self.after_death_symbol = "*"
        self.team = team
        self.orders = ""
