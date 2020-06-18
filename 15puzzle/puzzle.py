"""
15 Puzzle algorithms
"""
import copy
import random

import search


def board_to_tuple(board):
    """
        Converts list of lists to tuple of tuples
        Needed to allow hashing
    """
    if type(board) == tuple:
        return board
    t = []
    for r in range(len(board)):
        t.append(tuple(board[r]))
    return tuple(t)


def board_to_list(board):
    if type(board) == list:
        return board

    l = []
    for r in range(len(board)):
        l.append(list(board[r]))
    return l


def starting_board(board_size, moves):
    """
    Returns starting state of a correct board bt
        making random valid moves from a finished state
    """

    # first create a finished state
    board = []
    for row in range(board_size):
        board.append([row * board_size + i + 1 for i in range(board_size)])

    # now make random moves
    visited_states = set()
    visited_states.add(board_to_tuple(board))
    for move in range(moves):
        acts = actions(board)
        choices = random.sample(acts, len(acts))
        for action in choices:
            new_board = result(board, action)
            if board_to_tuple(new_board) not in visited_states:
                # print(action)
                board = new_board
                visited_states.add(board_to_tuple(board))
                break
    print(f'Starting Board {board}')
    return board


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
    actions = set()
    size = len(board)
    loc_spc = loc_space(board)
    if loc_spc[0] < size - 1:
        actions.add((loc_spc[0] + 1, loc_spc[1]))  # Slide tile below UP
    if loc_spc[0] > 0:
        actions.add((loc_spc[0] - 1, loc_spc[1]))  # Slide tile above DOWN
    if loc_spc[1] < size - 1:
        actions.add((loc_spc[0], loc_spc[1] + 1))  # Slide tile beside LEFT
    if loc_spc[1] > 0:
        actions.add((loc_spc[0], loc_spc[1] - 1))  # Slide tile beside RIGHT

    return actions


def loc_space(board):
    """
        Return the location of the SPACE tile on the board
    """
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == size ** 2:
                return i, j


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy_board(board)
    loc_spc = loc_space(board)
    new_board[action[0]][action[1]] = len(board) ** 2  # SPACE goes here
    new_board[loc_spc[0]][loc_spc[1]] = board[action[0]][action[1]]  # Value of moving tile set here
    return new_board


def copy_board(board):
    if type(board) is tuple:
        new_board = board_to_list(board)
    else:
        new_board = [board[row].copy() for row in range(len(board))]
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


def solve(board):
    """
        Returns the sequence of moves to solve the puzzle
    """

    sa = search.SearchAlgo()
    solution = sa.solve(board)

    return solution


def mhd(board):  # manhattan distance
    size = len(board)
    mhd = 0
    for r in range(size):
        for c in range(size):
            val = board[r][c] - 1
            tgt_r = val // size
            tgt_c = val % size
            mhd += abs(tgt_r - r) + abs(tgt_c - c)
    return mhd


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


def main():
    board = starting_board(4, 32)
    print(f'board {board}')
    print(f'mhd = {mhd(board)}')
    solution = solve(board)
    print(f'solution: {len(solution)} :  {solution}')


if __name__ == '__main__':
    main()
