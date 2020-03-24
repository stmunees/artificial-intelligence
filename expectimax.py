"""
Alpha Beta Pruning Implementation
"""

SQUARE_WEIGHTS = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 120, -20, 20, 5, 5, 20, -20, 120, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

MAX_VALUE = sum(map(abs, SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE


def squares():
    '''
    Creates all positions in board.
    '''
    board_pos = []
    for i in range(11, 89):
        if 1 <= (i % 10) <= 8:
            board_pos.append(i)
    return board_pos


def any_legal_move(player, board):
    """Can player make any moves?"""
    return any(is_legal(sq, player, board) for sq in squares())


def legal_moves(player, board):
    """Get a list of all legal moves for player."""
    return [sq for sq in squares() if is_legal(sq, player, board)]


def opponent(player):
    """Get player's opponent piece."""
    return BLACK if player is WHITE else WHITE


def find_bracket(square, player, board, direction):
    """
    Find a square that forms a bracket with `square` for `player` in the given
    `direction`.  Returns None if no such square exists.
    """
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    return None if board[bracket] in (OUTER, EMPTY) else bracket


def make_flips(move, player, board, direction):
    """Flip pieces in the given direction as a result of the move by player."""
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction


def make_move(move, player, board):
    """Update the board to reflect the move by the specified player."""
    board[move] = player
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board


def is_legal(move, player, board):
    """Is this a legal move for the player?"""
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(map(hasbracket, DIRECTIONS))


def weighted_score(player, board):
    """
    Compute the difference between the sum of the weights of player's
    squares and the sum of the weights of opponent's squares.
    """
    opp = opponent(player)
    total = 0
    for sq in squares():
        if board[sq] == player:
            total += SQUARE_WEIGHTS[sq]
        elif board[sq] == opp:
            total -= SQUARE_WEIGHTS[sq]
    return total


def score(player, board):
    """Compute player's score (number of player's pieces minus opponent's)."""
    mine, theirs = 0, 0
    opp = opponent(player)
    for sq in squares():
        piece = board[sq]
        if piece == player:
            mine += 1
        elif piece == opp:
            theirs += 1
    return mine - theirs


def final_value(player, board):
    """The game is over--find the value of this board to player."""
    diff = score(player, board)
    if diff < 0:
        return MIN_VALUE
    elif diff > 0:
        return MAX_VALUE
    return diff


def expectimax_search(player, board, depth):

    def maximum_value(board, depth, player):
        valid_moves = legal_moves(player, board)
        if depth == 0 or not valid_moves:
            return weighted_score(player, board), None
        max_value = -100000
        best_move = valid_moves[0]
        for valid_move in valid_moves:
            board[valid_move] = str(player)
            opponent_player = opponent(player)
            exp_val, score = expectimax_value(board, depth - 1, opponent_player)
            board[valid_move] = '.'
            if exp_val > max_value:
                max_value = exp_val
                best_move = valid_move
        return max_value, best_move

    def expectimax_value(board, depth, player):
        valid_moves = legal_moves(player, board)
        if depth == 0 or not valid_moves:
            return weighted_score(player, board), None
        length_moves = len(valid_moves)
        exp_val = 0
        for valid_move in valid_moves:
            board[valid_move] = str(player)
            opponent_player = opponent(player)
            max_val, best_move = maximum_value(board, depth - 1, opponent_player)
            board[valid_move] = '.'
            exp_val += max_val
        return exp_val/length_moves, None

    if depth == 0:
        return weighted_score(player, board), None
    else:
        return maximum_value(board, depth, player)

