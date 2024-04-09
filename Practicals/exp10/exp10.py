
import numpy as np
import random

# Function to calculate the distance between two cities
def distance(city1, city2):
    return np.linalg.norm(city1 - city2)

# Function to calculate the total distance of a route
def total_distance(route, cities):
    total = 0
    for i in range(len(route) - 1):
        total += distance(cities[route[i]], cities[route[i+1]])
    total += distance(cities[route[-1]], cities[route[0]])  # Return to the starting city
    return total

# Function to initialize the population
def initialize_population(num_routes, num_cities):
    population = []
    for _ in range(num_routes):
        route = list(range(num_cities))
        random.shuffle(route)
        population.append(route)
    return population

# Function to perform tournament selection
def tournament_selection(population, fitness_values, tournament_size):
    selected_parents = []
    for _ in range(len(population)):
        tournament_indices = random.sample(range(len(population)), tournament_size)
        tournament_fitness = [fitness_values[i] for i in tournament_indices]
        winner_index = tournament_indices[np.argmin(tournament_fitness)]
        selected_parents.append(population[winner_index])
    return selected_parents

# Function to perform ordered crossover
def ordered_crossover(parent1, parent2):
    size = len(parent1)
    start = random.randint(0, size - 1)
    end = random.randint(start + 1, size)
    offspring = [None] * size
    for i in range(start, end):
        offspring[i] = parent1[i]
    remaining = [item for item in parent2 if item not in offspring]
    j = 0
    for i in range(size):
        if offspring[i] is None:
            offspring[i] = remaining[j]
            j += 1
    return offspring

# Function to perform mutation
def mutate(route, mutation_rate):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]
    return route

# Function to replace the current population with the offspring
def replace(population, offspring, fitness_values):
    combined_population = list(zip(population, fitness_values))
    combined_population.sort(key=lambda x: x[1])
    combined_population[:len(offspring)] = zip(offspring, [total_distance(route, cities) for route in offspring])
    combined_population.sort(key=lambda x: x[1])
    new_population, _ = zip(*combined_population)
    return new_population

# Main genetic algorithm function
def genetic_algorithm_TSP(cities, num_routes, max_generations, tournament_size, mutation_rate):
    num_cities = len(cities)
    population = initialize_population(num_routes, num_cities)
    for generation in range(max_generations):
        fitness_values = [total_distance(route, cities) for route in population]
        selected_parents = tournament_selection(population, fitness_values, tournament_size)
        offspring = [ordered_crossover(parent1, parent2) for parent1, parent2 in zip(selected_parents[::2], selected_parents[1::2])]
        offspring = [mutate(route, mutation_rate) for route in offspring]
        population = replace(population, offspring, fitness_values)
    best_route = population[0]
    return best_route

# Input from the user
def get_city_coordinates(num_cities):
    cities = []
    for i in range(num_cities):
        x, y = map(int, input(f"Enter coordinates for city {i+1} (format: x y): ").split())
        cities.append([x, y])
    return np.array(cities)

# Example usage
if __name__ == "__main__":
    # Input number of cities from the user
    num_cities = int(input("Enter the number of cities: "))
    cities = get_city_coordinates(num_cities)

    # Parameters
    num_routes = 50
    max_generations = 1000
    tournament_size = 3
    mutation_rate = 0.01

    # Run genetic algorithm
    best_route = genetic_algorithm_TSP(cities, num_routes, max_generations, tournament_size, mutation_rate)
    print("Best Route:", best_route)
    print("Total Distance:", total_distance(best_route, cities))