import game


def setup_function():
    """Reset player position before each test."""
    game.player_row = 0
    game.player_col = 0


def test_move_right():
    game.move_player("d")
    assert game.player_row == 0
    assert game.player_col == 1


def test_move_down():
    game.move_player("s")
    assert game.player_row == 1
    assert game.player_col == 0


def test_move_left_blocked_at_origin():
    game.move_player("a")
    assert game.player_col == 0


def test_move_up_blocked_at_origin():
    game.move_player("w")
    assert game.player_row == 0


def test_move_right_then_left():
    game.move_player("d")
    game.move_player("a")
    assert game.player_col == 0


def test_move_down_then_up():
    game.move_player("s")
    game.move_player("w")
    assert game.player_row == 0


def test_boundary_right():
    for _ in range(4):
        game.move_player("d")
    assert game.player_col == 4
    game.move_player("d")
    assert game.player_col == 4


def test_boundary_bottom():
    for _ in range(4):
        game.move_player("s")
    assert game.player_row == 4
    game.move_player("s")
    assert game.player_row == 4


def test_full_traversal():
    for _ in range(4):
        game.move_player("d")
    for _ in range(4):
        game.move_player("s")
    assert game.player_row == 4
    assert game.player_col == 4


def test_draw_grid_output(capsys):
    game.draw_grid()
    captured = capsys.readouterr().out
    assert "[P]" in captured
    assert "[.]" in captured
    lines = captured.strip().split("\n")
    assert len(lines) == game.GRID_HEIGHT
    assert lines[0].startswith("[P]")
