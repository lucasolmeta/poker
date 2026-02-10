import Card

class Player:
    def __init__(self, cards: list):
        if len(cards) != 2:
            raise IndexError('Please submit 2 Cards!')
        if any([not isinstance(card, Card) for card in cards]):
            raise TypeError('All inputs must be Cards!')
    
    def card_one(self):
        return self.cards[0]
    
    def card_two(self):
        return self.cards[1]
    
    def cards(self):
        return self.cards