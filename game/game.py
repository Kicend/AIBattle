import importlib.util
import json
import time
import os
from math import fabs
from random import randint
from game.units.hq import HQ
from game.units.magnus import Magnus
from game.units.robot import Robot
from game.units.turret import Turret
from api.API import API

version = "0.1"


class Game:
    def __init__(self, cgi_status: bool, map_name: str, path_1: str, path_2: str):
        self.__is_cgi_enabled = cgi_status
        self.__script_1_path = path_1
        self.__script_2_path = path_2
        self.__ai_1_script = None
        self.__ai_2_script = None
        self.map_info = self.get_map_info(map_name)
        self.map = self.load_map()
        self.apis = []
        self.player_1_units = []
        self.player_2_units = []
        self.respawn_list = {}

    @staticmethod
    def get_map_info(map_name: str):
        with open(map_name, "r") as f:
            map_info = json.load(f)

        return map_info

    def load_map(self):
        premap = {}
        for number in range(self.map_info["size"][0]):
            i = 0
            x_field = []
            while i != self.map_info["size"][1]:
                x_field.append("-")
                i += 1
            premap[number] = x_field

        return premap

    def check_field(self, coordinates: list):
        x = coordinates[0]
        y = coordinates[1]

        if self.map[x][y] == "-":
            return True
        else:
            return False

    def get_field_info(self, coordinates: list):
        x = coordinates[0]
        y = coordinates[1]

        if not self.check_field(coordinates):
            return self.map[x][y]

    @staticmethod
    def get_distance(coordinates_a: list, coordinates_b: list):
        x_a = coordinates_a[0]
        y_a = coordinates_a[1]
        x_b = coordinates_b[0]
        y_b = coordinates_b[1]

        x_distance = fabs(x_a - x_b)
        y_distance = fabs(y_a - y_b)

        if x_distance >= y_distance:
            return x_distance
        else:
            return y_distance

    def respawn(self):
        if self.respawn_list != {}:
            for unit in self.respawn_list:
                self.respawn_list[unit] -= 1
                if self.respawn_list[unit] <= 0 and type(unit) != Magnus:
                    while True:
                        x = randint(0, self.map_info["size"][0] - 1)
                        if unit.team == 1:
                            y = 0
                        else:
                            y = self.map_info["size"][1] - 1
                        if self.map[x][y] == "-":
                            self.map[x][y] = unit
                            del self.respawn_list[unit]
                            break
                elif type(unit) == Magnus:
                    self.map[unit.coordinates[0]][unit.coordinates[1]] = unit.symbol
                    del self.respawn_list[unit]

    # noinspection PyTypeChecker
    def preparing(self):
        # Load API (create class instances)
        api_1 = API(self, self.player_1_units, 1)
        api_2 = API(self, self.player_2_units, 2)
        self.apis.extend([api_1, api_2])
        # Load AI modules
        spec = importlib.util.spec_from_file_location("AI", self.__script_1_path)
        self.__ai_1_script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.__ai_1_script)
        spec = importlib.util.spec_from_file_location("AI", self.__script_2_path)
        self.__ai_2_script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.__ai_2_script)

        hq_1 = HQ("HQ_1", self.map_info["HQ_1"], 1)
        self.map[hq_1.coordinates[0]][hq_1.coordinates[1]] = hq_1
        hq_2 = HQ("HQ_2", self.map_info["HQ_2"], 2)
        self.map[hq_2.coordinates[0]][hq_2.coordinates[1]] = hq_2
        self.player_1_units.append(hq_1)
        self.player_2_units.append(hq_2)
        m_1 = None
        m_2 = None
        for i in range(4):
            if i <= 1:
                m_1 = Magnus(f"M_1@{i+1}", self.map_info["M_1"][i], 1)
                self.map[m_1.coordinates[0]][m_1.coordinates[1]] = m_1
                m_2 = Magnus(f"M_2@{i+1}", self.map_info["M_2"][i], 2)
                self.map[m_2.coordinates[0]][m_2.coordinates[1]] = m_2
            t_1 = Turret(f"T_1@{i+1}", self.map_info["T_1"][i], 1)
            self.map[t_1.coordinates[0]][t_1.coordinates[1]] = t_1
            t_2 = Turret(f"T_2@{i + 1}", self.map_info["T_2"][i], 2)
            self.map[t_2.coordinates[0]][t_2.coordinates[1]] = t_2
            self.player_1_units.extend([m_1, t_1])
            self.player_2_units.extend([m_2, t_2])

        # TODO: Rozmieszczenie flag

        for i in range(self.map_info["MAX_UNIT_NUMBER"] - 7):
            while True:
                x = randint(0, self.map_info["size"][0] - 1)
                y = 0
                if self.map[x][y] == "-":
                    robot_1 = Robot(f"R_1@{i}", [x, y], 1)
                    self.map[robot_1.coordinates[0]][robot_1.coordinates[1]] = robot_1
                    break
            while True:
                x = randint(0, self.map_info["size"][0] - 1)
                y = self.map_info["size"][1] - 1
                if self.map[x][y] == "-":
                    robot_2 = Robot(f"R_2@{i}", [x, y], 2)
                    self.map[robot_2.coordinates[0]][robot_2.coordinates[1]] = robot_2
                    break
            self.player_1_units.append(robot_1)
            self.player_2_units.append(robot_2)

        self.main_loop()

    def render(self):
        main_map = ""
        k = 0
        while k != self.map_info["size"][1]+2:
            if k != self.map_info["size"][1]+1:
                main_map += "#"
            else:
                main_map += "#\n"
            k += 1

        for j, row in enumerate(self.map.values()):
            for i, field in enumerate(row):
                if i == 0:
                    main_map += "#"
                if field != "-":
                    unit = field
                    main_map += unit.symbol
                else:
                    main_map += field
                if i == len(row)-1:
                    main_map += "#\n"

        k = 0
        while k != self.map_info["size"][1]+2:
            if k != self.map_info["size"][1]+1:
                main_map += "#"
            else:
                main_map += "#\n"
            k += 1

        print(main_map)

    def is_victory(self):
        if "HQ_1" in self.respawn_list.keys():
            print("Wygrał gracz 2!")
            return True
        elif "HQ_2" in self.respawn_list.keys():
            print("Wygrał gracz 1!")
            return True
        else:
            return False

    def main_loop(self):
        while True:
            self.__ai_1_script.main(self.apis[0])
            os.system("cls")
            self.render()
            time.sleep(5)
            if self.is_victory():
                break
            self.__ai_2_script.main(self.apis[1])
            os.system("cls")
            self.render()
            time.sleep(5)
            if self.is_victory():
                break
