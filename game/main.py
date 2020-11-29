# TODO: UI

import time
from game import game


def main(game_config):
    player1 = game_config["ai_1_script_path"]
    player2 = game_config["ai_2_script_path"]
    session = game.Game(False, "game/maps/map1.json", player1, player2)
    session.preparing()
    time.sleep(30)
