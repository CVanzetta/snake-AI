# train_genetic_algorithm.py

from snake_game_logic import SnakeGameLogic
from agent import Agent
import random

def evaluate_agents(population, grid_size=10):
    scores = []
    for agent in population:
        game = SnakeGameLogic(grid_size=grid_size, agent=agent)
        game.play()
        # La fitness peut être le score multiplié par un facteur
        fitness = game.score * 1000 + game.steps
        scores.append((agent, fitness))
    return scores

def select_agents(scores, selection_ratio=0.2):
    # Trier les agents par fitness décroissante
    scores.sort(key=lambda x: x[1], reverse=True)
    num_selected = max(2, int(selection_ratio * len(scores)))
    selected = [agent for agent, score in scores[:num_selected]]
    return selected

def crossover(parent1, parent2):
    # Croisement à un point
    crossover_point = random.randint(1, parent1.genome_length - 1)
    child_genome = parent1.genome[:crossover_point] + parent2.genome[crossover_point:]
    return Agent(genome=child_genome)

def mutate(agent, mutation_rate=0.1):
    # Muter le génome de l'agent
    new_genome = []
    for gene in agent.genome:
        if random.random() < mutation_rate:
            gene += random.uniform(-0.5, 0.5)
            gene = max(-1, min(1, gene))
        new_genome.append(gene)
    agent.genome = new_genome

def generate_new_population(selected_agents, population_size):
    new_population = []
    while len(new_population) < population_size:
        parent1, parent2 = random.sample(selected_agents, 2)
        child = crossover(parent1, parent2)
        mutate(child)
        new_population.append(child)
    return new_population

def train_genetic_algorithm(generations=50, population_size=50, grid_size=10):
    # Initialisation de la population
    population = [Agent() for _ in range(population_size)]

    for generation in range(generations):
        print(f"Génération {generation + 1}")
        # Évaluation des agents
        scores = evaluate_agents(population, grid_size=grid_size)
        # Meilleure fitness pour le suivi
        best_fitness = max(scores, key=lambda x: x[1])[1]
        print(f"Meilleure fitness : {best_fitness}")
        # Sélection des agents
        selected_agents = select_agents(scores)
        # Génération de la nouvelle population
        population = generate_new_population(selected_agents, population_size)

    # Après l'entraînement, retourner le meilleur agent
    scores = evaluate_agents(population, grid_size=grid_size)
    best_agent = max(scores, key=lambda x: x[1])[0]
    return best_agent

if __name__ == "__main__":
    best_agent = train_genetic_algorithm()
    # Sauvegarder le meilleur agent
    with open("best_agent_genome.txt", "w") as f:
        f.write(",".join(map(str, best_agent.genome)))
    print("Entraînement terminé. Génome du meilleur agent sauvegardé dans 'best_agent_genome.txt'.")
