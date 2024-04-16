def check_winner(board, player):
    """
    Checks all possible winning conditions to determine if the specified player has won.

    Parameters:
        board (list of list of str): The current state of the game board, where each element is a string ('X', 'O', or ' ').
        player (str): The player symbol ('X' or 'O') to check for a winning condition.

    Returns:
        bool: True if the specified player has won, False otherwise.

    This function supports the learning outcome #ailogic by applying logical conditions to determine the game status.
    """
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]]
    ]
    return [player, player, player] in win_conditions

def empty_spaces(board):
    """
    Identifies all empty spaces on the game board.

    Parameters:
        board (list of list of str): The current state of the game board.

    Returns:
        list of tuples: A list of tuples where each tuple represents the coordinates (row, column) of an empty space on the board.

    This utility function facilitates the minimax algorithm by providing potential moves, supporting the #aicoding learning outcome.
    """
    spaces = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                spaces.append((i, j))
    return spaces

def minimax(board, depth, player, alpha, beta):
    """
    Recursive implementation of the minimax algorithm to determine the optimal move for 'O' or 'X' in Tic-Tac-Toe.

    Parameters:
        board (list of list of str): The game board.
        depth (int): The current depth in the game tree.
        player (str): 'O' or 'X', indicating the current player.
        alpha (float): The best value that the maximizing player can guarantee at that level or above.
        beta (float): The best value that the minimizing player can guarantee at that level or above.

    Returns:
        list: The best move as a list [row, column, score].

    This function demonstrates #search and #algorithms by using recursive tree search techniques and optimizing with alpha-beta pruning.
    """
    # Initialize the best move with default values
    if player == "O":
        best = [-1, -1, -float('inf')]
    else:
        best = [-1, -1, float('inf')]

    # Check if the game has reached the maximum depth or if there is a winner
    if depth == 0 or check_winner(board, "O") or check_winner(board, "X"):
        score = evaluate(board)
        return [-1, -1, score]

    # Iterate through each empty space on the board
    for cell in empty_spaces(board):
        x, y = cell
        # Place the current player's symbol on the empty space
        board[x][y] = player
        # Recursively call the minimax function for the opponent player
        score = minimax(board, depth - 1, 'O' if player == 'X' else 'X', alpha, beta)
        # Remove the current player's symbol from the board
        board[x][y] = " "
        # Update the move coordinates in the score list
        score[0], score[1] = x, y

        # Update the best move based on the player's turn
        if player == "O":
            if score[2] > best[2]:
                best = score
            # Update the alpha value for the maximizing player
            alpha = max(alpha, best[2])
        else:
            if score[2] < best[2]:
                best = score
            # Update the beta value for the minimizing player
            beta = min(beta, best[2])
        
        # Perform alpha-beta pruning if beta is less than or equal to alpha
        if beta <= alpha:
            break

    # Return the best move
    return best

def evaluate(board):
    """
    Evaluates the game board to provide a heuristic value used by the minimax algorithm.

    Parameters:
        board (list of list of str): The game board.

    Returns:
        int: The heuristic value of the board from the perspective of 'O'.

    This evaluation function directly contributes to the #modeling learning outcome by providing a basic heuristic for the minimax decision-making process.
    """
    if check_winner(board, "O"):
        return +1
    if check_winner(board, "X"):
        return -1
    return 0
