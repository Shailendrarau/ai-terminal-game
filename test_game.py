#!/usr/bin/env python3
"""Tests for the grid game."""

import pytest
import game


@pytest.fixture(autouse=True)
def reset_game_state():
    """Reset global game state before every test."""
    game.reset_state()
    yield


# ── Movement tests ──────────────────────────────────────────────

def test_move_w_increases_row():
    """W moves the player up (row decreases)."""
    game.player_row = 2
    game.player_col = 2
    game.move_player("w")
    assert game.player_row == 1
    assert game.player_col == 2


def test_move_s_decreases_row():
    """S moves the player down (row increases)."""
    game.player_row = 2
    game.player_col = 2
    game.move_player("s")
    assert game.player_row == 3
    assert game.player_col == 2


def test_move_a_decreases_col():
    """A moves the player left (col decreases)."""
    game.player_row = 2
    game.player_col = 2
    game.move_player("a")
    assert game.player_row == 2
    assert game.player_col == 1


def test_move_d_increases_col():
    """D moves the player right (col increases)."""
    game.player_row = 2
    game.player_col = 2
    game.move_player("d")
    assert game.player_row == 2
    assert game.player_col == 3


# ── Boundary tests ──────────────────────────────────────────────

def test_cannot_move_above_top_edge():
    """Can't move up when already at row 0."""
    game.player_row = 0
    game.player_col = 2
    game.move_player("w")
    assert game.player_row == 0


def test_cannot_move_below_bottom_edge():
    """Can't move down when already at the bottom row."""
    game.player_row = game.GRID_HEIGHT - 1
    game.player_col = 2
    game.move_player("s")
    assert game.player_row == game.GRID_HEIGHT - 1


def test_cannot_move_left_of_left_edge():
    """Can't move left when already at col 0."""
    game.player_row = 2
    game.player_col = 0
    game.move_player("a")
    assert game.player_col == 0


def test_cannot_move_right_of_right_edge():
    """Can't move right when already at the rightmost col."""
    game.player_row = 2
    game.player_col = game.GRID_WIDTH - 1
    game.move_player("d")
    assert game.player_col == game.GRID_WIDTH - 1


def test_move_from_top_left_corner():
    """Moving w or a from (0,0) stays at (0,0)."""
    game.player_row = 0
    game.player_col = 0
    game.move_player("w")
    game.move_player("a")
    assert game.player_row == 0
    assert game.player_col == 0


def test_move_from_bottom_right_corner():
    """Moving s or d from bottom-right stays put."""
    game.player_row = game.GRID_HEIGHT - 1
    game.player_col = game.GRID_WIDTH - 1
    game.move_player("s")
    game.move_player("d")
    assert game.player_row == game.GRID_HEIGHT - 1
    assert game.player_col == game.GRID_WIDTH - 1


# ── Collectible spawn tests ─────────────────────────────────────

def test_spawn_collectible_not_on_player():
    """Collectible never spawns on the player."""
    game.player_row = 2
    game.player_col = 2
    for _ in range(200):
        game.spawn_collectible()
        assert (game.collectible_row, game.collectible_col) != (2, 2)


def test_spawn_collectible_within_bounds():
    """Collectible always spawns within grid bounds."""
    for _ in range(200):
        game.spawn_collectible()
        assert 0 <= game.collectible_row < game.GRID_HEIGHT
        assert 0 <= game.collectible_col < game.GRID_WIDTH


# ── Hazard spawn tests ──────────────────────────────────────────

def test_spawn_hazard_not_on_player():
    """Hazard never spawns on the player."""
    game.player_row = 2
    game.player_col = 2
    game.collectible_row = 3
    game.collectible_col = 3
    for _ in range(200):
        game.spawn_hazard()
        assert (game.hazard_row, game.hazard_col) != (2, 2)


def test_spawn_hazard_not_on_collectible():
    """Hazard never spawns on the collectible."""
    game.player_row = 0
    game.player_col = 0
    game.collectible_row = 3
    game.collectible_col = 3
    for _ in range(200):
        game.spawn_hazard()
        assert (game.hazard_row, game.hazard_col) != (3, 3)


def test_spawn_hazard_within_bounds():
    """Hazard always spawns within grid bounds."""
    game.collectible_row = 0
    game.collectible_col = 0
    for _ in range(200):
        game.spawn_hazard()
        assert 0 <= game.hazard_row < game.GRID_HEIGHT
        assert 0 <= game.hazard_col < game.GRID_WIDTH


# ── Draw grid tests ─────────────────────────────────────────────

def test_draw_grid_contains_player(capsys):
    """Drawn grid contains [P] at the player position."""
    game.player_row = 1
    game.player_col = 1
    game.collectible_row = 4
    game.collectible_col = 4
    game.hazard_row = 3
    game.hazard_col = 3
    game.draw_grid()
    output = capsys.readouterr().out
    assert "[P]" in output


def test_draw_grid_contains_collectible(capsys):
    """Drawn grid contains [*] at the collectible position."""
    game.player_row = 0
    game.player_col = 0
    game.collectible_row = 2
    game.collectible_col = 2
    game.hazard_row = 4
    game.hazard_col = 4
    game.draw_grid()
    output = capsys.readouterr().out
    assert "[*]" in output


def test_draw_grid_contains_hazard(capsys):
    """Drawn grid contains [X] at the hazard position."""
    game.player_row = 0
    game.player_col = 0
    game.collectible_row = 1
    game.collectible_col = 1
    game.hazard_row = 2
    game.hazard_col = 2
    game.draw_grid()
    output = capsys.readouterr().out
    assert "[X]" in output


def test_draw_grid_has_correct_dimensions(capsys):
    """Drawn grid has exactly 5 rows and 5 tiles per row."""
    game.player_row = 0
    game.player_col = 0
    game.collectible_row = 1
    game.collectible_col = 1
    game.hazard_row = 2
    game.hazard_col = 2
    game.draw_grid()
    output = capsys.readouterr().out
    lines = output.strip().split("\n")
    assert len(lines) == game.GRID_HEIGHT
    for line in lines:
        assert line.count("[") == game.GRID_WIDTH


def test_draw_grid_no_overlap(capsys):
    """Player, collectible, and hazard each appear exactly once."""
    game.player_row = 0
    game.player_col = 0
    game.collectible_row = 2
    game.collectible_col = 2
    game.hazard_row = 4
    game.hazard_col = 4
    game.draw_grid()
    output = capsys.readouterr().out
    assert output.count("[P]") == 1
    assert output.count("[*]") == 1
    assert output.count("[X]") == 1


# ── Scoring tests ───────────────────────────────────────────────

def test_score_starts_at_zero():
    """Score starts at 0."""
    assert game.score == 0


def test_collectible_pickup_increments_score():
    """Moving onto the collectible increments the score."""
    game.player_row = 1
    game.player_col = 1
    game.collectible_row = 1
    game.collectible_col = 2
    game.move_player("d")
    if game.player_row == game.collectible_row and game.player_col == game.collectible_col:
        game.score += 1
    assert game.score == 1


def test_win_condition_at_10():
    """Score of 10 triggers the win condition."""
    game.score = 9
    game.score += 1
    assert game.score >= 10


def test_no_win_below_10():
    """Score below 10 does not trigger the win condition."""
    game.score = 9
    assert game.score < 10


def test_hazard_terminates_game():
    """Stepping on the hazard should cause a game over."""
    game.player_row = 1
    game.player_col = 1
    game.hazard_row = 1
    game.hazard_col = 2
    game.move_player("d")
    assert game.player_row == game.hazard_row
    assert game.player_col == game.hazard_col


# ── Reset state tests ───────────────────────────────────────────

def test_reset_state_clears_player():
    """Reset puts player back at (0,0)."""
    game.player_row = 4
    game.player_col = 4
    game.reset_state()
    assert game.player_row == 0
    assert game.player_col == 0


def test_reset_state_clears_score():
    """Reset sets score back to 0."""
    game.score = 7
    game.reset_state()
    assert game.score == 0


def test_reset_state_clears_collectible():
    """Reset clears collectible position."""
    game.collectible_row = 3
    game.collectible_col = 3
    game.reset_state()
    assert game.collectible_row == 0
    assert game.collectible_col == 0


def test_reset_state_clears_hazard():
    """Reset clears hazard position."""
    game.hazard_row = 2
    game.hazard_col = 2
    game.reset_state()
    assert game.hazard_row == 0
    assert game.hazard_col == 0


def test_reset_state_all_at_once():
    """Reset clears everything in one call."""
    game.player_row = 4
    game.player_col = 4
    game.score = 9
    game.collectible_row = 3
    game.collectible_col = 3
    game.hazard_row = 2
    game.hazard_col = 2
    game.reset_state()
    assert game.player_row == 0
    assert game.player_col == 0
    assert game.score == 0
    assert game.collectible_row == 0
    assert game.collectible_col == 0
    assert game.hazard_row == 0
    assert game.hazard_col == 0


# ── Show end screen tests ───────────────────────────────────────

def test_show_end_screen_displays_message(capsys):
    """End screen prints the given message."""
    game.score = 5
    game.player_row = 0
    game.player_col = 0
    game.collectible_row = 1
    game.collectible_col = 1
    game.hazard_row = 2
    game.hazard_col = 2
    game.show_end_screen("Game Over!")
    output = capsys.readouterr().out
    assert "Game Over!" in output


def test_show_end_screen_displays_score(capsys):
    """End screen prints the current score."""
    game.score = 8
    game.player_row = 0
    game.player_col = 0
    game.collectible_row = 1
    game.collectible_col = 1
    game.hazard_row = 2
    game.hazard_col = 2
    game.show_end_screen("You win!")
    output = capsys.readouterr().out
    assert "Score: 8/10" in output


def test_show_end_screen_displays_grid(capsys):
    """End screen prints the grid."""
    game.player_row = 1
    game.player_col = 1
    game.collectible_row = 3
    game.collectible_col = 3
    game.hazard_row = 4
    game.hazard_col = 4
    game.show_end_screen("Game Over!")
    output = capsys.readouterr().out
    assert "[P]" in output
    assert "[*]" in output
    assert "[X]" in output


# ── Play again tests ────────────────────────────────────────────

def test_play_again_returns_true_for_y(monkeypatch):
    """play_again returns True when user enters 'y'."""
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert game.play_again() is True


def test_play_again_returns_true_for_uppercase_y(monkeypatch):
    """play_again returns True for uppercase 'Y'."""
    monkeypatch.setattr("builtins.input", lambda _: "Y")
    assert game.play_again() is True


def test_play_again_returns_false_for_n(monkeypatch):
    """play_again returns False when user enters 'n'."""
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert game.play_again() is False


def test_play_again_returns_false_for_uppercase_n(monkeypatch):
    """play_again returns False for uppercase 'N'."""
    monkeypatch.setattr("builtins.input", lambda _: "N")
    assert game.play_again() is False


def test_play_again_retries_on_invalid_input(monkeypatch):
    """play_again reprompts on bad input, then accepts valid input."""
    inputs = iter(["maybe", "sure", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert game.play_again() is False


def test_play_again_retries_before_accepting_y(monkeypatch):
    """play_again reprompts on bad input, then accepts 'y'."""
    inputs = iter(["abc", "123", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert game.play_again() is True
