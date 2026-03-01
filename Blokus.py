import tkinter as tk
from functools import partial

# We can use this to later handle the button to put the pieces
# For now, it just prints the coordinates of the button clicked
def on_click(row, col, buttons):
    place_piece("example_piece", row, col, buttons)

### we have to later create the logic to check if the piece can be placed in the selected position
def place_piece(piece, row, col, buttons):
    # Access the button at the clicked position
    btn = buttons[row][col]
    btn.config(bg="red")  # Change the color of the button

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
def select_piece(piece):
    print(f"Selected piece: {piece}")

#### Here we call the functions for the game
board = create_board()
