class Flag:
    def __init__(self, uid: str, coordinates: list, team: int):
        self.uid = uid
        self.symbol = "F"
        self.attackable = False
        self.vision_range = 5
        self.coordinates = coordinates
        self.respawn_time_reduction = 1
        self.team = team
