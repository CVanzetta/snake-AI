# 🐍🎮 + 🤖 Snake Game with AI Agent

This project implements a classic 🐍 game with an 🤖 agent that uses a 🧠 neural network to make decisions. The 🤖 is trained through a 🧬 genetic algorithm and then tested in the 🎮 environment.

## Overview 🔍

The project consists of three main components:

1. **SnakeGameLogic**: Implements the 🎮 mechanics for the 🐍, including the grid, snake movement, and 🍎 generation.
2. **Agent**: The 🤖 agent that controls the 🐍, using a simple 🧠 neural network to decide movements based on the current 🎮 state.
3. **SnakeGameGUI**: Provides a 🎨 graphical interface for visualizing the 🎮 and the agent's actions.

## How It Works 🛠️

- The agent receives a perception of the 🌍, which includes ℹ️ about the position of obstacles (⛔️), the direction of the 🐍, and the relative position of the 🍎.
- The agent's decision-making is based on a 🧠 neural network whose weights are optimized through 🧬 genetic algorithms.

## Known Issue ⚠️

An issue is currently open due to difficulties encountered when extending the agent's perception to a range of 2️⃣. When the `range_vision` is set to 2️⃣, the agent tends to perform poorly, resulting in immediate 🎮 termination with a score of 0️⃣. This issue needs further investigation to understand the underlying cause and to improve the agent's performance with an extended perception range.

## Running the Game ▶️

To run the 🎮 with the current best-trained 🤖:

```bash
python snake_game_gui.py
```

The 🎮 will start with the 🤖 controlling the 🐍. The objective for the agent is to eat as many 🍎 as possible without colliding with obstacles (⬛️) or itself.

## Opening an Issue 📝

To report problems or contribute to the solution of the existing issue regarding the `range_vision`, please visit the [GitHub Issues page](https://github.com/your-repository/issues) and participate in the discussion.

## Requirements 📋

- Python 3.x
- Tkinter (for the 🎨 graphical interface)

## Future Work 🚀

- Improve the agent's 🧠 neural network to effectively handle an extended perception range.
- Experiment with different 🧠 network architectures to achieve better performance.
- Address the current issue with `range_vision` of 2️⃣, ensuring stability and improved 🎮 behavior.

## Contributing 🤝

Feel free to contribute to the project by opening pull requests or by providing suggestions on the Issues page.
