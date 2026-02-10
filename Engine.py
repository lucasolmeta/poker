import Player
import Board
import Deck

class Card:
    def __init__(self):
        self.rank = self.init_rank()
        self.suit = self.init_suit()