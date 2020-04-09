from game import othellogame,constant
import random

def random_strategy(player, board):
    """A strategy that always chooses a random legal move."""
    return random.choice(othellogame.legal_moves(player, board))

def alphabeta_agent(level):
    def alphabeta_strategy(player, board):
        return alphabeta(player, board, constant.MIN_VALUE, constant.MAX_VALUE,level.value)[1] 
    return alphabeta_strategy

def expectimax_agent(level):
    def expectimax_strategy(player, board):
        return expectimax_search(player, board, level.value)[1]
    return expectimax_strategy

def minimax_agent(level):
    def minimax_strategy(player, board):
        return minimax(player, board, level.value)[1]
    return minimax_strategy


def alphabeta(player, board, alpha, beta, depth):
    """
    Find the best legal move for player, searching to the specified depth.  Like
    minimax, but uses the bounds alpha and beta to prune branches.
    """
    if depth == 0:
        return othellogame.weighted_score(player, board), None

    def value(board, alpha, beta):
        return -alphabeta(othellogame.opponent(player), board, -beta, -alpha, depth-1)[0]

    moves = othellogame.legal_moves(player, board)
    if not moves:
        if not othellogame.any_legal_move(othellogame.opponent(player), board):
            return final_value(player, board), None
        return value(board, alpha, beta), None

    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            break
        val = value(othellogame.make_move(move, player, list(board)), alpha, beta)
        if val > alpha:
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

def minimax(player, board, depth):
    """
    Find the best legal move for player, searching to the specified depth.
    Returns a tuple (move, min_score), where min_score is the guaranteed minimum
    score achievable for player if the move is made.
    """

    def value(board):
        return -minimax(othellogame.opponent(player), board, depth-1)[0]

    if depth == 0:
        return othellogame.score(player, board), None
    
    moves = othellogame.legal_moves(player, board)
    
    # If player has no legal moves, then either:
    if not moves:
        # the game is over, so the best achievable score is victory or defeat;
        if not othellogame.any_legal_move(othellogame.opponent(player), board):
            return final_value(player, board), None
        # or we have to pass this turn, so just find the value of this board.
        return value(board), None
    
    return max((value(othellogame.make_move(m, player, list(board))), m) for m in moves)

# Values for endgame boards are big constants.
MAX_VALUE = sum(map(abs, constant.SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE

def final_value(player, board):
    """The game is over--find the value of this board to player."""
    score = othellogame.score(player, board)
    if (score[0] - score[1]) < 0:
        return MIN_VALUE
    elif (score[0] - score[1]) > 0:
        return MAX_VALUE
    return (score[0] - score[1])