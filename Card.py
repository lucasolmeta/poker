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
            2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
            8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'
        }

        suits = {
            0: 'c', 1: 'd', 2: 'h', 3: 's',
        }

        rank = ranks[self.r]
        suit = suits[self.s]

        return rank + suit
    
    @classmethod
    def from_str(cls, card_str: str):

        ranks = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
            '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        suits = {
            'c': 0, 'd': 1, 'h': 2, 's': 3
        }

        s_str = card_str[0].lower()
        r_str = card_str[1].upper()

        return cls(ranks[r_str], suits[s_str])
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.r == other.r and self.s == other.s
        return False