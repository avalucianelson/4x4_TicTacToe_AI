
"""
This module contains the GUI implementation for a Tic Tac Toe game using tkinter.
It includes functions to handle button clicks, update the game board, check for a winner or tie,
and trigger the AI move. It also provides a function to plot the log scale of nodes evaluated per move.
"""

import tkinter as tk
from tkinter import messagebox
from main import check_winner, empty_spaces, iterative_deepening_minimax
import matplotlib.pyplot as plt
import numpy as np

# For plotting node counts
node_counts_with_pruning = []
node_counts_without_pruning = []

def plot_node_counts(node_counts_with_pruning, node_counts_without_pruning):
    """
    Plot the log scale of nodes evaluated per move.

    Args:
        node_counts_with_pruning (list): List of node counts with pruning.
        node_counts_without_pruning (list): List of node counts without pruning.
    """
    plt.figure(figsize=(10, 5))
    # Convert zero or lower values to a very small number to avoid taking log of zero or negative numbers
    safe_log_with_pruning = [np.log10(count) if count > 0 else -1 for count in node_counts_with_pruning]
    safe_log_without_pruning = [np.log10(count) if count > 0 else -1 for count in node_counts_without_pruning]

    plt.plot(safe_log_with_pruning, marker='o', linestyle='-', color='b', label='With Pruning')
    plt.plot(safe_log_without_pruning, marker='x', linestyle='--', color='r', label='Without Pruning')
    
    plt.title('Log Scale of Nodes Evaluated per Move')
    plt.xlabel('Move Number')
    plt.ylabel('Log of Nodes Evaluated (log10 scale)')
    plt.legend()
    plt.grid(True)
    plt.show()

def on_plot_button_click():
    """
    Event handler for the plot button click.
    Calls the plot_node_counts function.
    """
    plot_node_counts(node_counts_with_pruning, node_counts_without_pruning)

def on_click(row, col):
    """
    Function to handle button click event.
    Updates the game board, checks for a winner or tie, and triggers AI move if necessary.

    Args:
        row (int): The row index of the clicked button.
        col (int): The column index of the clicked button.
    """
    global player_turn, board, buttons

    # Check if the button is empty and there is no winner yet
    if buttons[row][col]['text'] == "" and not check_winner(board, "O") and not check_winner(board, "X"):
        buttons[row][col]['text'] = player_turn
        board[row][col] = player_turn
        buttons[row][col].update_idletasks() 

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
    Function to make the AI move.
    Runs the iterative deepening minimax algorithm with alpha-beta pruning.
    Updates the node counts for both methods.
    """
    global board, buttons
    empty_count = len(empty_spaces(board))
    max_depth = min(4, empty_count)  # Adjust max depth based on empty spaces

    # Initialize node counters for both methods
    node_count_with_pruning = [0]
    node_count_without_pruning = [0]

    # Run minimax with alpha-beta pruning
    move_with_pruning, final_count_with_pruning = iterative_deepening_minimax(board, max_depth, 'O', node_count_with_pruning, True)
    node_counts_with_pruning.append(final_count_with_pruning[0])  # Append the count for this move to the list

    # Run minimax without alpha-beta pruning
    move_without_pruning, final_count_without_pruning = iterative_deepening_minimax(board, max_depth, 'O', node_count_without_pruning, False)
    node_counts_without_pruning.append(final_count_without_pruning[0])  # Append the count for this move to the list

    print("Nodes with pruning:", final_count_with_pruning[0])
    print("Nodes without pruning:", final_count_without_pruning[0])

    if move_with_pruning[0] != -1:  # Version with pruning for actual game play
        buttons[move_with_pruning[0]][move_with_pruning[1]].invoke()  # Simulate clicking the button for the AI's move

def reset_game():
    """
    Function to reset the game.
    Resets the game board and sets the player turn to 'X'.
    """
    global board, player_turn, buttons
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
    global window, buttons
    buttons = []
    
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

# Create the game board
create_board()

# Create the reset button
reset_button = tk.Button(window, text='Reset Game', font=('normal', 20), command=reset_game)
reset_button.grid(row=4, column=0, columnspan=4)

# Create the plot button
plot_button = tk.Button(window, text='Plot Node Counts', font=('normal', 20), command=on_plot_button_click)
plot_button.grid(row=5, column=0, columnspan=4)

# Start the main event loop
window.mainloop()

