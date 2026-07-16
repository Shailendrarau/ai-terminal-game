#!/usr/bin/env python3
"""A simple text-based game on a 5x5 grid."""

import os

# Grid dimensions
GRID_WIDTH = 5
GRID_HEIGHT = 5

# Player starting position (row, col)
player_row = 0
player_col = 0


def draw_grid() -> None:
    """Draw the grid with the player's position marked."""
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if row == player_row and col == player_col:
                print("[P]", end="")
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
    print("Welcome to the Grid Game!")
    print("You are marked as [P] on the grid.")
    print("WASD to move, 'quit' to exit.\n")
    input("Press Enter to start... ")

    while True:
        clear_screen()
        draw_grid()
        print()

        user_input = input("Enter command: ").strip().lower()

        if user_input == "quit":
            print("Thanks for playing!")
            break
        elif user_input in ("w", "a", "s", "d"):
            move_player(user_input)
        else:
            print(f"Unknown command: '{user_input}'\n")


if __name__ == "__main__":
    main()
