from Card import Card
import random

class Deck:
    def __init__(self, exclude: list = None):
        self.cards = [Card(r, s) for r in range(2, 15) for s in range(4)]
        self.shuffle()

        if exclude:
            for card in exclude:
                self.cards.remove(card)

    def shuffle(self):
        random.shuffle(self.cards)
    
    def burn(self):
        try:
            del self.cards[-1]
        except:
            raise IndexError('Deck only contains 52 cards!')

    def deal(self, num_cards):
        try:
            if num_cards == 1:
                return self.cards.pop()
            else:
                return [self.cards.pop() for _ in range(num_cards)]
        except:
            raise IndexError('Deck only contains 52 cards!')