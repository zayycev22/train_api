import datetime
import math
from random import shuffle, randint, uniform


def time_diff(time: str) -> float:
    start_time_str, end_time_str = time.split(' - ')
    start_time = datetime.datetime.strptime(start_time_str, '%H:%M')
    end_time = datetime.datetime.strptime(end_time_str, '%H:%M')
    return (end_time - start_time).total_seconds() / 60


def total_time(intervals: list[str]):
    res = 0
    for interval in intervals:
        res += time_diff(interval)
    return res


def create_start_way() -> list:
    ans = list(range(0, 6))
    shuffle(ans)
    return ans


class Annealing:
    TEMP: float = 100

    def __init__(self, situation: dict, initial_temp: float = 1000, end_temp: float = 0.1):
        self._full_map = self.parse_situation(situation)
        self.TEMP = initial_temp
        self._end_temp = end_temp
        self._train_maps = self.parse_trains_matrix(situation)
        self.start_ways = self.create_ways(situation)
        self.current_ways = self.start_ways.copy()

    @staticmethod
    def parse_situation(situation: dict) -> list:
        station_matrix = []
        for key in situation['stations']:
            station_matrix.append(list(map(int, situation['stations'][key])))
        return station_matrix

    @staticmethod
    def parse_trains_matrix(situation: dict) -> list:
        trains_map = []
        for key in situation['full_timetable'].keys():
            train = situation['full_timetable'][key]
            matrix = [[0 for _ in range(7)] for _ in range(7)]
            for i in range(len(train['route']) - 1):
                route = int(train['route'][i]) - 1
                route_to = int(train['route'][i + 1]) - 1
                matrix[route][route_to] = (int(train['free_carriage'][i]), time_diff(train["timetable"][i]))
            trains_map.append(matrix)
        return trains_map

    @property
    def train_maps(self):
        return self._train_maps

    @property
    def full_map(self):
        return self._full_map

    def delta(self, ways1, ways2):
        return sum(self.energy(ways2)) - sum(self.energy(ways1))

    def get_length(self, row, col):
        return self._full_map[row][col]

    def change_way(self, ways: list[list]):
        for way in ways:
            if len(way) > 3:
                i1 = 0
                i2 = 0
                while i1 == i2:
                    i1 = randint(1, len(way) - 2)
                    i2 = randint(1, len(way) - 2)
                way[i1], way[i2] = way[i2], way[i1]
                # 0 1 2 3 4

    def get_temp(self, temp):
        return temp * 0.5

    def energy(self, ways: list[list]) -> list:
        engs = []
        for way in ways:
            sm1 = 0
            for i in range(len(way) - 1):
                sm1 += self.get_length(way[i], way[i + 1])
            engs.append(sm1 * -1)
        return engs

    def percentage(self, cur_temp, ways1, ways2):
        p = self.TEMP * math.exp(-1 * (self.delta(ways1, ways2) / self.get_temp(cur_temp)))
        return p

    @staticmethod
    def create_ways(situation: dict) -> list:
        ways = []
        for train in situation['full_timetable'].keys():
            route = list(map(lambda x: x - 1, list(map(int, situation['full_timetable'][train]['route']))))
            ways.append(route)
        return ways

    def main_func(self, iteration=0, replay=0, temp: float = TEMP):
        if iteration + replay >= 900 or temp <= 0.001:
            #print("Finished", self.current_ways, abs(sum(self.energy(self.current_ways))),
                  #temp, iteration, replay)
            return
        new_ways = self.current_ways.copy()
        self.change_way(new_ways)
        e1 = self.energy(self.current_ways)
        e2 = self.energy(new_ways)
        if sum(e2) < sum(e1):
            temp = self.get_temp(temp)
            self.main_func(iteration + 1, replay, temp)
        else:
            if uniform(0, 100) < self.percentage(temp, self.current_ways, new_ways):
                temp = self.get_temp(temp)
                self.main_func(iteration + 1, replay, temp)
            else:
                self.main_func(iteration, replay + 1, temp)
        return self.current_ways, self.energy(self.current_ways)
