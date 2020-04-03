import game
import utility

def check(move, player, board):
    return game.is_valid(move) and game.is_legal(move, player, board)

def human(player, board):
    print(game.print_board(board))
    print('Your move?')
    while True:
        move = input('> ')
        if move and check(int(move), player, board):
            return int(move)
        elif move:
            print('Illegal move--try again.')

def get_choice(prompt, options):
    print(prompt)
    print('Options:',end =" ")
    utility.Utility.printKeys(options)
    while True:
        choice = input('> ')
        if choice in options:
            return options[choice]
        elif choice:
            print('Invalid choice.')

def get_players():
    print('Welcome to OTHELLO!')
    options = { 'human': human,
                'random': game.random_strategy}
    black = get_choice('BLACK: choose a strategy', options)
    white = get_choice('WHITE: choose a strategy', options)
    return black, white

def main():
    try:
        black, white = get_players()
        board, score = game.play(black, white)
    except game.IllegalMoveError as e:
        print(e)
        return
    except EOFError as e:
        print('Goodbye.')
        return
    print('Final score:'), score
    print('%s wins!' % ('Black' if score > 0 else 'White'))
    print(game.print_board(board))

if __name__ == '__main__':
    main()
