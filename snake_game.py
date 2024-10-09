import random
import curses

# Taille de la grille
grid_size = 10

# Initialisation de la fenêtre Curses
def init_window():
    window = curses.initscr()
    curses.curs_set(0)
    window.timeout(100)
    window.keypad(1)
    window.nodelay(1)
    return window

# Fonction pour générer un nouveau fruit sur la grille
def generate_fruit(snake):
    while True:
        fruit = [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)]
        if fruit not in snake:
            return fruit

# Fonction principale du jeu
def main(window):
    # Position initiale du serpent et direction
    snake = [[5, 5]]
    direction = [0, 1]  # Début vers la droite
    fruit = generate_fruit(snake)
    score = 0

    # Boucle principale du jeu
    while True:
        window.clear()

        # Affichage de la grille
        for y in range(grid_size):
            for x in range(grid_size):
                if [y, x] in snake:
                    window.addch(y, x * 2, '#')  # Représentation du serpent
                elif [y, x] == fruit:
                    window.addch(y, x * 2, 'F')  # Représentation du fruit
                else:
                    window.addch(y, x * 2, '.')  # Représentation d'une case vide

        # Affichage du score
        window.addstr(grid_size, 0, f'Score: {score}')

        # Gestion des entrées utilisateur
        key = window.getch()
        if key == curses.KEY_UP and direction != [1, 0]:
            direction = [-1, 0]
        elif key == curses.KEY_DOWN and direction != [-1, 0]:
            direction = [1, 0]
        elif key == curses.KEY_LEFT and direction != [0, 1]:
            direction = [0, -1]
        elif key == curses.KEY_RIGHT and direction != [0, -1]:
            direction = [0, 1]

        # Calcul de la nouvelle position de la tête du serpent
        new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

        # Conditions de fin de jeu : collision avec le mur ou avec soi-même
        if (
            new_head in snake
            or new_head[0] < 0
            or new_head[0] >= grid_size
            or new_head[1] < 0
            or new_head[1] >= grid_size
        ):
            window.clear()
            window.addstr(grid_size // 2, grid_size - 5, 'GAME OVER')
            window.addstr(grid_size // 2 + 1, grid_size - 7, f'Final Score: {score}')
            window.refresh()
            window.getch()
            break

        # Ajout de la nouvelle tête au serpent
        snake.insert(0, new_head)

        # Si le serpent mange un fruit, on génère un nouveau fruit
        if new_head == fruit:
            fruit = generate_fruit(snake)
            score += 1
        else:
            snake.pop()  # Retirer la queue du serpent si aucun fruit mangé

        # Vérification de la victoire (si le serpent remplit toute la grille)
        if len(snake) == grid_size * grid_size:
            window.clear()
            window.addstr(grid_size // 2, grid_size - 5, 'YOU WIN!')
            window.addstr(grid_size // 2 + 1, grid_size - 7, f'Final Score: {score}')
            window.refresh()
            window.getch()
            break

        window.refresh()

# Début du programme
if __name__ == "__main__":
    try:
        window = init_window()
        main(window)
    finally:
        curses.endwin()