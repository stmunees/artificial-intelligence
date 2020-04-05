from game import othellogame,utility,multiAgent
def check(move, player, board):
    return othellogame.is_valid(move) and othellogame.is_legal(move, player, board)

def human(player, board):
    print(utility.Utility.print_board(board))
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

def get_choice(prompt, agents):
    print(prompt)
    print("Player's to choose from :",end =" ")
    utility.Utility.printKeys(agents)
    while True:
        choice = input('> ')
        if choice in agents:
            return agents[choice],choice
        elif choice:
            print('Invalid choice.')

def get_players():
    print('!OTHELLO!'.center(20))
    agents = {  'human': human,
                'random': multiAgent.random_strategy,
                'alpha':multiAgent.alphabeta_strategy,
                'expec':multiAgent.expectimax_strategy,
                'minmax':multiAgent.minimax_strategy}
    black,choice = get_choice('Choose player using BLACK:', agents)
    if choice in ['alpha','expec','minmax']:
        agents.pop(choice)
    white,choice = get_choice('Choose plyer using WHITE:', agents)
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
    print(utility.Utility.print_board(board))

if __name__ == '__main__':
    main()
