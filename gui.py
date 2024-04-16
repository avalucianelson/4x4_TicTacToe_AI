import tkinter as tk
from tkinter import messagebox
from main import check_winner, minimax, empty_spaces

def on_click(row, col):
    global player_turn
    if buttons[row][col]['text'] == "" and check_winner(board, "O") is False and check_winner(board, "X") is False:
        buttons[row][col]['text'] = player_turn
        board[row][col] = player_turn
        if check_winner(board, player_turn):
            messagebox.showinfo("Game Over", f"{player_turn} wins!")
            reset_game()
        elif all(board[r][c] != ' ' for r in range(3) for c in range(3)):
            messagebox.showinfo("Game Over", "It's a Tie!")
            reset_game()
        else:
            player_turn = 'O' if player_turn == 'X' else 'X'
            if player_turn == 'O':
                ai_move()

def ai_move():
    move = minimax(board, len(empty_spaces(board)), 'O', -float('inf'), float('inf'))
    buttons[move[0]][move[1]].invoke()

def reset_game():
    global board, player_turn
    player_turn = "X"
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for row in buttons:
        for button in row:
            button.config(text='')

def create_board():
    for i in range(3):
        row = []
        for j in range(3):
            button = tk.Button(window, text='', font=('normal', 40), width=5, height=2,
                               command=lambda i=i, j=j: on_click(i, j))
            button.grid(row=i, column=j)
            row.append(button)
        buttons.append(row)

window = tk.Tk()
window.title("Tic Tac Toe")
player_turn = "X"
board = [[' ' for _ in range(3)] for _ in range(3)]
buttons = []
create_board()
reset_button = tk.Button(window, text='Reset Game', font=('normal', 20), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3)
window.mainloop()
