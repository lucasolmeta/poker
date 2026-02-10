from Card import Card

class Player:
    def __init__(self, cards: list):
        if len(cards) != 2:
            raise IndexError('Please submit 2 Cards!')
        if any([not isinstance(card, Card) for card in cards]):
            raise TypeError('All inputs must be Cards!')
        
        self.cards = cards
        self.balance = 1000
        self.is_folded = False

    def get_action(self, call_amount):
        if call_amount == 0:
            options = "(check, raise, fold)"
        else:
            options = f"(call {call_amount}, raise, fold)"

            while True:
                choice = input(f'What would you like to do? {options}: ').lower().strip()
                if choice == 'fold':
                    return ('fold', 0)
                if choice == 'check' and call_amount == 0:
                    return ('check', 0)
                if choice == 'call' and call_amount > 0:
                    self.balance -= call_amount
                    return ('call', call_amount)
                if choice == 'raise':
                    while True:
                        raise_amount = input("Enter TOTAL amount to raise to: ")
                        if raise_amount.isdigit():
                            self.balance -= (call_amount + int(raise_amount))
                            return ('raise', int(raise_amount))
    
    def card(self, n: int):
        return self.cards[n]
    
    def cards(self):
        return self.cards
    
    def folded(self):
        return self.is_folded
    
    def to_str(self):
        return ", ".join([card.to_str() for card in self.cards if card is not None])