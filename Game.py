from Player import Player
from Board import Board
from Deck import Deck

class Game:
    def __init__(self, n: int):
        self.deck = Deck()
        self.players = [None] * n

        for i in range(n):
            self.players[i] = Player( self.deck.deal(2) )

        self.pot = 0
    
    def betting_round(self):
        last_aggressor = -1
        action_on = 0
        call_amount = 0

        while True:
            if action_on == last_aggressor:
                break

            if self.players[ action_on ].folded():
                action_on = (action_on + 1) % len(self.players)
                continue
            
            print('-----')
            print(f'Player {action_on + 1}:')
            print( self.players[ action_on ].to_str() )
            print('-----')

            action = self.players[ action_on ].get_action( call_amount )

            if action[0] == 'fold':
                action_on = (action_on + 1) % len(self.players)
                continue
            elif action[0] == 'check':
                if last_aggressor == -1:
                    last_aggressor = action_on
            elif action[0] == 'call':
                self.pot += action[1]

                if last_aggressor == -1:
                    last_aggressor = action_on
            elif action[0] == 'raise':
                self.pot += action[1]
                call_amount = action[1]

                last_aggressor = action_on

            action_on = (action_on + 1) % len(self.players)

    def deal_flop(self):
        self.board = Board( self.deck.deal(3) )

    def deal_turn(self):
        self.board.set_turn( self.deck.deal(1) )

    def deal_river(self):
        self.board.set_river( self.deck.deal(1) )
    
    def burn(self):
        self.deck.burn()
    
    def print_players(self):
        for i, player in enumerate(self.players):
            print( f'Player {i + 1}: {player.to_str()}' )

    def payout(self):
        #to be completed
        return

    def print_board(self):
        print('-----')
        print('BOARD:')
        print(self.board.to_str())