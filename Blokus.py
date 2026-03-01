import tkinter as tk
from functools import partial

#### Here we define the pieces of the game, we can later add more pieces and also the logic to rotate and flip them.
pieces = {
    "one": [(0, 0)],

    "two_horizontal": [(0, 0), (0, 1)],
    "two_vertical":   [(0, 0), (1, 0)],

    "three_line":     [(0, 0), (0, 1), (0, 2)],
    "three_L":        [(0, 0), (1, 0), (1, 1)]
}

#### Here we call the functions for the game
class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Blokus 20x20 board")

        self.board = Board(self)   
        self.players = [Player("red"), Player("blue"), Player("green"), Player("yellow")]
        self.current_player = self.players[0]
        self.selected_piece = "one"   # for now we just select one piece, but we can later implement a UI to select different pieces just like the game

    def select_piece(self, piece_name):
        self.selected_piece = piece_name

    def on_click(self, row, col):
        if self.selected_piece:
            if self.board.place_piece(self.selected_piece, row, col, self.current_player.color, self.current_player):
                self.switch_player()

    def start(self):
        self.root.mainloop()
    
    def switch_player(self):
        # Move to the next player in the list
        index = self.players.index(self.current_player)
        self.current_player = self.players[(index + 1) % len(self.players)]
        print(f"Now it's {self.current_player.color}'s turn")

class Board:
    def __init__(self, game):
        self.game = game
        self.buttons = self.create_board()

    def create_board(self):
        buttons = []
        for i in range(20):
            row_buttons = []
            for j in range(20):
                btn = tk.Button(
                    self.game.root,
                    text=f"{i,j}",  # para tenerlo numerado
                    width=4,
                    height=1,
                    command=lambda r=i, c=j: self.game.on_click(r, c)
                )
                btn.grid(row=i, column=j)
                row_buttons.append(btn)
            buttons.append(row_buttons)
        return buttons

    def place_piece(self, selected_piece, row, col, color, player):
        piece = pieces[selected_piece]

        # 0. FIRST MOVE RULE: must cover ANY corner
        if not player.has_played:
            corners = [(0, 0), (0, 19), (19, 0), (19, 19)]
            covers_corner = False

            for dr, dc in piece:
                r = row + dr
                c = col + dc
                if (r, c) in corners:
                    covers_corner = True
                    break

            if not covers_corner:
                print("First move must cover ANY corner of the board!")
                return False

        # 1. Check bounds
        for dr, dc in piece:
            r = row + dr
            c = col + dc
            if not (0 <= r < 20 and 0 <= c < 20):
                print("Piece goes out of bounds!")
                return False

        # 2. Check overlap
        for dr, dc in piece:
            r = row + dr
            c = col + dc
            if self.buttons[r][c]["bg"] != "SystemButtonFace":
                print("Cell already occupied!")
                return False

        # 3. Blokus rule: only apply AFTER first move
        if player.has_played:
            touches_corner = False

            for dr, dc in piece:
                r = row + dr
                c = col + dc

                # Edge neighbors (forbidden)
                edge_neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
                for nr, nc in edge_neighbors:
                    if 0 <= nr < 20 and 0 <= nc < 20:
                        if self.buttons[nr][nc]["bg"] == color:
                            print("Cannot touch your own piece on an edge!")
                            return False

                # Corner neighbors (required)
                corner_neighbors = [(r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)]
                for nr, nc in corner_neighbors:
                    if 0 <= nr < 20 and 0 <= nc < 20:
                        if self.buttons[nr][nc]["bg"] == color:
                            touches_corner = True

            if not touches_corner:
                print("Must touch your own piece at a corner!")
                return False

        # 4. Place the piece
        for dr, dc in piece:
            r = row + dr
            c = col + dc
            self.buttons[r][c].config(bg=color)

        # Mark first move as done
        player.has_played = True
        return True


class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = ["one", "two_horizontal", "three_L"]
        self.has_played = False

    def select_piece(self):
        # For now we just return the same piece, but we can later implement a UI to select different pieces just like the game
        return pieces["three_L"]


game = Game()
game.start()