from demoparser2 import DemoParser
import math
import numpy as np

def show_player(Demo_Name):
    Demo_File = DemoParser(Demo_Name)
    players = Demo_File.parse_player_info()
    for i in players["name"]:
        print(i)

class Data():
    def __init__(self, Demo_Name, Display_Size, Player_Name):
        self.Demo_File = DemoParser(Demo_Name)
        self.Props = ["yaw", "pitch", "is_alive", "FIRE"]

        self.players = self.Demo_File.parse_player_info()
        self.current_player = Player_Name
        self.display_size = Display_Size

        self.all_player_input = []
        self.isFire = False
        self.Fire_Rate = 10
        self.Compile_Rate = 30

        self.out_data = []

    def get_player_data(self):
        for player_number in range(len(self.players["name"])):
            if self.players["name"][player_number] == self.current_player:
                return self.players["steamid"][player_number]

    def convert_data(self, yaw, pitch):
        yaw_rad = math.radians(yaw)
        pitch_rad = math.radians(pitch)

        x = int(math.cos(pitch_rad) * math.cos(yaw_rad) * self.display_size[0])
        y = int(math.cos(pitch_rad) * math.sin(yaw_rad) * self.display_size[1])

        return x, y

    def get_player_input(self):
        player_input = self.Demo_File.parse_ticks(self.Props, players=[self.get_player_data()])
        for frame in range(len(player_input["yaw"])):
            if player_input["is_alive"][frame]:

                yaw = player_input["yaw"][frame]
                pitch = player_input["pitch"][frame]

                x, y = self.convert_data(yaw, pitch)
                self.all_player_input.append([x, y])

                if player_input["FIRE"][frame]:
                    if self.isFire == False:
                        self.fire_reg()
                        self.isFire = True
                else:
                    self.isFire = False
        compile_data = self.compile_data()

        return compile_data

    def module(self, x):
        if x < 0:
            return -x
        else:
            return x

    def calc_speed(self, old_pos, new_pos):
        x_speed = self.module(old_pos[0] - new_pos[0])
        y_speed = self.module(old_pos[1] - new_pos[1])

        return x_speed + y_speed

    def calc_avg(self, all):
        all_sum = 0
        for i in all:
            all_sum += i

        return all_sum / len(all)

    def is_line(self, points):
        points = np.array(points)

        x = points[:, 0]
        y = points[:, 1]

        line_kof = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(line_kof, y, rcond=None)[0]

        distances = np.abs(m * x + c - y) / np.sqrt(m ** 2 + 1)
        is_line = np.sqrt(np.mean(distances ** 2))

        return is_line

    def fire_reg(self):
        current_fire_info = self.all_player_input[-self.Fire_Rate:]
        all_speed = []
        for i in range(1, len(current_fire_info)):
            all_speed.append(self.calc_speed(current_fire_info[i - 1], current_fire_info[i]))

        avg_speed = self.calc_avg(all_speed)
        is_line = self.is_line(current_fire_info)
        fire_offset = self.calc_speed(current_fire_info[len(current_fire_info) - 2], current_fire_info[len(current_fire_info) - 1])

        self.out_data.append([avg_speed, float(is_line), fire_offset])

    def noramlize_data(self, data):
        norm_data = []
        for i in range(len(data)):
            for j in range(len(data[i])):
                norm_data.append(data[i][j])

        return norm_data

    def compile_data(self):
        compile_data = []
        current_data = []
        normalize_data = self.noramlize_data(self.out_data)
        for i in range(len(normalize_data)):
            if i != 0:
                current_data.append(normalize_data[i])
            if i % ((self.Compile_Rate * 3)) == 0 and i != 0:
                compile_data.append(current_data)
                current_data = []

        return compile_data



