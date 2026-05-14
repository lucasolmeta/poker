from .card import Card

class Player:
    def __init__(self, cards: list):
        if len(cards) != 2:
            raise IndexError('Please submit 2 Cards!')
        if any([not isinstance(card, Card) for card in cards]):
            raise TypeError('All inputs must be Cards!')
        
        self.card_list = cards
    
    def card(self, n: int):
        return self.card_list[n]
    
    def cards(self):
        return self.card_list
    
    def to_str(self):
        return ", ".join([card.to_str() for card in self.card_list if card is not None])