'''
Implements the Rules of Othello Game.
'''
import math
from alphabetapruning import alphabeta

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

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

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

def initial_board():
    '''
    Initialises the board with initial settings/positions.
    '''
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    board[44], board[45], board[54], board[55] = WHITE, BLACK, BLACK, WHITE
    return board

def print_board(board):
    '''
    Pretty Prints the board.
    '''
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep

def game_over(board):
    '''
    If all the places of the board are filled then game is over.
    '''
    for i in squares():
        if(board[i]=='.'):
            return False
    return True


def do_flips(player,i,j,board):
    '''
    flips all opponent disks between a players ith and jth disk
    '''
    x1 = int(i/10)
    y1 = i%10;
    x2 = int(j/10)
    y2 = j%10

    count=0;

    if(x1<x2):
        xs = x1;xb=x2
    else:
        xs = x2;xb=x1

    if(y1<y2):
        ys = y1;yb=y2
    else:
        ys = y2;yb=y1


    if(x1==x2):
        for i in range(ys,yb):
                if(board[int(str(x1)+str(i))]!=player):
                    board[int(str(x1)+str(i))] = player
                    count+=1

    elif(y1==y2):
        for i in range(xs,xb):
                if(board[int(str(i)+str(y1))]!=player):
                    board[int(str(i)+str(y1))] = player
                    count+=1

    else:

            slope = (y2-y1)/(x2-x1)
            start  = ys;
            if(slope<0):
                a = xb;b=xs;incr = -1
            else:
                a = xs;b=xb;incr = 1

            for k in range(a,b,incr):
                if(start<=yb and board[int(str(k)+str(start))]!=player):
                    board[int(str(k)+str(start))]=player
                    count+=1
                start+=1;
    return count;


def check_for_straight_line(a,b,opp):
    '''
    checks if a players ath disk and probable bth disk are in a straight line and that there exists
    at least one opponent disk between disk a and  b
    '''
    x1 = int(a/10)
    y1 = a%10;
    x2 = int(b/10)
    y2 = b%10;
    #
    # if(x1==3 and y1==6 and x2==1 and y2==4):
    #     import pdb; pdb.set_trace()

    d1 = x2-x1
    d2 = y2-y1


    if( x1==x2 or y1==y2 or (abs(d1) == abs(d2))):
        for i in opp:
            x3 = int(i/10)
            y3 = i%10
            len1 = math.sqrt((abs(x1-x3)**2) + (abs(y1-y3)**2))
            len2 = math.sqrt((abs(x2-x3)**2) + (abs(y2-y3)**2))
            len3 = math.sqrt((abs(x1-x2)**2) + (abs(y1-y2)**2))
            len4 = len1+len2;
            if(len4 == len3):
                if(x1<x2):
                    xs = x1;xb=x2
                else:
                    xs = x2;xb=x1
                if(y1<y2):
                    ys = y1;yb=y2
                else:
                    ys = y2;yb=y1


                if(x1==x2):
                    for i in range(ys+1,yb):
                            if(board[int(str(x1)+str(i))]=='.'):
                                return False

                elif(y1==y2):
                    for i in range(xs+1,xb):
                            if(board[int(str(i)+str(y1))]=='.'):
                                return False
                else:
                        # if(x1==3 and y1==6 and x2==1 and y2==4):
                        #     import pdb; pdb.set_trace()
                        slope = (y2-y1)/(x2-x1)
                        start  = ys;
                        if(slope<0):
                            a = xb;b=xs;incr = -1
                        else:
                            a = xs;b=xb;incr = 1

                        count =0;

                        for k in range(a,b,incr):
                            if(start<=yb and board[int(str(k)+str(start))]=='.'):
                                count+=1
                            start+=1;

                        if(a==x2 and count<=1):
                            return True
                        if(count>0):
                            return False
                return True

def get_empty_around_piece(piece,board):
    '''
    returns a list of empty spaces around a piece on the board
    '''
    x = int(piece/10)
    y = piece%10;
    surroundings = []
    surroundings.append([x-1,y])#up
    surroundings.append([x+1,y])#down
    surroundings.append([x,y-1])#left
    surroundings.append([x,y+1])#right
    surroundings.append([x-1,y-1])#top_left
    surroundings.append([x-1,y+1])#top_right
    surroundings.append([x+1,y-1])#bottom_right
    surroundings.append([x+1,y+1])#bottom_left
    result = []
    for each in surroundings:
        i = int(''.join(str(e) for e in each))
        if i in squares() and board[i] == '.':
            result.append(i)
    return result;

def get_legal_moves(player,board):
    '''
    return legal moves for a player on the board
    '''
    if player=='o':
        opp = '@'
    else:
        opp = 'o'

    legals = {}
    ownpieces = []
    opppieces = []

    for i in  squares():
        if(board[i]==player):
            ownpieces.append(i)
    for i in squares():
        if(board[i]==opp):
            opppieces.append(i)


    empty_arround_opponent = []
    for op in opppieces:
        empty_arround_opponent.extend(get_empty_around_piece(op,board))

    for j in empty_arround_opponent:
        for i in ownpieces:
                if(check_for_straight_line(i,j,opppieces)):
                    legals[j] = i;
    print("Turn:" + player)
    return legals



if __name__ == '__main__':
    player_score = 2
    comp_score = 2
    board = initial_board()
    print(print_board(board))
    print("You: "+str(player_score)+"\tComputer: "+str(comp_score))


    while True:
            moves = get_legal_moves('@',board)#gets legal moves for the player
            print("Your choices: " + str(moves.keys()))#accepts the choice from the player
            move = int(input('Enter Choice:'))#accepts the choice from the player
            if (move in moves.keys()):
                board[move] = '@';#puts players disk at chosen space
                player_score+=1
                num = do_flips('@',move,moves[move],board)#flips opponent's pieces accordingly
                print(num)
                player_score+=num
                comp_score-=num
                print(print_board(board))
                print("You: "+str(player_score)+"\tComputer: "+str(comp_score))
                if(game_over(board)):#checks if game is over
                    exit();
            computer_moves = get_legal_moves('o',board)#gets legal moves for the compute
            print("Computer Choices: "+ str(computer_moves.keys()))
            # Random Moves by Computer.
            # a,b = computer_moves.popitem()#choses first legal move in the dictionary
            alpha, a = alphabeta('o', board, MIN_VALUE, MAX_VALUE, 7)
            # Change 7 here in the above code to make it a strong/weak player.
            b = computer_moves[a]
            print("Move chosen:" + str(a))
            board[a] = 'o';
            comp_score+=1
            num = do_flips('o',a,b,board)
            print(num)
            player_score-=num
            comp_score+=num
            print(print_board(board))
            print("You: "+str(player_score)+"\tComputer: "+str(comp_score))
            if(game_over(board)):
                exit();
