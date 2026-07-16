#!/usr/bin/env python3
"""A simple text-based game on a 5x5 grid."""

import os
import random

# Grid dimensions
GRID_WIDTH = 5
GRID_HEIGHT = 5

# Theme
GAME_NAME = "[Dark Rider Dragon]"
STORY_INTRO = "[a dragon fearless night ]"
PLAYER_EMOJI = "🦊"
COLLECTIBLE_EMOJI = "🚀"
HAZARD_EMOJI = "🌋"
WIN_MESSAGE = "WOHO ! YOU WIN"
LOSE_MESSAGE = "opps you lose"

# Game state
player_row = 0
player_col = 0
score = 0
collectible_row = 0
collectible_col = 0
hazard_row = 0
hazard_col = 0


def reset_state() -> None:
    """Reset all game state for a new round."""
    global player_row, player_col, score
    global collectible_row, collectible_col
    global hazard_row, hazard_col

    player_row = 0
    player_col = 0
    score = 0
    collectible_row = 0
    collectible_col = 0
    hazard_row = 0
    hazard_col = 0


def spawn_collectible() -> None:
    """Spawn the collectible at a random position not occupied by the player."""
    global collectible_row, collectible_col

    while True:
        collectible_row = random.randint(0, GRID_HEIGHT - 1)
        collectible_col = random.randint(0, GRID_WIDTH - 1)
        if (collectible_row, collectible_col) != (player_row, player_col):
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
                print(f"[{PLAYER_EMOJI}]", end="")
            elif row == collectible_row and col == collectible_col:
                print(f"[{COLLECTIBLE_EMOJI}]", end="")
            elif row == hazard_row and col == hazard_col:
                print(f"[{HAZARD_EMOJI}]", end="")
            else:
                print("[.]", end="")
        print()


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


def show_end_screen(message: str) -> None:
    """Display the final grid and end-of-game message."""
    clear_screen()
    print(f"Score: {score}/10")
    draw_grid()
    print()
    print(message)


def play_again() -> bool:
    """Prompt the user to play again. Returns True if yes, False if no."""
    while True:
        choice = input("Play again? (y/n): ").strip().lower()
        if choice == "y":
            return True
        elif choice == "n":
            return False
        print("Please enter 'y' or 'n'.")


def run_game() -> None:
    """Run a single round of the game."""
    global score

    reset_state()
    spawn_collectible()
    spawn_hazard()

    while True:
        clear_screen()
        print(f"Score: {score}/10")
        draw_grid()
        print()

        user_input = input("Enter command: ").strip().lower()

        if user_input == "quit":
            raise SystemExit

        if user_input in ("w", "a", "s", "d"):
            move_player(user_input)

            # Check hazard collision
            if player_row == hazard_row and player_col == hazard_col:
                show_end_screen(LOSE_MESSAGE)
                return

            # Check collectible pickup
            if player_row == collectible_row and player_col == collectible_col:
                score += 1
                if score >= 10:
                    show_end_screen(WIN_MESSAGE)
                    return
                spawn_collectible()


def main() -> None:
    """Top-level game loop with play-again support."""
    print(f"=== {GAME_NAME} ===")
    print()
    print(STORY_INTRO)
    print()
    print(f"{PLAYER_EMOJI} = You, {COLLECTIBLE_EMOJI} = Collectible, {HAZARD_EMOJI} = Hazard")
    print("WASD to move, 'quit' to exit.")
    print("Collect 10 items to win! Avoid the hazard!")
    input("Press Enter to start... ")

    while True:
        run_game()
        if not play_again():
            break

    clear_screen()
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
