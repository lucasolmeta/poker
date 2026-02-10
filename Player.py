from Card import Card

class Player:
    def __init__(self, cards: list):
        if len(cards) != 2:
            raise IndexError('Please submit 2 Cards!')
        if any([not isinstance(card, Card) for card in cards]):
            raise TypeError('All inputs must be Cards!')
        
        self.cards = cards
        self.balance = 1000
    
    def card(self, n: int):
        return self.cards[n]
    
    def cards(self):
        return self.cards
    
    def balance(self):
        return self.balance
    
    def to_str(self):
        return ", ".join([card.to_str() for card in self.cards if card is not None])