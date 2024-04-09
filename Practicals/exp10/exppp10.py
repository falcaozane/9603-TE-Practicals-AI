import random
import numpy as np


cities = {
    'A': (4,9),
    'B': (6,9),
    'C': (3,7),
    'D': (70,5),
    'E': (75,3)
}

# Genetic Algorithm parameters
population_size = 50
generations = 1000
mutation_rate = 0.01

def calculate_distance(route):
    total_distance = 0
    for i in range(len(route) - 1):
        city1, city2 = route[i], route[i + 1]
        total_distance += np.linalg.norm(np.array(cities[city1]) - np.array(cities[city2]))
    return total_distance

def generate_initial_population():
    population = []
    cities_list = list(cities.keys())
    
    for _ in range(population_size):
        route = random.sample(cities_list, len(cities_list))
        population.append(route)
    
    return population

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + [city for city in parent2 if city not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [city for city in parent1 if city not in parent2[:crossover_point]]
    
    return child1, child2

def mutate(route):
    if random.random() < mutation_rate:
        mutation_point1, mutation_point2 = random.sample(range(len(route)), 2)
        route[mutation_point1], route[mutation_point2] = route[mutation_point2], route[mutation_point1]
    
    return route

def genetic_algorithm():
    population = generate_initial_population()

    for generation in range(generations):
        population = sorted(population, key=lambda x: calculate_distance(x))
        new_population = []

        for _ in range(int(population_size/2)):
            parent1, parent2 = random.sample(population[:10], 2)  # Select top 10 as parents
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.extend([child1, child2])

        population = new_population

    best_route = min(population, key=lambda x: calculate_distance(x))
    min_distance = calculate_distance(best_route)

    print(f"Best Route: {best_route}")
    print(f"Total Distance: {min_distance}")

if __name__ == "__main__":
    genetic_algorithm()