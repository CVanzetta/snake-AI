# snake_game.py

import tkinter as tk
from snake_game_logic import SnakeGameLogic
from agent import Agent

# Charger le génome du meilleur agent
with open("best_agent_genome.txt", "r") as f:
    genome_str = f.read()
best_genome = list(map(float, genome_str.strip().split(",")))
best_agent = Agent(genome=best_genome)

class SnakeGameGUI:
    def __init__(self, root, agent, grid_size=10, cell_size=30):
        self.root = root
        self.root.title("Snake Game avec IA")
        self.canvas = tk.Canvas(root, width=grid_size * cell_size, height=grid_size * cell_size, bg="white")
        self.canvas.pack()
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.agent = agent
        self.game = SnakeGameLogic(grid_size=grid_size, agent=agent)
        self.delay_time = 200  # Temps en millisecondes
        self.running = True
        self.draw()
        self.update()

    def draw(self):
        self.canvas.delete("all")
        # Dessiner le serpent
        for i, segment in enumerate(self.game.snake):
            x, y = segment[1] * self.cell_size, segment[0] * self.cell_size
            if i == 0:  # Tête du serpent
                self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="darkgreen")
            else:
                self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size, fill="green")
        # Dessiner le fruit
        fx, fy = self.game.fruit[1] * self.cell_size, self.game.fruit[0] * self.cell_size
        self.canvas.create_oval(fx, fy, fx + self.cell_size, fy + self.cell_size, fill="red")
        # Afficher le score
        self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.game.score}", fill="black", font=("Arial", 14))

    def update(self):
        if self.game.running:
            self.game.update()
            self.draw()
            self.root.after(self.delay_time, self.update)
        else:
            self.canvas.create_text(
                self.grid_size * self.cell_size // 2,
                self.grid_size * self.cell_size // 2,
                text="Game Over",
                fill="red",
                font=("Arial", 24)
            )
            self.canvas.create_text(
                self.grid_size * self.cell_size // 2,
                self.grid_size * self.cell_size // 2 + 30,
                text=f"Score final: {self.game.score}",
                fill="black",
                font=("Arial", 16)
            )

if __name__ == "__main__":
    root = tk.Tk()
    game_gui = SnakeGameGUI(root, best_agent)
    root.mainloop()
