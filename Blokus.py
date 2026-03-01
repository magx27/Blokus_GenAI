import tkinter as tk
from functools import partial

# We can use this to later handle the button to put the pieces
# For now, it just prints the coordinates of the button clicked
def on_click(row, col):
    print(f"Button clicked at ({row}, {col})")

root = tk.Tk()
root.title("Blokus 20x20 board")
buttons = []

for i in range(20):
    row_buttons = []
    for j in range(20):
        btn = tk.Button(
            root,
            text=f"{i,j}", #para tenerlo numerado
            width=4,
            height=1,
            command=lambda r=i, c=j: on_click(r, c)
        )
        btn.grid(row=i, column=j)
        row_buttons.append(btn)
    buttons.append(row_buttons)

root.mainloop()