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
        self.selected_piece = "three_L"   # for now we just select one piece, but we can later implement a UI to select different pieces just like the game

    def select_piece(self, piece_name):
        self.selected_piece = piece_name

    def on_click(self, row, col):
        if self.selected_piece:
            self.board.place_piece(self.selected_piece, row, col, self.current_player.color)
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

    def place_piece(self, selected_piece, row, col, color):
        piece = pieces[selected_piece]

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

        # 3. Place the piece
        for dr, dc in piece:
            r = row + dr
            c = col + dc
            self.buttons[r][c].config(bg=color)
        return True


class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = ["one", "two_horizontal", "three_L"]

    def select_piece(self):
        # For now we just return the same piece, but we can later implement a UI to select different pieces just like the game
        return pieces["three_L"]


game = Game()
game.start()