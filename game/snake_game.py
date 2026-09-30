"""A turn-based Snake game that is played through GitHub issues.

Each click on a direction link in the profile README opens an issue titled
``snake|<command>``. A workflow runs this script with the title, advances the
game by one step, redraws ``assets/snake-game.svg`` and commits the result.

The issue title comes from the public and is treated as untrusted: only a fixed
allowlist of commands is accepted, and player names are validated as GitHub
logins and XML-escaped before they are drawn.
"""

from __future__ import annotations

import copy
import json
import os
import random
import re
import sys
from pathlib import Path
from typing import Any, Optional
from xml.sax.saxutils import escape

WIDTH, HEIGHT = 20, 12
CELL = 30
BOARD_X, BOARD_Y = 20, 56

DIRECTIONS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
OPPOSITE = {"up": "down", "down": "up", "left": "right", "right": "left"}
COMMANDS = set(DIRECTIONS) | {"new"}

COMMAND_RE = re.compile(r"^snake\|([a-z]+)$")
ACTOR_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,38}$")

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "game" / "state.json"
SVG_PATH = ROOT / "assets" / "snake-game.svg"

State = dict[str, Any]


def parse_command(title: Optional[str]) -> Optional[str]:
    """Return the command for a ``snake|<command>`` title, or None if invalid."""
    if not isinstance(title, str):
        return None
    match = COMMAND_RE.match(title.strip().lower())
    if not match or match.group(1) not in COMMANDS:
        return None
    return match.group(1)


def sanitize_actor(login: Optional[str]) -> str:
    """Accept only a valid GitHub login; anything else becomes 'anonymous'."""
    if isinstance(login, str) and ACTOR_RE.match(login):
        return login
    return "anonymous"


def place_food(snake: list[list[int]], rng: random.Random) -> Optional[list[int]]:
    occupied = {tuple(cell) for cell in snake}
    free = [
        [x, y] for x in range(WIDTH) for y in range(HEIGHT) if (x, y) not in occupied
    ]
    return rng.choice(free) if free else None


def new_state(rng: random.Random, best: int = 0) -> State:
    snake = [[5, 6], [4, 6], [3, 6]]
    return {
        "width": WIDTH,
        "height": HEIGHT,
        "snake": snake,
        "direction": "right",
        "food": place_food(snake, rng),
        "score": 0,
        "best": best,
        "moves": 0,
        "alive": True,
        "won": False,
        "last_player": "",
    }


def apply_move(
    state: State, command: str, actor: str, rng: random.Random
) -> tuple[State, str]:
    """Return the new state and a message for one command."""
    if command == "new":
        fresh = new_state(rng, best=state.get("best", 0))
        fresh["last_player"] = actor
        return fresh, "New game started. Good luck!"

    current = copy.deepcopy(state)
    if not current["alive"]:
        return current, "The game is over. Click **New game** to play again."

    direction = current["direction"]
    if command != OPPOSITE[direction]:
        direction = command
    dx, dy = DIRECTIONS[direction]
    head_x, head_y = current["snake"][0]
    target = [head_x + dx, head_y + dy]

    grows = target == current["food"]
    body = current["snake"] if grows else current["snake"][:-1]
    current["direction"] = direction
    current["moves"] += 1
    current["last_player"] = actor

    out_of_bounds = not (0 <= target[0] < WIDTH and 0 <= target[1] < HEIGHT)
    if out_of_bounds or target in body:
        current["alive"] = False
        return current, f"Game over! Final score: {current['score']}."

    current["snake"].insert(0, target)
    if not grows:
        current["snake"].pop()
        return current, "Moved."

    current["score"] += 1
    current["best"] = max(current["best"], current["score"])
    food = place_food(current["snake"], rng)
    if food is None:
        current["alive"] = False
        current["won"] = True
        return current, f"You filled the board! Final score: {current['score']}."
    current["food"] = food
    return current, f"Ate the food! Score: {current['score']}."


def _segment_color(index: int, length: int) -> str:
    """Blend from bright cyan at the head to deep teal at the tail."""
    ratio = index / max(length - 1, 1)
    start, end = (0x22, 0xD3, 0xEE), (0x0E, 0x74, 0x90)
    red, green, blue = (round(a + (b - a) * ratio) for a, b in zip(start, end))
    return f"#{red:02x}{green:02x}{blue:02x}"


def render_svg(state: State) -> str:
    width = BOARD_X * 2 + WIDTH * CELL
    height = BOARD_Y + HEIGHT * CELL + 52
    board_w, board_h = WIDTH * CELL, HEIGHT * CELL
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" '
        f'aria-label="Snake game, score {state["score"]}">',
        "<style>"
        ".mono{font-family:'JetBrains Mono','SF Mono',Menlo,Consolas,monospace}"
        ".food{animation:pulse 1.4s ease-in-out infinite;transform-box:fill-box;"
        "transform-origin:center}"
        "@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.25)}}"
        "@media (prefers-reduced-motion:reduce){.food{animation:none}}"
        "</style>",
        '<defs><pattern id="g" width="30" height="30" patternUnits="userSpaceOnUse">'
        '<path d="M30 0H0V30" fill="none" stroke="#22d3ee" stroke-opacity="0.08"/>'
        "</pattern></defs>",
        f'<rect width="{width}" height="{height}" rx="14" fill="#0d1117" '
        'stroke="#22d3ee" stroke-opacity="0.35"/>',
        '<text x="20" y="36" class="mono" font-size="16" font-weight="700" '
        'letter-spacing="4" fill="#22d3ee">SNAKE</text>',
        f'<text x="{width - 20}" y="36" class="mono" font-size="15" '
        f'text-anchor="end" fill="#e6edf3">SCORE {state["score"]}'
        f'  ·  BEST {state["best"]}</text>',
        f'<rect x="{BOARD_X}" y="{BOARD_Y}" width="{board_w}" height="{board_h}" '
        'rx="6" fill="#0a0f16"/>',
        f'<rect x="{BOARD_X}" y="{BOARD_Y}" width="{board_w}" height="{board_h}" '
        'rx="6" fill="url(#g)" stroke="#22d3ee" stroke-opacity="0.25"/>',
    ]

    food = state.get("food")
    if food:
        cx = BOARD_X + food[0] * CELL + CELL // 2
        cy = BOARD_Y + food[1] * CELL + CELL // 2
        parts.append(f'<circle class="food" cx="{cx}" cy="{cy}" r="9" fill="#f85149"/>')

    snake = state["snake"]
    for index, (x, y) in enumerate(snake):
        px, py = BOARD_X + x * CELL + 2, BOARD_Y + y * CELL + 2
        parts.append(
            f'<rect x="{px}" y="{py}" width="{CELL - 4}" height="{CELL - 4}" rx="8" '
            f'fill="{_segment_color(index, len(snake))}"/>'
        )
    head_x, head_y = snake[0]
    hx, hy = BOARD_X + head_x * CELL, BOARD_Y + head_y * CELL
    eyes = {
        "right": ((22, 9), (22, 21)),
        "left": ((8, 9), (8, 21)),
        "up": ((9, 8), (21, 8)),
        "down": ((9, 22), (21, 22)),
    }[state["direction"]]
    for ex, ey in eyes:
        parts.append(f'<circle cx="{hx + ex}" cy="{hy + ey}" r="2.6" fill="#0d1117"/>')

    if not state["alive"]:
        title = "YOU WON" if state.get("won") else "GAME OVER"
        parts.append(
            f'<rect x="{BOARD_X}" y="{BOARD_Y}" width="{board_w}" height="{board_h}" '
            'rx="6" fill="#0d1117" fill-opacity="0.72"/>'
            f'<text x="{width // 2}" y="{BOARD_Y + board_h // 2 - 6}" class="mono" '
            'font-size="34" font-weight="800" text-anchor="middle" '
            f'fill="#f85149">{title}</text>'
            f'<text x="{width // 2}" y="{BOARD_Y + board_h // 2 + 26}" class="mono" '
            'font-size="15" text-anchor="middle" fill="#e6edf3">'
            f'final score {state["score"]} · click New game below</text>'
        )

    player = state.get("last_player") or ""
    footer = (
        f'last move by @{escape(player)} · {state["moves"]} moves'
        if player
        else "no moves yet, be the first to play"
    )
    parts.append(
        f'<text x="{width // 2}" y="{height - 18}" class="mono" font-size="13" '
        f'text-anchor="middle" fill="#9fb3c8">{footer}</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def load_state(rng: random.Random) -> State:
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return new_state(rng)


def save(state: State) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SVG_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    SVG_PATH.write_text(render_svg(state), encoding="utf-8")


def main(argv: list[str]) -> int:
    rng = random.Random()
    if "--init" in argv:
        save(new_state(rng))
        return 0

    state = load_state(rng)
    command = parse_command(os.environ.get("TITLE"))
    actor = sanitize_actor(os.environ.get("ACTOR"))

    if command is None:
        message = "That is not a valid move. Use the links in the README."
    else:
        state, message = apply_move(state, command, actor, rng)
        save(state)

    message_file = os.environ.get("MESSAGE_FILE")
    if message_file:
        Path(message_file).write_text(message + "\n", encoding="utf-8")
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
