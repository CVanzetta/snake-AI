import random

class SnakeGameLogic:
    def __init__(self, grid_size=10, agent=None, range_vision=2):
        self.grid_size = grid_size
        self.range_vision = range_vision
        center = grid_size // 2
        self.snake = [
            [center, center],
            [center, center - 1],
            [center, center - 2]
        ]
        self.direction = [0, 1]  # Mouvement initial vers la droite
        self.fruit = self.generate_fruit()
        self.score = 0
        self.agent = agent
        self.running = True
        self.steps = 0
        self.max_steps = grid_size * grid_size * 4
        self.total_distance_to_fruit = 0
        self.last_moves = []
        self.max_last_moves = 4
        self.collisions = 0  # Nouveau compteur pour suivre les collisions

    def generate_fruit(self):
        while True:
            fruit = [random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)]
            if fruit not in self.snake:
                return fruit

    def get_perception(self):
        head = self.snake[0]
        perception = []

        # Ajouter la direction actuelle du serpent
        perception.extend(self.direction)

        # Ajouter la direction relative du fruit
        fruit_direction = [
            (self.fruit[0] - head[0]) / self.grid_size,  # Différence normalisée en X
            (self.fruit[1] - head[1]) / self.grid_size   # Différence normalisée en Y
        ]
        perception.extend(fruit_direction)

        # Capteurs pour les obstacles dans les directions cardinales (haut, bas, gauche, droite)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            x, y = head[0] + dx, head[1] + dy
            if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size or [x, y] in self.snake:
                perception.append(1)  # Obstacle
            else:
                perception.append(0)  # Pas d'obstacle

        return perception

    def update(self):
        if not self.running:
            return

        # Obtenir la décision de l'agent
        if self.agent is not None:
            perception = self.get_perception()
            action_index = self.agent.decide(perception)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Haut, Bas, Gauche, Droite
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
            self.collisions += 1
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

        # Mise à jour de la distance totale au fruit
        head = self.snake[0]
        distance = abs(head[0] - self.fruit[0]) + abs(head[1] - self.fruit[1])
        self.total_distance_to_fruit += distance

        # Enregistrement des derniers mouvements pour détecter les répétitions
        self.last_moves.append(self.direction)
        if len(self.last_moves) > self.max_last_moves:
            self.last_moves.pop(0)

        self.steps += 1
        if self.steps >= self.max_steps:
            self.running = False  # Arrêter si trop de pas

    def count_repetitive_moves(self):
        # Compter le nombre de fois où les derniers mouvements sont identiques
        if len(self.last_moves) < self.max_last_moves:
            return 0
        else:
            return sum(1 for move in self.last_moves if move == self.last_moves[0]) == self.max_last_moves

    def play(self):
        while self.running:
            self.update()
        print(f"Partie terminée. Score: {self.score}, Steps: {self.steps}, Collisions: {self.collisions}")