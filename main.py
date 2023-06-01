import random
import math
from tabulate import tabulate

def generate_route_map(file_path, num_cities_range, road_distance_range):
    num_cities = random.randint(*num_cities_range)
    route_map = [[0] * num_cities for _ in range(num_cities)]

    for i in range(num_cities):
        for j in range(i+1, num_cities):
            distance = random.randint(*road_distance_range)
            route_map[i][j] = distance
            route_map[j][i] = distance

    with open(file_path, 'w') as file:
        file.write(f'{num_cities}\n')
        for row in route_map:
            file.write(' '.join(map(str, row)) + '\n')

def load_route_map(file_path):
    route_map = []

    with open(file_path, 'r') as file:
        num_cities = int(file.readline().strip())
        for _ in range(num_cities):
            row = list(map(int, file.readline().strip().split()))
            route_map.append(row)

    return route_map

def ant_colony_tsp(route_map, num_ants, evaporation_rate, alpha, beta):
    num_cities = len(route_map)
    pheromone = [[1.0] * num_cities for _ in range(num_cities)]
    best_distance = float('inf')
    best_tour = []

    for _ in range(num_ants):
        start_city = random.randint(0, num_cities-1)
        ant = Ant(start_city, num_cities, alpha, beta)

        while not ant.is_completed():
            ant.select_next_city(route_map, pheromone)

        distance = ant.get_total_distance()
        if distance < best_distance:
            best_distance = distance
            best_tour = ant.get_tour()

        ant.update_pheromone(pheromone, distance)

    return best_distance, best_tour

class Ant:
    def __init__(self, start_city, num_cities, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.num_cities = num_cities
        self.visited = [False] * num_cities
        self.visited[start_city] = True
        self.tour = [start_city]
        self.total_distance = 0.0

    def select_next_city(self, route_map, pheromone):
        current_city = self.tour[-1]
        probabilities = [0.0] * self.num_cities
        total = 0.0

        for i in range(self.num_cities):
            if not self.visited[i]:
                probabilities[i] = (
                    math.pow(pheromone[current_city][i], self.alpha)
                    * math.pow(1.0 / route_map[current_city][i], self.beta)
                )
                total += probabilities[i]

        rand = random.uniform(0, total)
        current = 0.0

        for i in range(self.num_cities):
            if not self.visited[i]:
                current += probabilities[i]
                if current >= rand:
                    next_city = i
                    break

        self.visited[next_city] = True
        self.tour.append(next_city)
        self.total_distance += route_map[current_city][next_city]

    def is_completed(self):
        return all(self.visited)

    def get_total_distance(self):
        return self.total_distance

    def get_tour(self):
        return self.tour

    def update_pheromone(self, pheromone, distance):
        evaporation = 1.0 - evaporation_rate

        for i in range(self.num_cities - 1):
            city_a = self.tour[i]
            city_b = self.tour[i+1]
            pheromone[city_a][city_b] = evaporation * pheromone[city_a][city_b] + (1.0 / distance)

        last_city = self.tour[-1]
        first_city = self.tour[0]
        pheromone[last_city][first_city] = evaporation * pheromone[last_city][first_city] + (1.0 / distance)


num_ants = 10
evaporation_rate = 0.5
alpha = 1
beta = 2

generate_route_map('route_map.txt', (25, 35), (10, 100))
route_map = load_route_map('route_map.txt')

simulation_results = []

for simulation in range(10):
    best_distance, best_tour = ant_colony_tsp(route_map, num_ants, evaporation_rate, alpha, beta)
    simulation_results.append([simulation + 1, best_distance, best_tour])

table_headers = ["Simulation", "Best Distance", "Best Tour"]
table = tabulate(simulation_results, headers=table_headers, tablefmt="grid")
print(table)
