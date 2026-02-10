import Card

class Board:
    def __init__(self, cards: list) -> None:
        if len(cards) != 3:
            raise IndexError('Please submit 3 Cards!')
        if any([not isinstance(card, Card) for card in cards]):
            raise TypeError('All inputs must be Cards!')
        
        self.cards = [None] * 5
        self.cards[:3] = cards

    def set_turn(self, card: Card) -> None:
        self.cards[3] = card

    def set_river(self, card: Card) -> None:
        self.cards[4] = card

    def card(self, n: int):
        return self.cards[n]
    
    def cards(self):
        return self.cards