"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    xplays = sum(x.count(X) for x in board)
    oplays = sum(x.count(O) for x in board)
    return X if xplays == oplays else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for x in range(3):
        for y in range(3):
            if board[x][y] == EMPTY:
                actions.append((x, y))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = [board[row].copy() for row in range(3)]
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    x_wins = o_wins = False
    for row in board:
        if row.count(X) == 3:
            x_wins = True
        if row.count(O) == 3:
            o_wins = True

    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            if board[0][col] == X:
                x_wins = True
            if board[0][col] == O:
                o_wins = True

    # diag
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2]) or \
            (board[0][2] == board[1][1] and board[1][1] == board[2][0]):
        if board[1][1] == X:
            x_wins = True
        if board[1][1] == O:
            o_wins = True

    if x_wins:
        return X
    if o_wins:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if len(actions(board)) == 0:
        return True
    if winner(board) is not None:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if player(board) == X:
        _, action = maxValue(board)
    else:
        _, action = minValue(board)

    return action


def minValue(board, move=None):
    if terminal(board):
        return utility(board), move
    min_val = 1
    min_action = None
    for action in actions(board):
        if min_val > -1:
            next_val, _ = maxValue(result(board, action), action)
            if next_val < min_val:
                min_val = next_val
                min_action = action
    return min_val, min_action


def maxValue(board, move=None):

    if terminal(board):
        return utility(board), move
    max_val = -1
    max_action = None
    for action in actions(board):
        if max_val < 1:
            next_val, _ = minValue(result(board, action), action)
            if next_val > max_val:
                max_val = next_val
                max_action = action

    return max_val, max_action
