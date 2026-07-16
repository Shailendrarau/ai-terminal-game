#!/usr/bin/env python3
"""A simple text-based game on a 5x5 grid."""

import os
import random

# Grid dimensions
GRID_WIDTH = 5
GRID_HEIGHT = 5

# Player starting position (row, col)
player_row = 0
player_col = 0

# Score and collectible
score = 0
collectible_row = 0
collectible_col = 0

# Hazard
hazard_row = 0
hazard_col = 0


def spawn_collectible() -> None:
    """Spawn the collectible at a random position not occupied by the player."""
    global collectible_row, collectible_col

    while True:
        collectible_row = random.randint(0, GRID_HEIGHT - 1)
        collectible_col = random.randint(0, GRID_WIDTH - 1)
        if collectible_row != player_row or collectible_col != player_col:
            break


def spawn_hazard() -> None:
    """Spawn the hazard at a random empty position."""
    global hazard_row, hazard_col

    while True:
        hazard_row = random.randint(0, GRID_HEIGHT - 1)
        hazard_col = random.randint(0, GRID_WIDTH - 1)
        if (hazard_row, hazard_col) != (player_row, player_col) and \
           (hazard_row, hazard_col) != (collectible_row, collectible_col):
            break


def draw_grid() -> None:
    """Draw the grid with the player, collectible, and hazard marked."""
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if row == player_row and col == player_col:
                print("[P]", end="")
            elif row == collectible_row and col == collectible_col:
                print("[*]", end="")
            elif row == hazard_row and col == hazard_col:
                print("[X]", end="")
            else:
                print("[.]", end="")
        print()  # New line after each row


def move_player(direction: str) -> None:
    """Move the player in the given direction if within bounds."""
    global player_row, player_col

    if direction == "w" and player_row > 0:
        player_row -= 1
    elif direction == "s" and player_row < GRID_HEIGHT - 1:
        player_row += 1
    elif direction == "a" and player_col > 0:
        player_col -= 1
    elif direction == "d" and player_col < GRID_WIDTH - 1:
        player_col += 1


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def main() -> None:
    """Main game loop."""
    global score

    print("Welcome to the Grid Game!")
    print("[P] = You, [*] = Collectible, [X] = Hazard")
    print("WASD to move, 'quit' to exit.")
    print("Collect 10 items to win! Avoid the hazard!")
    input("Press Enter to start... ")

    spawn_collectible()
    spawn_hazard()

    while True:
        clear_screen()
        print(f"Score: {score}/10")
        draw_grid()
        print()

        user_input = input("Enter command: ").strip().lower()

        if user_input == "quit":
            print("Thanks for playing!")
            break
        elif user_input in ("w", "a", "s", "d"):
            move_player(user_input)

            # Check if player hit the hazard
            if player_row == hazard_row and player_col == hazard_col:
                clear_screen()
                print(f"Score: {score}/10")
                draw_grid()
                print()
                print("Game Over!")
                break

            # Check if player collected the item
            if player_row == collectible_row and player_col == collectible_col:
                score += 1
                if score >= 10:
                    clear_screen()
                    print(f"Score: {score}/10")
                    draw_grid()
                    print()
                    print("You win! You collected 10 items!")
                    break
                spawn_collectible()
        else:
            print(f"Unknown command: '{user_input}'\n")


if __name__ == "__main__":
    main()
