from Player import Player
from Board import Board
from Deck import Deck

class Game:
    def __init__(self, n: int):
        self.deck = Deck()
        self.players = [None] * n

        for i in range(n):
            self.players[i] = Player( self.deck.deal(2) )
        
        self.board = Board( self.deck.deal(3) )
    
    def print_players(self):
        for i, player in enumerate(self.players):
            print( f'Player {i + 1}: {player.to_str()}' )

    def print_board(self):
        print( f'Board: {self.board.to_str()}' )