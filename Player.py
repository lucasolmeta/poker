import Card

class Player:
    def __init__(self):
        self.cardOne = Card()
        self.cardTwo = Card()
    
    def card_one(self):
        return self.cardOne
    
    def card_two(self):
        return self.cardTwo
    
    def cards(self):
        return [self.cardOne, self.cardTwo]