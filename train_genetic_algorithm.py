import os
import random
import pickle
from snake_game_logic import SnakeGameLogic
from agent import Agent

def evaluate_agents(population, grid_size=10, range_vision=2):
    scores = []
    for agent in population:
        game = SnakeGameLogic(grid_size=grid_size, agent=agent, range_vision=range_vision)
        game.play()
        # Calculer la distance moyenne au fruit
        average_distance = game.total_distance_to_fruit / game.steps if game.steps > 0 else 0
        # Calculer le nombre de mouvements répétitifs
        repetitive_moves = game.count_repetitive_moves()
        # Calculer la fitness
        fitness = (game.score * 1000) - (average_distance * 5) - (repetitive_moves * 100)
        scores.append((agent, fitness))
    return scores

def select_agents(scores, selection_ratio=0.2):
    scores.sort(key=lambda x: x[1], reverse=True)
    num_selected = max(2, int(selection_ratio * len(scores)))
    selected = [agent for agent, score in scores[:num_selected]]
    return selected

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1.genome) - 1)
    child_genome = parent1.genome[:crossover_point] + parent2.genome[crossover_point:]
    return Agent(input_size=parent1.input_size, genome=child_genome)

def mutate(agent, mutation_rate=0.1):
    new_genome = []
    for gene in agent.genome:
        if random.random() < mutation_rate:
            gene += random.uniform(-0.5, 0.5)
            gene = max(-1, min(1, gene))
        new_genome.append(gene)
    agent.genome = new_genome

def generate_new_population(selected_agents, population_size, input_size):
    new_population = []
    while len(new_population) < population_size:
        parent1, parent2 = random.sample(selected_agents, 2)
        child = crossover(parent1, parent2)
        mutate(child)
        new_population.append(child)
    # Introduire de nouveaux agents aléatoires pour maintenir la diversité
    num_random_agents = int(0.05 * population_size)
    for _ in range(num_random_agents):
        new_population[random.randint(0, population_size - 1)] = Agent(input_size=input_size)
    return new_population

def train_genetic_algorithm(generations=500, population_size=100, grid_size=10, range_vision=2):
    input_size = ((2 * range_vision + 1) ** 2 - 1) + 2  # Calculer le input_size pour range_vision=2

    population_file = "population_state.pkl"

    if os.path.exists(population_file):
        with open(population_file, "rb") as f:
            population = pickle.load(f)
        print("Population chargée depuis '{}'.".format(population_file))
    else:
        population = [Agent(input_size=input_size) for _ in range(population_size)]
        print("Nouvelle population initialisée.")

    for generation in range(generations):
        print(f"Génération {generation + 1}/{generations}")
        scores = evaluate_agents(population, grid_size=grid_size, range_vision=range_vision)
        best_fitness = max(scores, key=lambda x: x[1])[1]
        average_fitness = sum(score for agent, score in scores) / len(scores)
        print(f"Meilleure fitness : {best_fitness}, Fitness moyenne : {average_fitness}")

        selected_agents = select_agents(scores)
        population = generate_new_population(selected_agents, population_size, input_size)

        # Sauvegarder la population toutes les 10 générations
        if (generation + 1) % 10 == 0:
            with open(population_file, "wb") as f:
                pickle.dump(population, f)
            print(f"Population sauvegardée à la génération {generation + 1}.")

    # Sauvegarder la population à la fin de l'entraînement
    with open(population_file, "wb") as f:
        pickle.dump(population, f)
    print("Population finale sauvegardée dans '{}'.".format(population_file))

    # Sauvegarder le meilleur agent
    scores = evaluate_agents(population, grid_size=grid_size, range_vision=range_vision)
    best_agent = max(scores, key=lambda x: x[1])[0]
    with open("best_agent_genome.txt", "w") as f:
        f.write(",".join(map(str, best_agent.genome)))
    print("Entraînement terminé. Génome du meilleur agent sauvegardé dans 'best_agent_genome.txt'.")

if __name__ == "__main__":
    train_genetic_algorithm()