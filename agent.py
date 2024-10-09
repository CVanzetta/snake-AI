# agent.py

import random
import math

class Agent:
    def __init__(self, input_size, hidden_size=10, genome=None):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = 4  # 4 actions possibles: haut, bas, gauche, droite
        self.genome_length = (self.input_size * self.hidden_size) + (self.hidden_size * self.output_size)
        
        if genome is None:
            # Initialisation aléatoire du génome
            self.genome = [random.uniform(-1, 1) for _ in range(self.genome_length)]
        else:
            self.genome = genome

        # Décomposer le génome en poids pour les couches
        self.decode_genome()

    def decode_genome(self):
        # Extraire les poids du génome
        ih_end = self.input_size * self.hidden_size
        ho_end = ih_end + self.hidden_size * self.output_size
        self.weights_input_hidden = self.genome[:ih_end]
        self.weights_hidden_output = self.genome[ih_end:ho_end]

    def decide(self, perception):
        # Propagation vers l'avant dans le réseau de neurones
        # Entrée -> Couche cachée
        hidden = []
        for i in range(self.hidden_size):
            weight_start = i * self.input_size
            weight_end = weight_start + self.input_size
            weights = self.weights_input_hidden[weight_start:weight_end]
            activation = sum(p * w for p, w in zip(perception, weights))
            hidden.append(self.sigmoid(activation))

        # Couche cachée -> Sortie
        outputs = []
        for i in range(self.output_size):
            weight_start = i * self.hidden_size
            weight_end = weight_start + self.hidden_size
            weights = self.weights_hidden_output[weight_start:weight_end]
            activation = sum(h * w for h, w in zip(hidden, weights))
            outputs.append(activation)

        # Sélectionner l'action avec la valeur maximale
        max_value = max(outputs)
        best_actions = [i for i, v in enumerate(outputs) if v == max_value]
        action_index = random.choice(best_actions)
        return action_index

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
