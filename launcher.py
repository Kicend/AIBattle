import json
from os import path
from game import main

default_config = {"ai_1_script_path": "game/AI/A.W.L.B.py",
                  "ai_2_script_path": "game/AI/A.W.L.B.py"}


def startup():
    if not path.isfile("game/settings/config.json"):
        with open("game/settings/config.json", "a") as f:
            json.dump(default_config, f, indent=4)


def update():
    pass


if __name__ == "__main__":
    startup()
    main.main()
