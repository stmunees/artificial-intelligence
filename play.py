from game import othellogame,utility
def check(move, player, board):
    return othellogame.is_valid(move) and othellogame.is_legal(move, player, board)

def human(player, board):
    print(othellogame.print_board(board))
    print('Your move?')
    while True:
        utility.Utility.printLegalMoves(othellogame.legal_moves(player, board))
        try:
          val = int(input('> '))
          if val and check(val, player, board):
            return val
          elif val:
            print('Illegal move--try again.')
        except ValueError:
          print("That's not an integer!")

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
                'random': othellogame.random_strategy}
    black = get_choice('BLACK: choose a strategy', options)
    white = get_choice('WHITE: choose a strategy', options)
    return black, white

def main():
    try:
        black, white = get_players()
        board, score = othellogame.play(black, white)
    except othellogame.IllegalMoveError as e:
        print(e)
        return
    except EOFError as e:
        print('Goodbye.')
        return
    print('Final score:'), score
    print('%s wins!' % ('Black' if score > 0 else 'White'))
    print(othellogame.print_board(board))

if __name__ == '__main__':
    main()
