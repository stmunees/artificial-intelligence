from game import othellogame,constant
import random

def random_strategy(player, board):
    """A strategy that always chooses a random legal move."""
    return random.choice(othellogame.legal_moves(player, board))

def alphabeta_strategy(player, board):
    return alphabeta(player, board, constant.MIN_VALUE, constant.MAX_VALUE,7)[1]

def alphabeta(player, board, alpha, beta, depth):
    """
    Find the best legal move for player, searching to the specified depth.  Like
    minimax, but uses the bounds alpha and beta to prune branches.
    """
    if depth == 0:
        return othellogame.weighted_score(player, board), None

    def value(board, alpha, beta):
        # Like in `minimax`, the value of a board is the opposite of its value
        # to the opponent.  We pass in `-beta` and `-alpha` as the alpha and
        # beta values, respectively, for the opponent, since `alpha` represents
        # the best score we know we can achieve and is therefore the worst score
        # achievable by the opponent.  Similarly, `beta` is the worst score that
        # our opponent can hold us to, so it is the best score that they can
        # achieve.
        return -alphabeta(othellogame.opponent(player), board, -beta, -alpha, depth-1)[0]

    moves = othellogame.legal_moves(player, board)
    if not moves:
        if not othellogame.any_legal_move(othellogame.opponent(player), board):
            return final_value(player, board), None
        return value(board, alpha, beta), None

    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            # If one of the legal moves leads to a better score than beta, then
            # the opponent will avoid this branch, so we can quit looking.
            break
        val = value(othellogame.make_move(move, player, list(board)), alpha, beta)
        if val > alpha:
            # If one of the moves leads to a better score than the current best
            # achievable score, then replace it with this one.
            alpha = val
            best_move = move
    return alpha, best_move

def expectimax_search(player, board, depth):

    def maximum_value(board, depth, player):
        valid_moves = othellogame.legal_moves(player, board)
        if depth == 0 or not valid_moves:
            return othellogame.weighted_score(player, board), None
        max_value = -100000
        best_move = valid_moves[0]
        for valid_move in valid_moves:
            board[valid_move] = str(player)
            opponent_player = othellogame.opponent(player)
            exp_val, score = expectimax_value(board, depth - 1, opponent_player)
            board[valid_move] = '.'
            if exp_val > max_value:
                max_value = exp_val
                best_move = valid_move
        return max_value, best_move

    def expectimax_value(board, depth, player):
        valid_moves = othellogame.legal_moves(player, board)
        if depth == 0 or not valid_moves:
            return othellogame.weighted_score(player, board), None
        length_moves = len(valid_moves)
        exp_val = 0
        for valid_move in valid_moves:
            board[valid_move] = str(player)
            opponent_player = othellogame.opponent(player)
            max_val, best_move = maximum_value(board, depth - 1, opponent_player)
            board[valid_move] = '.'
            exp_val += max_val
        return exp_val/length_moves, None

    if depth == 0:
        return othellogame.weighted_score(player, board), None
    else:
        return maximum_value(board, depth, player)

def minimax(player, board, depth, evaluate):
    """
    Find the best legal move for player, searching to the specified depth.
    Returns a tuple (move, min_score), where min_score is the guaranteed minimum
    score achievable for player if the move is made.
    """

    # We define the value of a board to be the opposite of its value to our
    # opponent, computed by recursively applying `minimax` for our opponent.
    def value(board):
        return -minimax(othellogame.opponent(player), board, depth-1)[0]
    
    # When depth is zero, don't examine possible moves--just determine the value
    # of this board to the player.
    if depth == 0:
        return othellogame.score(player, board), None
    
    # We want to evaluate all the legal moves by considering their implications
    # `depth` turns in advance.  First, find all the legal moves.
    moves = othellogame.legal_moves(player, board)
    
    # If player has no legal moves, then either:
    if not moves:
        # the game is over, so the best achievable score is victory or defeat;
        if not othellogame.any_legal_move(othellogame.opponent(player), board):
            return final_value(player, board), None
        # or we have to pass this turn, so just find the value of this board.
        return value(board), None
    
    # When there are multiple legal moves available, choose the best one by
    # maximizing the value of the resulting boards.
    return max((value(othellogame.make_move(m, player, list(board))), m) for m in moves)

# Values for endgame boards are big constants.
MAX_VALUE = sum(map(abs, constant.SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE

def final_value(player, board):
    """The game is over--find the value of this board to player."""
    diff = othellogame.score(player, board)
    if diff < 0:
        return MIN_VALUE
    elif diff > 0:
        return MAX_VALUE
    return diff


def minimax_searcher(depth):
    """
    Construct a strategy that uses `minimax` with the specified leaf board
    evaluation function.
    """
    def strategy(player, board):
        return minimax(player, board, depth)[1]
    return strategy


