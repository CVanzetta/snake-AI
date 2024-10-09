# snake_game_logic.py

import random

class SnakeGameLogic:
    def __init__(self, grid_size=10, agent=None, range_vision=1):
        self.grid_size = grid_size
        self.snake = [
            [grid_size // 2, grid_size // 2],
            [grid_size // 2, grid_size // 2 - 1],
            [grid_size // 2, grid_size // 2 - 2]
        ]
        self.direction = [0, 1]  # Mouvement initial vers la droite
        self.fruit = self.generate_fruit()
        self.score = 0
        self.agent = agent
        self.running = True
        self.steps = 0
        self.max_steps = grid_size * grid_size * 4
        self.range_vision = range_vision  # Ajout du paramètre range_vision

    def generate_fruit(self):
        while True:
            fruit = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
            if fruit not in self.snake:
                return fruit

    def get_perception(self):
        head = self.snake[0]
        perception = []
        for dx in range(-self.range_vision, self.range_vision + 1):
            for dy in range(-self.range_vision, self.range_vision + 1):
                if dx == 0 and dy == 0:
                    continue  # Ignorer la position de la tête du serpent
                x, y = head[0] + dx, head[1] + dy
                if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
                    perception.append(-1)  # Mur
                elif [x, y] in self.snake:
                    perception.append(-1)  # Corps du serpent
                elif [x, y] == self.fruit:
                    perception.append(1)   # Fruit
                else:
                    perception.append(0)   # Case vide
        return perception

    def update(self):
        if not self.running:
            return

        # Obtenir la décision de l'agent
        if self.agent is not None:
            perception = self.get_perception()
            action_index = self.agent.decide(perception)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            self.direction = directions[action_index]

        # Mise à jour de la position du serpent
        new_head = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]

        # Vérification des collisions
        if (
            new_head in self.snake
            or new_head[0] < 0
            or new_head[0] >= self.grid_size
            or new_head[1] < 0
            or new_head[1] >= self.grid_size
        ):
            self.running = False
            return

        # Déplacement du serpent
        self.snake.insert(0, new_head)

        # Vérification si le fruit est mangé
        if new_head == self.fruit:
            self.score += 1
            self.fruit = self.generate_fruit()
        else:
            self.snake.pop()  # Retirer la queue

        self.steps += 1
        if self.steps >= self.max_steps:
            self.running = False  # Arrêter si trop de pas

    def play(self):
        while self.running:
            self.update()
