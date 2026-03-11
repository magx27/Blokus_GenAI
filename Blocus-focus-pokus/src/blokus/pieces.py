"""Piece definitions and transform helpers."""

from dataclasses import dataclass

Coordinate = tuple[int, int]


@dataclass(frozen=True)
class Transform:
    rotation: int
    flipped: bool
    cells: tuple[Coordinate, ...]


@dataclass(frozen=True)
class PieceDefinition:
    piece_id: str
    cells: tuple[Coordinate, ...]
    transforms: tuple[Transform, ...]

    @property
    def size(self) -> int:
        return len(self.cells)


BASE_PIECE_CELLS: dict[str, tuple[Coordinate, ...]] = {
    "I1": ((0, 0),),
    "I2": ((0, 0), (1, 0)),
    "I3": ((0, 0), (1, 0), (2, 0)),
    "V3": ((0, 0), (0, 1), (1, 1)),
    "I4": ((0, 0), (1, 0), (2, 0), (3, 0)),
    "O4": ((0, 0), (1, 0), (0, 1), (1, 1)),
    "T4": ((0, 0), (1, 0), (2, 0), (1, 1)),
    "L4": ((0, 0), (0, 1), (0, 2), (1, 2)),
    "Z4": ((0, 0), (1, 0), (1, 1), (2, 1)),
    "F5": ((1, 0), (2, 0), (0, 1), (1, 1), (1, 2)),
    "I5": ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)),
    "L5": ((0, 0), (0, 1), (0, 2), (0, 3), (1, 3)),
    "N5": ((0, 0), (1, 0), (1, 1), (2, 1), (3, 1)),
    "P5": ((0, 0), (1, 0), (0, 1), (1, 1), (0, 2)),
    "T5": ((0, 0), (1, 0), (2, 0), (1, 1), (1, 2)),
    "U5": ((0, 0), (2, 0), (0, 1), (1, 1), (2, 1)),
    "V5": ((0, 0), (0, 1), (0, 2), (1, 2), (2, 2)),
    "W5": ((0, 0), (0, 1), (1, 1), (1, 2), (2, 2)),
    "X5": ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    "Y5": ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1)),
    "Z5": ((0, 0), (1, 0), (2, 0), (2, 1), (3, 1)),
}


def normalize_cells(cells: tuple[Coordinate, ...] | list[Coordinate]) -> tuple[Coordinate, ...]:
    min_x = min(x for x, _ in cells)
    min_y = min(y for _, y in cells)
    normalized = sorted((x - min_x, y - min_y) for x, y in cells)
    return tuple(normalized)


def _rotate_clockwise(cells: tuple[Coordinate, ...]) -> tuple[Coordinate, ...]:
    return tuple((y, -x) for x, y in cells)


def _flip_horizontally(cells: tuple[Coordinate, ...]) -> tuple[Coordinate, ...]:
    return tuple((-x, y) for x, y in cells)


def apply_transform(
    cells: tuple[Coordinate, ...],
    rotation: int = 0,
    flipped: bool = False,
) -> tuple[Coordinate, ...]:
    transformed = cells
    if flipped:
        transformed = _flip_horizontally(transformed)
    for _ in range(rotation % 4):
        transformed = _rotate_clockwise(transformed)
    return normalize_cells(transformed)


def _build_transforms(cells: tuple[Coordinate, ...]) -> tuple[Transform, ...]:
    unique: dict[tuple[Coordinate, ...], Transform] = {}
    for flipped in (False, True):
        for rotation in range(4):
            transformed = apply_transform(cells, rotation=rotation, flipped=flipped)
            unique.setdefault(
                transformed,
                Transform(rotation=rotation, flipped=flipped, cells=transformed),
            )
    return tuple(sorted(unique.values(), key=lambda item: (item.cells, item.flipped, item.rotation)))


def _build_piece_catalog() -> dict[str, PieceDefinition]:
    catalog: dict[str, PieceDefinition] = {}
    for piece_id, cells in BASE_PIECE_CELLS.items():
        normalized = normalize_cells(cells)
        catalog[piece_id] = PieceDefinition(
            piece_id=piece_id,
            cells=normalized,
            transforms=_build_transforms(normalized),
        )
    return catalog


PIECES = _build_piece_catalog()


def piece_sort_key(piece_id: str) -> tuple[int, str]:
    return (-PIECES[piece_id].size, piece_id)


PIECE_IDS = tuple(sorted(PIECES, key=piece_sort_key))


def absolute_cells(
    piece_id: str,
    origin: Coordinate,
    rotation: int = 0,
    flipped: bool = False,
) -> tuple[Coordinate, ...]:
    transformed = apply_transform(PIECES[piece_id].cells, rotation=rotation, flipped=flipped)
    origin_x, origin_y = origin
    return tuple(sorted((origin_x + dx, origin_y + dy) for dx, dy in transformed))

