import random
import math

class Card:
    def __init__(self, rank: int, suit: int):
        self.rank = rank
        self.suit = suit
    
    def rank(self):
        return self.rank
    
    def suit(self):
        return self.suit
    
    def to_str(self):
        ranks = {
            2: '2',
            3: '3',
            4: '4',
            5: '5',
            6: '6',
            7: '7',
            8: '8',
            9: '9',
            10: '10',
            11: 'J',
            12: 'Q',
            13: 'K',
            14: 'A'
        }

        suits = {
            0: 'Clubs',
            1: 'Diamonds',
            2: 'Hearts',
            3: 'Spades',
        }

        rank = ranks[self.rank]
        suit = suits[self.suit]

        return f'{rank} of {suit}'