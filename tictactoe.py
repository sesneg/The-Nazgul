"""
tictactoe.py  –  Minimax Tic-Tac-Toe AI
"""
import copy
import math

X     = "X"
O     = "O"
EMPTY = None

# ──────────────────────────────────────────────
def initial_state():
    """Returns the starting empty 3×3 board."""
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# ──────────────────────────────────────────────
def player(board):
    """Return whose turn it is (X or O)."""
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O

# ──────────────────────────────────────────────
def actions(board):
    """Return set of all valid (i, j) actions."""
    return {(i, j)
            for i in range(3)
            for j in range(3)
            if board[i][j] == EMPTY}

# ──────────────────────────────────────────────
def result(board, action):
    """Return new board after applying action (deep copy, no mutation)."""
    i, j = action
    if board[i][j] != EMPTY:
        raise ValueError(f"Invalid action {action}: cell is already occupied.")
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board

# ──────────────────────────────────────────────
def winner(board):
    """Return X, O, or None."""
    lines = (
        # rows
        [board[0], board[1], board[2]],
        # cols
        [[board[r][c] for r in range(3)] for c in range(3)],
        # diagonals
        [[board[i][i] for i in range(3)]],
        [[board[i][2-i] for i in range(3)]],
    )
    for group in lines:
        for line in group:
            if line[0] is not None and line[0] == line[1] == line[2]:
                return line[0]
    return None

# ──────────────────────────────────────────────
def terminal(board):
    """Return True if the game is over."""
    if winner(board) is not None:
        return True
    return all(board[i][j] != EMPTY for i in range(3) for j in range(3))

# ──────────────────────────────────────────────
def utility(board):
    """Return +1 (X wins), -1 (O wins), or 0 (tie). Only call on terminal boards."""
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    return 0

# ──────────────────────────────────────────────
# Minimax with optional alpha-beta pruning
# ──────────────────────────────────────────────
def _max_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None
    v    = -math.inf
    best = None
    for action in actions(board):
        val, _ = _min_value(result(board, action), alpha, beta)
        if val > v:
            v, best = val, action
        alpha = max(alpha, v)
        if alpha >= beta:
            break           # β cut-off
    return v, best

def _min_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None
    v    = math.inf
    best = None
    for action in actions(board):
        val, _ = _max_value(result(board, action), alpha, beta)
        if val < v:
            v, best = val, action
        beta = min(beta, v)
        if alpha >= beta:
            break           # α cut-off
    return v, best

def minimax(board):
    """Return the optimal action for the current player, or None if terminal."""
    if terminal(board):
        return None
    if player(board) == X:
        _, action = _max_value(board, -math.inf, math.inf)
    else:
        _, action = _min_value(board, -math.inf, math.inf)
    return action
