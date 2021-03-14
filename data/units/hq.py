class HQ:
    def __init__(self, uid: str, coordinates: list, team: int):
        self.uid = uid
        self.symbol = "H"
        self.hp = 500
        self.status = "alive"
        self.attackable = True
        self.regenerate_rate = 5
        self.vision_range = 5
        self.coordinates = coordinates
        self.team = team
        self.orders = ""
