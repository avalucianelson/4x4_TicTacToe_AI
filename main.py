def print_board(board):
    """Prints the current state of the Tic-Tac-Toe board."""
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    """Checks if a player has won. Returns True if a player has won, False otherwise."""
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
    """Returns a list of empty spaces on the board."""
    spaces = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                spaces.append((i, j))
    return spaces

def minimax(board, depth, player, alpha, beta):
    """Implements the minimax algorithm with alpha-beta pruning."""
    if player == "O":
        best = [-1, -1, -float('inf')]
    else:
        best = [-1, -1, float('inf')]

    if depth == 0 or check_winner(board, "O") or check_winner(board, "X"):
        score = evaluate(board)
        return [-1, -1, score]

    for cell in empty_spaces(board):
        x, y = cell
        board[x][y] = player
        score = minimax(board, depth - 1, 'O' if player == 'X' else 'X', alpha, beta)
        board[x][y] = " "
        score[0], score[1] = x, y

        if player == "O":
            if score[2] > best[2]:
                best = score  # max value
            alpha = max(alpha, best[2])
        else:
            if score[2] < best[2]:
                best = score  # min value
            beta = min(beta, best[2])
        
        if beta <= alpha:
            break

    return best

def evaluate(board):
    """Evaluates the board and returns a score."""
    if check_winner(board, "O"):
        return +1
    if check_winner(board, "X"):
        return -1
    return 0

def main():
    """Main game loop for running the Tic-Tac-Toe game."""
    board = [[" " for _ in range(3)] for _ in range(3)]
    player_turn = "X"

    while True:
        print_board(board)
        if check_winner(board, "O"):
            print("O wins!")
            break
        elif check_winner(board, "X"):
            print("X wins!")
            break
        elif len(empty_spaces(board)) == 0:
            print("Tie!")
            break

        if player_turn == "X":
            print("Player X's turn:")
            x, y = map(int, input("Enter row and column numbers to place X (e.g., 0 1): ").split())
            board[x][y] = "X"
            player_turn = "O"
        else:
            print("AI's turn:")
            move = minimax(board, len(empty_spaces(board)), "O", -float('inf'), float('inf'))
            x, y = move[0], move[1]
            board[x][y] = "O"
            player_turn = "X"

if __name__ == "__main__":
    main()
