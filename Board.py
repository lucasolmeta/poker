import Card

class Board:
    def __init__(self):
        self.cardOne = Card()
        self.cardTwo = Card()
        self.cardThree = Card()
        self.cardFour = Card()
        self.cardFive = Card()

    def card_one(self):
        return self.cardOne
    
    def card_two(self):
        return self.cardTwo
    
    def card_three(self):
        return self.cardThree
    
    def card_four(self):
        return self.cardFour
    
    def card_five(self):
        return self.cardFive
    
    def cards(self):
        cards = [self.cardOne, self.cardTwo, self.cardThree, self.cardFour, self.cardFive]
        
        return cards