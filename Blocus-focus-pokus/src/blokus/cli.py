"""Command-line interface for the Blokus engine."""

from argparse import ArgumentParser, Namespace
import json
from pathlib import Path
import sys

from blokus.config import get_mode_config
from blokus.engine import apply_move, list_legal_moves, new_game, pass_turn, validate_move
from blokus.evaluate import main as evaluate_main
from blokus.models import GameState, Move
from blokus.players import choose_simple_move
from blokus.render import render_state


def _load_state(path: str) -> GameState:
    with Path(path).open("r", encoding="utf-8") as handle:
        return GameState.from_dict(json.load(handle))


def _dump_json(payload: dict[str, object], output_path: str | None) -> None:
    if output_path:
        with Path(output_path).open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
        return
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def _parse_controllers(mode: str, value: str | None) -> dict[str, str]:
    players = get_mode_config(mode).players
    if value is None:
        return {player: "human" for player in players}
    parsed = tuple(part.strip().lower() for part in value.split(",") if part.strip())
    if len(parsed) != len(players):
        raise ValueError(
            f"Mode '{mode}' expects {len(players)} controller types, got {len(parsed)}."
        )
    for controller in parsed:
        if controller not in {"human", "computer"}:
            raise ValueError("Controller types must be 'human' or 'computer'.")
    return {player: controller for player, controller in zip(players, parsed)}


def _move_from_args(state: GameState, args: Namespace) -> Move:
    return Move(
        player=args.player or state.current_player,
        piece=args.piece,
        x=args.x,
        y=args.y,
        rotation=args.rotation,
        flipped=args.flipped,
    )


def cmd_new(args: Namespace) -> int:
    controllers = _parse_controllers(args.mode, args.players)
    state = new_game(mode=args.mode, controllers=controllers)
    _dump_json(state.to_dict(), args.output)
    return 0


def cmd_show(args: Namespace) -> int:
    print(render_state(_load_state(args.state)))
    return 0


def cmd_validate(args: Namespace) -> int:
    state = _load_state(args.state)
    result = validate_move(state, _move_from_args(state, args))
    print(result.reason)
    return 0 if result.ok else 1


def cmd_apply(args: Namespace) -> int:
    state = _load_state(args.state)
    move = _move_from_args(state, args)
    result = validate_move(state, move)
    if not result.ok:
        print(result.reason)
        return 1
    new_state = apply_move(state, move)
    _dump_json(new_state.to_dict(), args.output)
    return 0


def cmd_pass_turn(args: Namespace) -> int:
    state = _load_state(args.state)
    try:
        new_state = pass_turn(state, player=args.player or state.current_player)
    except ValueError as exc:
        print(str(exc))
        return 1
    _dump_json(new_state.to_dict(), args.output)
    return 0


def cmd_legal_moves(args: Namespace) -> int:
    state = _load_state(args.state)
    moves = list_legal_moves(state, player=args.player, limit=args.limit)
    if args.json:
        _dump_json({"moves": [move.to_dict() for move in moves]}, args.output)
    else:
        for move in moves:
            print(
                f"{move.player}: {move.piece} @ ({move.x}, {move.y}) "
                f"rotation={move.rotation} flipped={move.flipped}"
            )
    return 0


def cmd_suggest(args: Namespace) -> int:
    state = _load_state(args.state)
    player = args.player or state.current_player
    move = choose_simple_move(state, player=player)
    if move is None:
        print(f"No legal move exists for {player}.")
        return 1
    if args.json:
        _dump_json(move.to_dict(), args.output)
    else:
        print(
            f"{move.player}: {move.piece} @ ({move.x}, {move.y}) "
            f"rotation={move.rotation} flipped={move.flipped}"
        )
    return 0


def _handle_human_turn(state: GameState) -> GameState | None:
    print(render_state(state))
    print(
        "\nEnter one of: "
        "'move PIECE X Y ROTATION FLIPPED(0|1)', "
        "'legal [N]', 'pass', 'show', 'quit'."
    )
    while True:
        raw = input(f"{state.current_player}> ").strip()
        if not raw:
            continue
        if raw == "quit":
            return None
        if raw == "show":
            print(render_state(state))
            continue
        if raw.startswith("legal"):
            parts = raw.split()
            limit = int(parts[1]) if len(parts) > 1 else 10
            moves = list_legal_moves(state, limit=limit)
            if not moves:
                print("No legal moves.")
            else:
                for move in moves:
                    print(
                        f"{move.piece} @ ({move.x}, {move.y}) "
                        f"rotation={move.rotation} flipped={move.flipped}"
                    )
            continue
        if raw == "pass":
            try:
                return pass_turn(state)
            except ValueError as exc:
                print(str(exc))
                continue
        if raw.startswith("move "):
            parts = raw.split()
            if len(parts) != 6:
                print("Expected exactly: move PIECE X Y ROTATION FLIPPED")
                continue
            move = Move(
                player=state.current_player,
                piece=parts[1],
                x=int(parts[2]),
                y=int(parts[3]),
                rotation=int(parts[4]),
                flipped=bool(int(parts[5])),
            )
            result = validate_move(state, move)
            if not result.ok:
                print(result.reason)
                continue
            return apply_move(state, move)
        print("Unsupported command.")


def cmd_play(args: Namespace) -> int:
    if args.state:
        state = _load_state(args.state)
    else:
        state = new_game(mode=args.mode, controllers=_parse_controllers(args.mode, args.players))

    max_turns = args.max_turns
    turns = 0
    while not state.finished and (max_turns is None or turns < max_turns):
        controller = state.controller_types.get(state.current_player, "human")
        if controller == "computer":
            move = choose_simple_move(state)
            if move is None:
                print(f"{state.current_player} passes.")
                state = pass_turn(state)
            else:
                print(
                    f"{state.current_player} plays {move.piece} at ({move.x}, {move.y}) "
                    f"rotation={move.rotation} flipped={move.flipped}"
                )
                state = apply_move(state, move)
        else:
            maybe_state = _handle_human_turn(state)
            if maybe_state is None:
                if args.output:
                    _dump_json(state.to_dict(), args.output)
                return 0
            state = maybe_state
        turns += 1

    print(render_state(state))
    if args.output:
        _dump_json(state.to_dict(), args.output)
    return 0


def cmd_evaluate(_: Namespace) -> int:
    return evaluate_main()


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(prog="blokus", description="Blokus Classic Phase 1 CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="Create a new game state.")
    new_parser.add_argument("--mode", default="classic")
    new_parser.add_argument("--players", help="Comma-separated controllers, e.g. human,computer,computer,computer")
    new_parser.add_argument("--output", help="Write the JSON state to this path.")
    new_parser.set_defaults(func=cmd_new)

    show_parser = subparsers.add_parser("show", help="Render a saved game state.")
    show_parser.add_argument("--state", required=True)
    show_parser.set_defaults(func=cmd_show)

    validate_parser = subparsers.add_parser("validate", help="Validate a proposed move.")
    validate_parser.add_argument("--state", required=True)
    validate_parser.add_argument("--player")
    validate_parser.add_argument("--piece", required=True)
    validate_parser.add_argument("--x", required=True, type=int)
    validate_parser.add_argument("--y", required=True, type=int)
    validate_parser.add_argument("--rotation", type=int, default=0)
    validate_parser.add_argument("--flipped", action="store_true")
    validate_parser.set_defaults(func=cmd_validate)

    apply_parser = subparsers.add_parser("apply", help="Apply a legal move and print the new state.")
    apply_parser.add_argument("--state", required=True)
    apply_parser.add_argument("--player")
    apply_parser.add_argument("--piece", required=True)
    apply_parser.add_argument("--x", required=True, type=int)
    apply_parser.add_argument("--y", required=True, type=int)
    apply_parser.add_argument("--rotation", type=int, default=0)
    apply_parser.add_argument("--flipped", action="store_true")
    apply_parser.add_argument("--output", help="Write the JSON state to this path.")
    apply_parser.set_defaults(func=cmd_apply)

    pass_parser = subparsers.add_parser("pass-turn", help="Pass when no legal move exists.")
    pass_parser.add_argument("--state", required=True)
    pass_parser.add_argument("--player")
    pass_parser.add_argument("--output", help="Write the JSON state to this path.")
    pass_parser.set_defaults(func=cmd_pass_turn)

    legal_parser = subparsers.add_parser("legal-moves", help="List legal moves for a player.")
    legal_parser.add_argument("--state", required=True)
    legal_parser.add_argument("--player")
    legal_parser.add_argument("--limit", type=int)
    legal_parser.add_argument("--json", action="store_true")
    legal_parser.add_argument("--output", help="Write JSON output to this path.")
    legal_parser.set_defaults(func=cmd_legal_moves)

    suggest_parser = subparsers.add_parser("suggest", help="Choose a simple computer move.")
    suggest_parser.add_argument("--state", required=True)
    suggest_parser.add_argument("--player")
    suggest_parser.add_argument("--json", action="store_true")
    suggest_parser.add_argument("--output", help="Write JSON output to this path.")
    suggest_parser.set_defaults(func=cmd_suggest)

    play_parser = subparsers.add_parser("play", help="Play interactively or run computer-vs-computer turns.")
    play_parser.add_argument("--mode", default="classic")
    play_parser.add_argument("--players", help="Comma-separated controllers, e.g. human,computer,computer,computer")
    play_parser.add_argument("--state", help="Resume from an existing JSON state.")
    play_parser.add_argument("--max-turns", type=int)
    play_parser.add_argument("--output", help="Write the final state to this path.")
    play_parser.set_defaults(func=cmd_play)

    evaluate_parser = subparsers.add_parser("evaluate", help="Run the fixture-backed evaluation harness.")
    evaluate_parser.set_defaults(func=cmd_evaluate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValueError as exc:
        print(str(exc))
        return 1

