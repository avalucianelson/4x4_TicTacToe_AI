def check_winner(board, player):
    """
    Checks all possible winning conditions to determine if the specified player has won.

    Parameters:
        board (list of list of str): The current state of the game board, where each element is a string ('X', 'O', or ' ').
        player (str): The player symbol ('X' or 'O') to check for a winning condition.

    Returns:
        bool: True if the specified player has won, False otherwise.
    """
    # Check horizontal lines
    for i in range(4):
        if all(board[i][j] == player for j in range(4)):
            return True
    # Check vertical lines
    for j in range(4):
        if all(board[i][j] == player for i in range(4)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(4)) or all(board[i][3-i] == player for i in range(4)):
        return True

    return False

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
    for i in range(4):  
        for j in range(4):  
            if board[i][j] == " ":
                spaces.append((i, j))
    return spaces

def iterative_deepening_minimax(board, max_depth, player):
    """
    Uses iterative deepening to wrap around the minimax function, gradually increasing the depth searched.

    Parameters:
        board (list of list of str): The game board.
        max_depth (int): The maximum depth to search.
        player (str): The initial player to move, typically 'O' (the AI).

    Returns:
        list: The best move as a list [row, column, score].
    """
    best_move = [-1, -1, -float('inf') if player == 'O' else float('inf')]
    for depth in range(1, max_depth + 1):
        current_move = minimax(board, depth, player, -float('inf'), float('inf'))
        if player == 'O' and current_move[2] > best_move[2]:
            best_move = current_move  # Update if better move is found for maximizer
        elif player == 'X' and current_move[2] < best_move[2]:
            best_move = current_move  # Update if better move is found for minimizer
        if abs(current_move[2]) == float('inf'):  # Found a winning move
            break
    return best_move

def minimax(board, depth, player, alpha, beta):
    """
    Recursive implementation of the minimax algorithm with alpha-beta pruning.

    Parameters:
        board (list of list of str): The game board.
        depth (int): The current depth in the game tree.
        player (str): 'O' or 'X', indicating the current player.
        alpha (float): The best value that the maximizing player can guarantee at that level or above.
        beta (float): The best value that the minimizing player can guarantee at that level or above.

    Returns:
        list: The best move as a list [row, column, score].
    """
    if depth == 0 or check_winner(board, "O") or check_winner(board, "X"):
        return [-1, -1, evaluate(board)]

    if player == "O":
        best = [-1, -1, -float('inf')]
    else:
        best = [-1, -1, float('inf')]

    for cell in empty_spaces(board):
        x, y = cell
        board[x][y] = player
        score = minimax(board, depth - 1, 'O' if player == 'X' else 'X', alpha, beta)
        board[x][y] = " "
        score[0], score[1] = x, y

        if player == "O":
            if score[2] > best[2]:
                best = score
            alpha = max(alpha, score[2])
        else:
            if score[2] < best[2]:
                best = score
            beta = min(beta, score[2])

        if beta <= alpha:
            break

    return best

def evaluate(board):
    """
    Evaluates the game board to provide a heuristic value used by the minimax algorithm.

    Parameters:
        board (list of list of str): The game board.

    Returns:
        int: The heuristic value of the board from the perspective of 'O'.
    """
    def evaluate_line(line):
        score = 0
        count_O = line.count('O')
        count_X = line.count('X')
        empty = line.count(' ')

        if count_O == 4:
            score += 1000  # Winning condition
        elif count_X == 4:
            score -= 1000  # Opponent winning condition
        elif count_O == 3 and empty == 1:
            score += 100  # Winning next move
        elif count_X == 3 and empty == 1:
            score -= 100  # Block opponent winning
        elif count_O == 2 and empty == 2:
            score += 10  # Potential setup for win
        elif count_X == 2 and empty == 2:
            score -= 10  # Block opponent setup
        return score

    total_score = 0
    # Check all rows and columns
    for i in range(4):
        total_score += evaluate_line([board[i][j] for j in range(4)])  # Evaluate rows
        total_score += evaluate_line([board[j][i] for j in range(4)])  # Evaluate columns

    # Check diagonals
    total_score += evaluate_line([board[i][i] for i in range(4)])
    total_score += evaluate_line([board[i][3-i] for i in range(4)])

    return total_score


