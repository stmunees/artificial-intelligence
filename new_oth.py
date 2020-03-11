'''
Implements the Rules of Othello Game.
'''


EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

def squares():
    '''
    Creates all positions in board.
    '''
    board_pos = []
    for i in range(11, 89):
        if 1 <= (i % 10) <= 8:
            board_pos.append(i)
    return board_pos

def initial_board():
    '''
    Initialises the board with initial settings/positions.
    '''
    # import pdb; pdb.set_trace();
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    board[44], board[45], board[54], board[55] = WHITE, BLACK, BLACK, WHITE
    return board

def print_board():
    '''
    Pretty Prints the board.
    '''
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep



def is_legal_move(black_move,'b',board):
    




if __name__ == '__main__':
    board = initial_board()
    print(print_board())
    print('You are black, Black Plays First')

    is_legal_move(black_move,'b',board)

    # while True:
        # while True:
            # black_move = input('Enter Grid Coordinates:')
            # if (is_legal_move(black_move,'b')):
                # board[black_move] = '@'
                # print(print_board())
                # print_score();
                # if(game_over()):
                    # exit();
                # break;
        # computer move = get_best_move();
        # board[black_move] = 'o';

    #test=print_board(initial_board())
    #print(test)
