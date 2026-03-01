import tkinter as tk
from functools import partial

# We can use this to later handle the button to put the pieces
# For now, it just prints the coordinates of the button clicked
def on_click(row, col, buttons):
    selected_piece = select_piece()
    place_piece(selected_piece, row, col, buttons)

### we have to later create the logic to check if the piece can be placed in the selected position
def place_piece(selected_piece, row, col, buttons):
    piece = selected_piece
    # First check if ALL blocks are inside the board
    for dr, dc in piece:
        r = row + dr
        c = col + dc

        if not (0 <= r < 20 and 0 <= c < 20):
            print("Piece goes out of bounds!")
            return

    for dr, dc in piece:
        r = row + dr
        c = col + dc
        buttons[r][c].config(bg="red")

def create_board():
    root = tk.Tk()
    root.title("Blokus 20x20 board")
    buttons = []

    for i in range(20):
        row_buttons = []
        for j in range(20):
            btn = tk.Button(
                root,
                text=f"{i,j}",  # para tenerlo numerado
                width=4,
                height=1,
                command=lambda r=i, c=j: on_click(r, c, buttons)
            )
            btn.grid(row=i, column=j)
            row_buttons.append(btn)
        buttons.append(row_buttons)

    root.mainloop()
    return buttons

### we have to later create the pieces and the logic to select them.
def select_piece():
    # For now we just return the same piece, but we can later implement a UI to select different pieces just like the game
    return pieces["three_L"]

#### Here we define the pieces of the game, we can later add more pieces and also the logic to rotate and flip them.
pieces = {
    "one": [(0, 0)],

    "two_horizontal": [(0, 0), (0, 1)],
    "two_vertical":   [(0, 0), (1, 0)],

    "three_line":     [(0, 0), (0, 1), (0, 2)],
    "three_L":        [(0, 0), (1, 0), (1, 1)]
}
#### Here we call the functions for the game
board = create_board()
