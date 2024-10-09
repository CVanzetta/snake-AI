import random
import tkinter as tk
import time

# Taille de la grille
grid_size = 10
cell_size = 30

delay_time = 200  # Temps d'attente entre les mouvements pour éviter les changements trop rapides

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size, bg="white")
        self.canvas.pack()
        self.direction = [0, 1]
        self.snake = [[5, 5], [5, 4], [5, 3]]  # Commence avec 3 segments
        self.fruit = self.generate_fruit()
        self.score = 0
        self.running = True
        self.last_key_press_time = time.time()
        self.root.bind("<KeyPress>", self.change_direction)
        self.update()

    def generate_fruit(self):
        while True:
            fruit = [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)]
            if fruit not in self.snake:
                return fruit

    def change_direction(self, event):
        current_time = time.time()
        if current_time - self.last_key_press_time < delay_time / 1000:
            return  # Ignore les touches si elles sont pressées trop rapidement
        
        self.last_key_press_time = current_time
        if event.keysym == "Up" and self.direction != [1, 0]:
            self.direction = [-1, 0]
        elif event.keysym == "Down" and self.direction != [-1, 0]:
            self.direction = [1, 0]
        elif event.keysym == "Left" and self.direction != [0, 1]:
            self.direction = [0, -1]
        elif event.keysym == "Right" and self.direction != [0, -1]:
            self.direction = [0, 1]

    def update(self):
        if not self.running:
            return

        # Calcul de la nouvelle position de la tête du serpent
        new_head = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]

        # Conditions de fin de jeu : collision avec le mur ou avec soi-même
        if (
            new_head in self.snake
            or new_head[0] < 0
            or new_head[0] >= grid_size
            or new_head[1] < 0
            or new_head[1] >= grid_size
        ):
            self.game_over()
            return

        # Ajout de la nouvelle tête au serpent
        self.snake.insert(0, new_head)

        # Si le serpent mange un fruit, on génère un nouveau fruit
        if new_head == self.fruit:
            self.fruit = self.generate_fruit()
            self.score += 1
        else:
            self.snake.pop()  # Retirer la queue du serpent si aucun fruit mangé

        # Vérification de la victoire (si le serpent remplit toute la grille)
        if len(self.snake) == grid_size * grid_size:
            self.win()
            return

        self.draw()
        self.root.after(delay_time, self.update)

    def draw(self):
        self.canvas.delete("all")

        # Affichage du serpent
        for i, segment in enumerate(self.snake):
            x, y = segment[1] * cell_size, segment[0] * cell_size
            if i == 0:  # La tête du serpent
                self.canvas.create_oval(x, y, x + cell_size, y + cell_size, fill="darkgreen")
            else:
                self.canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill="green")

        # Affichage du fruit
        fx, fy = self.fruit[1] * cell_size, self.fruit[0] * cell_size
        self.canvas.create_oval(fx, fy, fx + cell_size, fy + cell_size, fill="red")

        # Affichage du score
        self.canvas.create_text(50, 10, anchor="nw", text=f"Score: {self.score}", fill="black", font=("Arial", 14))

    def game_over(self):
        self.running = False
        self.canvas.create_text(grid_size * cell_size // 2, grid_size * cell_size // 2, text="GAME OVER", fill="red", font=("Arial", 24))
        self.canvas.create_text(grid_size * cell_size // 2, grid_size * cell_size // 2 + 30, text=f"Final Score: {self.score}", fill="black", font=("Arial", 16))

    def win(self):
        self.running = False
        self.canvas.create_text(grid_size * cell_size // 2, grid_size * cell_size // 2, text="YOU WIN!", fill="blue", font=("Arial", 24))
        self.canvas.create_text(grid_size * cell_size // 2, grid_size * cell_size // 2 + 30, text=f"Final Score: {self.score}", fill="black", font=("Arial", 16))

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()