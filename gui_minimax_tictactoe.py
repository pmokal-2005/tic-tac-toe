import tkinter as tk
import math
import random

# -----------------------
# Game State
# -----------------------
board = [" " for _ in range(9)]
buttons = []

# -----------------------
# Background colors
# -----------------------
colors = ["#ffadad", "#ffd6a5", "#fdffb6", "#caffbf",
          "#9bf6ff", "#a0c4ff", "#bdb2ff", "#ffc6ff"]
color_index = 0

# -----------------------
# Check Winner
# -----------------------
def check_winner(player):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(board[i] == player for i in w) for w in wins)

def is_draw():
    return " " not in board

# -----------------------
# Minimax Algorithm
# -----------------------
def minimax(is_ai):
    if check_winner("O"):
        return 1
    if check_winner("X"):
        return -1
    if is_draw():
        return 0

    if is_ai:
        best = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(False)
                board[i] = " "
                best = max(best, score)
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(True)
                board[i] = " "
                best = min(best, score)
        return best

# -----------------------
# AI Move
# -----------------------
def ai_move():
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i

    board[move] = "O"
    buttons[move].config(text="O", state="disabled")

    if check_winner("O"):
        status.config(text="🤖 AI Wins!")
        disable_all()

# -----------------------
# Button Click
# -----------------------
def click(i):
    if board[i] == " ":
        board[i] = "X"
        buttons[i].config(text="X", state="disabled")

        if check_winner("X"):
            status.config(text="🎉 You Win!")
            disable_all()
            return

        if is_draw():
            status.config(text="🤝 Draw")
            return

        ai_move()

# -----------------------
# Helpers
# -----------------------
def disable_all():
    for b in buttons:
        b.config(state="disabled")

def reset():
    global board
    board = [" " for _ in range(9)]
    for b in buttons:
        b.config(text=" ", state="normal")
    status.config(text="Your Turn")

# -----------------------
# Color Changing Background
# -----------------------
def change_bg():
    global color_index
    root.configure(bg=colors[color_index])
    title_label.configure(bg=colors[color_index])
    status.configure(bg=colors[color_index])
    frame.configure(bg=colors[color_index])

    color_index = (color_index + 1) % len(colors)
    root.after(1000, change_bg)  # change every 1 second

# -----------------------
# GUI
# -----------------------
root = tk.Tk()
root.title("Tic-Tac-Toe Minimax AI")
root.geometry("400x500")

# Project name (BACKGROUND TEXT)
title_label = tk.Label(
    root,
    text="PREM'S PROJECT",
    font=("Arial", 20, "bold"),
    fg="black"
)
title_label.pack(pady=10)

status = tk.Label(root, text="Your Turn", font=("Arial", 14))
status.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

for i in range(9):
    btn = tk.Button(
        frame,
        text=" ",
        font=("Arial", 20),
        width=5,
        height=2,
        command=lambda i=i: click(i)
    )
    btn.grid(row=i//3, column=i%3, padx=3, pady=3)
    buttons.append(btn)

tk.Button(root, text="Reset Game", command=reset).pack(pady=10)

# Start background animation
change_bg()

root.mainloop()
