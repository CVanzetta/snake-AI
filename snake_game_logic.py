# snake_game_logic.py

import random

class SnakeGameLogic:
    def __init__(self, grid_size=10, agent=None):
        self.grid_size = grid_size
        self.snake = [[grid_size // 2, grid_size // 2]]
        self.direction = [0, 1]  # Direction initiale : droite
        self.fruit = self.generate_fruit()
        self.score = 0
        self.agent = agent
        self.running = True
        self.steps = 0  # Pour limiter le nombre de pas sans fin
        self.max_steps = grid_size * grid_size * 4  # Nombre maximum de pas

    def generate_fruit(self):
        while True:
            fruit = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
            if fruit not in self.snake:
                return fruit

    def get_perception(self):
        head = self.snake[0]
        perception = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, Bas, Gauche, Droite
        for dx, dy in directions:
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
        else:
            # Si aucun agent, le serpent continue dans la même direction
            pass

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
