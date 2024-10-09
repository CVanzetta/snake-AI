# agent.py

import random

class Agent:
    def __init__(self, genome=None):
        self.genome_length = 4  # Nombre de poids correspondant aux entrées de perception
        if genome is None:
            # Initialisation aléatoire du génome (poids entre -1 et 1)
            self.genome = [random.uniform(-1, 1) for _ in range(self.genome_length)]
        else:
            self.genome = genome

    def decide(self, perception):
        # Calculer la somme pondérée de la perception
        action_values = [p * w for p, w in zip(perception, self.genome)]
        # Sélectionner l'action avec la valeur maximale
        max_value = max(action_values)
        best_actions = [i for i, v in enumerate(action_values) if v == max_value]
        action_index = random.choice(best_actions)
        return action_index  # 0: Haut, 1: Bas, 2: Gauche, 3: Droite
