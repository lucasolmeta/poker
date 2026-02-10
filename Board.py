from Card import Card

class Board:
    def __init__(self, cards: list) -> None:
        if len(cards) != 3:
            raise IndexError('Please submit 3 Cards!')
        if any([not isinstance(card, Card) for card in cards]):
            raise TypeError('All inputs must be Cards!')
        
        self.cards = [None] * 5
        self.cards[:3] = cards

    def set_turn(self, card: Card) -> None:
        if isinstance(card, Card):
            self.cards[3] = card
        else:
            raise TypeError('Input must be a card!')

    def set_river(self, card: Card) -> None:
        if isinstance(card, Card):
            self.cards[4] = card
        else:
            raise TypeError('Input must be a card!')

    def card(self, n: int):
        return self.cards[n]
    
    def cards(self):
        return self.cards
    
    def to_str(self):
        return ', '.join([card.to_str() for card in self.cards if card is not None])