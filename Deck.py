from Card import Card
import random

class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for r in range(2, 15) for s in range(4)]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)
    
    def burn(self):
        try:
            del self.cards[-1]
        except:
            raise IndexError('Deck only contains 52 cards!')

    def deal(self, num_cards):
        try:
            return [self.cards.pop() for _ in range(num_cards)]
        except:
            raise IndexError('Deck only contains 52 cards!')