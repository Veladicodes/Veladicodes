"""Tests for the README snake game logic."""

import random
import sys
from pathlib import Path
from xml.dom import minidom

sys.path.insert(0, str(Path(__file__).parent))

import snake_game as game  # noqa: E402


def make_state(snake, direction="right", food=(10, 10), **overrides):
    state = {
        "width": game.WIDTH,
        "height": game.HEIGHT,
        "snake": [list(cell) for cell in snake],
        "direction": direction,
        "food": list(food),
        "score": 0,
        "best": 0,
        "moves": 0,
        "alive": True,
        "last_player": "",
    }
    state.update(overrides)
    return state


def rng():
    return random.Random(7)


def test_new_state_is_valid():
    state = game.new_state(rng())
    assert state["alive"] is True
    assert len(state["snake"]) == 3
    for x, y in state["snake"]:
        assert 0 <= x < game.WIDTH and 0 <= y < game.HEIGHT
    assert state["food"] not in state["snake"]
    assert state["score"] == 0


def test_moving_forward_advances_head_and_keeps_length():
    state = make_state([[5, 5], [4, 5], [3, 5]])
    new, _ = game.apply_move(state, "right", "alice", rng())
    assert new["snake"][0] == [6, 5]
    assert len(new["snake"]) == 3
    assert new["moves"] == 1
    assert new["last_player"] == "alice"


def test_turning_changes_direction():
    state = make_state([[5, 5], [4, 5], [3, 5]])
    new, _ = game.apply_move(state, "up", "bob", rng())
    assert new["direction"] == "up"
    assert new["snake"][0] == [5, 4]


def test_reversing_is_ignored_and_snake_continues():
    state = make_state([[5, 5], [4, 5], [3, 5]], direction="right")
    new, _ = game.apply_move(state, "left", "bob", rng())
    assert new["direction"] == "right"
    assert new["snake"][0] == [6, 5]
    assert new["alive"] is True


def test_eating_food_grows_scores_and_respawns_food():
    state = make_state([[5, 5], [4, 5], [3, 5]], food=(6, 5))
    new, _ = game.apply_move(state, "right", "carol", rng())
    assert len(new["snake"]) == 4
    assert new["score"] == 1
    assert new["best"] == 1
    assert new["food"] not in new["snake"]
    assert new["food"] != [6, 5]


def test_hitting_a_wall_ends_the_game():
    state = make_state([[game.WIDTH - 1, 5], [game.WIDTH - 2, 5], [game.WIDTH - 3, 5]])
    new, message = game.apply_move(state, "right", "dave", rng())
    assert new["alive"] is False
    assert "game over" in message.lower()


def test_hitting_itself_ends_the_game():
    snake = [[5, 5], [5, 6], [4, 6], [4, 5], [4, 4], [5, 4], [6, 4]]
    state = make_state(snake, direction="up")
    new, _ = game.apply_move(state, "up", "erin", rng())
    # head moves to (5, 4): a body cell that is not the tail, so it is a collision
    assert new["alive"] is False


def test_moving_into_the_cell_the_tail_just_left_is_allowed():
    snake = [[2, 1], [2, 2], [1, 2], [1, 1]]
    state = make_state(snake, direction="up", food=(15, 9))
    new, _ = game.apply_move(state, "left", "fay", rng())
    assert new["alive"] is True
    assert new["snake"][0] == [1, 1]


def test_dead_game_ignores_moves_until_new_game():
    state = make_state([[5, 5], [4, 5], [3, 5]], alive=False, score=4, best=9)
    same, message = game.apply_move(state, "up", "gus", rng())
    assert same["snake"] == state["snake"]
    assert "new game" in message.lower()


def test_new_game_resets_but_keeps_best_score():
    state = make_state([[5, 5], [4, 5], [3, 5]], alive=False, score=4, best=9)
    fresh, _ = game.apply_move(state, "new", "hal", rng())
    assert fresh["alive"] is True
    assert fresh["score"] == 0
    assert fresh["best"] == 9


def test_parse_command_accepts_only_the_allowlist():
    assert game.parse_command("snake|up") == "up"
    assert game.parse_command("  snake|DOWN ") == "down"
    assert game.parse_command("snake|new") == "new"
    assert game.parse_command("snake|up; rm -rf /") is None
    assert game.parse_command("snake|") is None
    assert game.parse_command("hello") is None
    assert game.parse_command("") is None
    assert game.parse_command(None) is None


def test_sanitize_actor_rejects_anything_that_is_not_a_github_login():
    assert game.sanitize_actor("octocat") == "octocat"
    assert game.sanitize_actor("a-b-1") == "a-b-1"
    assert game.sanitize_actor("<script>") == "anonymous"
    assert game.sanitize_actor("x" * 60) == "anonymous"
    assert game.sanitize_actor("") == "anonymous"


def test_render_svg_is_well_formed_and_shows_the_score():
    state = make_state([[5, 5], [4, 5], [3, 5]], score=3, best=8, last_player="octocat")
    svg = game.render_svg(state)
    minidom.parseString(svg)  # raises if the XML is malformed
    assert "SCORE 3" in svg
    assert "BEST 8" in svg
    assert "@octocat" in svg


def test_render_svg_escapes_hostile_player_names():
    state = make_state([[5, 5], [4, 5], [3, 5]], last_player="<b>x</b>")
    svg = game.render_svg(state)
    minidom.parseString(svg)
    assert "<b>x</b>" not in svg
