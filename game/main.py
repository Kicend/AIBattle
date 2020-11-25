# TODO: UI

import time
from game import game


def main():
    player1 = "game/AI/A.W.L.B.py"
    player2 = "game/AI/A.W.L.B.py"
    session = game.Game(False, "game/maps/map1.json", player1, player2)
    session.preparing()
    time.sleep(30)
