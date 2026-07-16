import game


def setup_function():
    """Reset game state before each test."""
    game.player_row = 0
    game.player_col = 0
    game.score = 0
    game.collectible_row = 4
    game.collectible_col = 4


# --- move_player tests ---

def test_move_right():
    game.move_player("d")
    assert (game.player_row, game.player_col) == (0, 1)


def test_move_left():
    game.player_col = 2
    game.move_player("a")
    assert (game.player_row, game.player_col) == (0, 1)


def test_move_down():
    game.move_player("s")
    assert (game.player_row, game.player_col) == (1, 0)


def test_move_up():
    game.player_row = 2
    game.move_player("w")
    assert (game.player_row, game.player_col) == (1, 0)


def test_boundary_left_at_origin():
    game.move_player("a")
    assert (game.player_row, game.player_col) == (0, 0)


def test_boundary_up_at_origin():
    game.move_player("w")
    assert (game.player_row, game.player_col) == (0, 0)


def test_boundary_right_at_edge():
    game.player_col = 4
    game.move_player("d")
    assert game.player_col == 4


def test_boundary_bottom_at_edge():
    game.player_row = 4
    game.move_player("s")
    assert game.player_row == 4


def test_full_traversal_right_down():
    for _ in range(4):
        game.move_player("d")
    for _ in range(4):
        game.move_player("s")
    assert (game.player_row, game.player_col) == (4, 4)


def test_full_traversal_left_up():
    game.player_row = 4
    game.player_col = 4
    for _ in range(4):
        game.move_player("a")
    for _ in range(4):
        game.move_player("w")
    assert (game.player_row, game.player_col) == (0, 0)


# --- spawn_collectible tests ---

def test_spawn_not_on_player():
    game.player_row = 2
    game.player_col = 2
    for _ in range(50):
        game.spawn_collectible()
        assert (game.collectible_row, game.collectible_col) != (2, 2)


def test_spawn_within_bounds():
    for _ in range(50):
        game.spawn_collectible()
        assert 0 <= game.collectible_row < game.GRID_HEIGHT
        assert 0 <= game.collectible_col < game.GRID_WIDTH


# --- draw_grid tests ---

def test_draw_grid_contains_player(capsys):
    game.draw_grid()
    output = capsys.readouterr().out
    assert "[P]" in output


def test_draw_grid_contains_collectible(capsys):
    game.draw_grid()
    output = capsys.readouterr().out
    assert "[*]" in output


def test_draw_grid_dimensions(capsys):
    game.draw_grid()
    output = capsys.readouterr().out
    lines = output.strip().split("\n")
    assert len(lines) == game.GRID_HEIGHT
    for line in lines:
        cells = line.count("[")
        assert cells == game.GRID_WIDTH


def test_draw_grid_player_at_position(capsys):
    game.player_row = 2
    game.player_col = 3
    game.draw_grid()
    output = capsys.readouterr().out
    lines = output.strip().split("\n")
    assert "[P]" in lines[2]
    assert lines[2].index("[P]") == lines[2].index("[") + 3 * 3
