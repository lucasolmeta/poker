import random
import math

class Card:
    def __init__(self, rank: int, suit: int):
        self.r = rank
        self.s = suit
    
    def rank(self):
        return self.r
    
    def suit(self):
        return self.s
    
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
            11: 'Jack',
            12: 'Queen',
            13: 'King',
            14: 'Ace'
        }

        suits = {
            0: 'Clubs',
            1: 'Diamonds',
            2: 'Hearts',
            3: 'Spades',
        }

        rank = ranks[self.r]
        suit = suits[self.s]

        return f'{rank} of {suit}'