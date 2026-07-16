# Dark Rider Dragon

A terminal-based grid game built in Python where you play as a fearless dragon navigating a 5x5 grid, collecting items while avoiding hazards.

## Story

> *[a dragon fearless night ]*

You are the Dark Rider Dragon — a swift fox-like creature soaring through a dangerous grid world. Collect 10 rocket-powered items scattered across the terrain, but beware: volcanic hazards lurk on the map, and stepping on one means instant defeat.

## Features

- **WASD Movement** — Navigate the 5x5 grid using classic WASD controls
- **Collectible System** — Pick up rockets to increase your score
- **Hazard Tiles** — Avoid volcanic hazards or face game over
- **Win/Lose Conditions** — Score 10 to win, hit a hazard to lose
- **Play Again** — After each round, choose to replay or exit
- **Custom Theme** — Styled with emojis and a narrative intro
- **Clean Terminal UI** — Screen clears and re-renders each turn

## How to Run

### Start the Game

```bash
python game.py
```

### Run Tests

```bash
pytest test_game.py -v
```

## Controls

| Key | Action |
|-----|--------|
| `w` | Move up |
| `a` | Move left |
| `s` | Move down |
| `d` | Move right |
| `quit` | Exit the game |

## Project Structure

```
ai-terminal-game/
├── game.py          # Main game logic and loop
├── test_game.py     # Pytest test suite (39 tests)
└── README.md        # This file
```

## What I Learned

- **Iterative Development** — Built the game in stages: grid, movement, collectibles, hazards, theming, and play-again logic. Each step was tested before moving to the next.
- **Engineering Prompts to Prevent Regression** — Wrote clear, specific prompts for each feature addition to ensure existing functionality wasn't broken by new changes.
- **Automated Testing with Pytest** — Used pytest fixtures, monkeypatching, and capsys to test movement, boundaries, spawning, rendering, and user input without manual verification.

## Author

Built with Python 3.11 and a lot of ☕
