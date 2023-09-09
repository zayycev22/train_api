import time

from utils.annealing import Annealing
import json
import numpy as np
from pprint import pprint


def matrix_sum(matrix: list[list[int]]):
    return np.matrix(matrix).sum()


def wagons(matrix: list[list[int]], ways: list[list[int]], situation: dict) -> dict:
    ks = list(situation['full_timetable'].keys())
    take_wags = [[0 for _ in range(len(way) - 1)] for way in ways]
    answer = {}
    for way_idx in range(len(ways)):
        for route_idx in range(len(ways[way_idx]) - 1):
            row, col = ways[way_idx][route_idx], ways[way_idx][route_idx + 1]
            train = situation['full_timetable'][ks[way_idx]]
            poss_carriage = int(train["free_carriage"][route_idx])
            if poss_carriage > 0 and matrix[row][col] > 0:
                if matrix[row][col] - poss_carriage >= 0:
                    matrix[row][col] -= poss_carriage
                    matrix[col][row] += poss_carriage
                    train["free_carriage"][route_idx] = '0'
                else:
                    raz = abs(matrix[row][col] - poss_carriage)
                    poss_carriage -= raz
                    matrix[row][col] -= poss_carriage
                    matrix[col][row] += poss_carriage
                    train["free_carriage"][route_idx] = str(raz)
                take_wags[way_idx][route_idx] = poss_carriage
        answer[ks[way_idx]] = {
            "way": list(map(lambda x: x + 1, ways[way_idx])),
            "take_carriage": take_wags[way_idx]
        }
    print(sum(list(map(lambda x: sum(x), take_wags))))
    #print(take_wags)
    return answer


if __name__ == '__main__':
    with open("../files/situations.json", 'r', encoding='utf-8') as f:
        datas = json.loads(f.read())

    start = time.time()
    for data in datas:
        annealing = Annealing(data)
        # pprint(annealing.create_ways(data))
        annealing.main_func()
        print(annealing.current_ways, abs(sum(annealing.energy(annealing.current_ways))))
        # pprint(annealing.full_map)
        pprint(wagons(annealing.full_map, annealing.current_ways, data))
    print("time", time.time() - start)
