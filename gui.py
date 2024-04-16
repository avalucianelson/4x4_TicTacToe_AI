import tkinter as tk
from tkinter import messagebox
from main import check_winner, minimax, empty_spaces

def on_click(row, col):
    """
    Function to handle button click event.
    Updates the game board, checks for a winner or tie, and triggers AI move if necessary.

    Args:
        row (int): The row index of the clicked button.
        col (int): The column index of the clicked button.
    """
    global player_turn

    # Check if the button is empty and there is no winner yet
    if buttons[row][col]['text'] == "" and not check_winner(board, "O") and not check_winner(board, "X"):
        buttons[row][col]['text'] = player_turn
        board[row][col] = player_turn
        buttons[row][col].update_idletasks()  # Force the button to update its display

        # Check for a winner
        if check_winner(board, player_turn):
            messagebox.showinfo("Game Over", f"{player_turn} wins!")
            reset_game()
        # Check for a tie
        elif all(board[r][c] != ' ' for r in range(3) for c in range(3)):
            messagebox.showinfo("Game Over", "It's a Tie!")
            reset_game()
        else:
            # Switch player turn
            player_turn = 'O' if player_turn == 'X' else 'X'
            if player_turn == 'O':
                ai_move()

def ai_move():
    """
    Function to make the AI move.
    Uses the minimax algorithm to determine the best move for the AI.
    """
    move = minimax(board, len(empty_spaces(board)), 'O', -float('inf'), float('inf'))
    buttons[move[0]][move[1]].invoke()

def reset_game():
    """
    Function to reset the game.
    Resets the game board and sets the player turn to 'X'.
    """
    global board, player_turn
    player_turn = "X"
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for row in buttons:
        for button in row:
            button.config(text='')

def create_board():
    """
    Function to create the game board.
    Creates a 3x3 grid of buttons using tkinter.
    """
    for i in range(3):
        row = []
        for j in range(3):
            button = tk.Button(window, text='', font=('normal', 40), width=5, height=2,
                               command=lambda i=i, j=j: on_click(i, j))
            button.grid(row=i, column=j)
            row.append(button)
        buttons.append(row)

# Create the main window
window = tk.Tk()
window.title("Tic Tac Toe")

# Initialize game variables
player_turn = "X"
board = [[' ' for _ in range(3)] for _ in range(3)]
buttons = []

# Create the game board
create_board()

# Create the reset button
reset_button = tk.Button(window, text='Reset Game', font=('normal', 20), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3)

# Start the main event loop
window.mainloop()
