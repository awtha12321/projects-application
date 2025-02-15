"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def looping_the_board(board, player=False, actions=False):

    count_for_turn = 0
    avaliable_sqaure = []

    if actions == True:
        for row in range(len(board)):
            for each_value in range(len(board[row])):
                if board[row][each_value] == EMPTY:
                    avaliable_sqaure.append((row, each_value))

        return avaliable_sqaure

    if player == True:
        for row in board:
            for each_value in row:
                if each_value != None:
                    count_for_turn += 1
        return count_for_turn


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    turn = looping_the_board(board, True, False)
    if turn % 2 == 0:
        turn = X  # 1 = X
    else:
        turn = O  # 2 = O

    return turn


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    avaliable_sqaures = looping_the_board(board, False, True)
    return avaliable_sqaures


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise Exception("Action is not valid")

    new_board = copy.deepcopy(board)

    if player(board) == X:
        new_board[action[0]][action[1]] = X
    else:
        new_board[action[0]][action[1]] = O

    return new_board


def winner_check(board, player):  # problem might be here
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(len(board)):
        if all(board[row][col] == player for row in range(len(board))):
            return True
    if all(board[i][i] == player for i in range(len(board))) or all(
        board[i][len(board) - 1 - i] == player for i in range(len(board))
    ):
        return True

    return False


def winner(board):  # problem might be here
    """
    Returns the winner of the game, if there is one.
    """

    winner_result_X = winner_check(board, X)
    if winner_result_X == True:
        return X
    winner_result_O = winner_check(board, O)
    if winner_result_O == True:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    has_winner = winner(board)

    if has_winner != None:
        return True

    for row in board:
        if EMPTY in row:
            return False

    return True


def utility(board):  # problem might be here
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    player_winner = winner(board)
    if player_winner == X:
        return 1
    if player_winner == O:
        return -1
    else:
        return 0


def recursion(move, board):
    frontier = []
    frontier.append(move)
    total_score = 0
    new_board = board
    tracker = []
    tracker_count = 0

    while True:

        if len(frontier) == 0:
            break

        if terminal(new_board):
            player_winner = utility(new_board)
            if player_winner == 1:
                total_score += 1
            if player_winner == -1:
                total_score -= 1
            new_board = board
            tracker_count = 0

        if frontier[0] in tracker:
            frontier.pop(0)
            continue
        if frontier[0] not in actions(new_board):
            frontier.pop(0)
            continue
        new_board = result(new_board, frontier[0])
        if tracker_count == 0:
            tracker.append(frontier[0])
        avaliable_actions = actions(new_board)
        for move in avaliable_actions:
            if move not in frontier:
                frontier.append(move)

        frontier.pop(0)
        tracker_count += 1

    return total_score


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    immediate_actions = actions(board)
    score_for_immediate_actions = []

    for move in immediate_actions:
        score_for_immediate_actions.append(recursion(move, board))

    turn = player(board)
    if turn == X:
        index_ = score_for_immediate_actions.index(max(score_for_immediate_actions))
    if turn == O:
        index_ = score_for_immediate_actions.index(min(score_for_immediate_actions))

    return immediate_actions[index_]
