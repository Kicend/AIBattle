import json
import os
from game import main

version = "0.2"

default_config = {"ai_1_script_path": "game/AI/A.W.L.B.py",
                  "ai_2_script_path": "game/AI/A.W.L.B.py"}


def startup():
    os.makedirs("game/settings", exist_ok=True)
    if not os.path.isfile("game/settings/config.json"):
        with open("game/settings/config.json", "a") as f:
            json.dump(default_config, f, indent=4)

    with open("game/settings/config.json", "r") as f:
        game_config = json.load(f)

    return game_config


def update():
    pass


if __name__ == "__main__":
    config = startup()
    main.main(config)
