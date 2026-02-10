import random
import math

class Card:
    def __init__(self):
        self.rank = self.init_rank()
        self.suit = self.init_suit()

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def init_rank(self) -> int:
        rank = math.floor(random.random() * 13) + 2
        return rank
    
    def init_suit(self) -> int:
        suit = math.floor(random.random() * 4)
        return suit
    
    def suit(self) -> int:
        return self.suit
    
    def rank(self) -> int:
        return self.rank