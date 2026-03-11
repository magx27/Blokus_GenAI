"""Mode and symbol configuration."""

from dataclasses import dataclass

Coordinate = tuple[int, int]


@dataclass(frozen=True)
class ModeConfig:
    name: str
    board_size: int
    players: tuple[str, ...]
    start_corners: dict[str, Coordinate]


CLASSIC_CONFIG = ModeConfig(
    name="classic",
    board_size=20,
    players=("blue", "yellow", "red", "green"),
    start_corners={
        "blue": (0, 0),
        "yellow": (19, 0),
        "red": (19, 19),
        "green": (0, 19),
    },
)

MODE_CONFIGS = {
    CLASSIC_CONFIG.name: CLASSIC_CONFIG,
}

PLAYER_SYMBOLS = {
    "blue": "B",
    "yellow": "Y",
    "red": "R",
    "green": "G",
    "orange": "O",
}

SYMBOL_PLAYERS = {symbol: player for player, symbol in PLAYER_SYMBOLS.items()}


def get_mode_config(name: str) -> ModeConfig:
    try:
        return MODE_CONFIGS[name]
    except KeyError as exc:
        supported = ", ".join(sorted(MODE_CONFIGS))
        raise ValueError(f"Unsupported mode '{name}'. Supported modes: {supported}.") from exc


def symbol_for_player(player: str) -> str:
    try:
        return PLAYER_SYMBOLS[player]
    except KeyError as exc:
        raise ValueError(f"No board symbol configured for player '{player}'.") from exc


def player_for_symbol(symbol: str) -> str:
    try:
        return SYMBOL_PLAYERS[symbol]
    except KeyError as exc:
        raise ValueError(f"No player configured for board symbol '{symbol}'.") from exc

