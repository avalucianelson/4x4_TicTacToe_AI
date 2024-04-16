import tkinter as tk
from tkinter import messagebox
from main import check_winner, empty_spaces, iterative_deepening_minimax

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
        elif all(board[r][c] != ' ' for r in range(4) for c in range(4)):
            messagebox.showinfo("Game Over", "It's a Tie!")
            reset_game()
        else:
            # Switch player turn
            player_turn = 'O' if player_turn == 'X' else 'X'
            if player_turn == 'O':
                ai_move()

def ai_move():
    """
    Function to make the AI move using the iterative deepening minimax algorithm.
    Uses the iterative deepening minimax to determine the best move for the AI.
    """
    # Dynamically adjust max depth based on the number of empty spaces
    empty_count = len(empty_spaces(board))
    max_depth = min(4, empty_count)  # Limit the max depth to either 4 or the number of empty spaces
    node_count = [0] # Initialize node counter 

    move, final_count = iterative_deepening_minimax(board, max_depth, 'O')
    print("Total nodes evaluated:", final_count[0])  # Print the count for analysis

    if move[0] != -1:  # Ensure that a valid move is found
        buttons[move[0]][move[1]].invoke()  # Simulate clicking the button for the AI's move
    
def reset_game():
    """
    Function to reset the game.
    Resets the game board and sets the player turn to 'X'.
    """
    global board, player_turn
    player_turn = "X"
    board = [[' ' for _ in range(4)] for _ in range(4)]  
    for row in buttons:
        for button in row:
            button.config(text='')

def create_board():
    """
    Function to create the game board.
    Creates a 4x4 grid of buttons using tkinter.
    """
    for i in range(4):
        row = []
        for j in range(4):  
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
board = [[' ' for _ in range(4)] for _ in range(4)] 
buttons = []

# Create the game board
create_board()

# Create the reset button
reset_button = tk.Button(window, text='Reset Game', font=('normal', 20), command=reset_game)
reset_button.grid(row=4, column=0, columnspan=4)

# Start the main event loop
window.mainloop()
