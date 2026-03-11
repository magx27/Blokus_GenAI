import unittest

from blokus.pieces import PIECES


class PieceCatalogTests(unittest.TestCase):
    def test_catalog_contains_all_phase_one_pieces(self) -> None:
        self.assertEqual(len(PIECES), 21)

    def test_total_square_count_matches_classic_set(self) -> None:
        self.assertEqual(sum(piece.size for piece in PIECES.values()), 89)

    def test_transform_counts_cover_key_symmetry_cases(self) -> None:
        self.assertEqual(len(PIECES["I5"].transforms), 2)
        self.assertEqual(len(PIECES["O4"].transforms), 1)
        self.assertEqual(len(PIECES["X5"].transforms), 1)
        self.assertEqual(len(PIECES["T4"].transforms), 4)
        self.assertEqual(len(PIECES["F5"].transforms), 8)


if __name__ == "__main__":
    unittest.main()

