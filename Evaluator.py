from Player import Player
from Board import Board
from collections import Counter

class Evaluator:
    def __init__(self):
        pass

    def classify_hand(self, player: Player, board: Board):
        cards = player.cards() + board.cards()
        cards.sort(key=lambda card: (card.rank(), card.suit()))
        
        if score := self.straight_flush( cards ): return score
        if score := self.four_of_kind( cards ): return score
        if score := self.full_house( cards ): return score
        if score := self.flush( cards ): return score
        if score := self.straight( cards ): return score
        if score := self.three_of_kind( cards ): return score
        if score := self.two_pair( cards ): return score
        if score := self.pair( cards ): return score
        return self.high_card( cards )


    def straight_flush(self, cards: list):
        suit_counts = Counter(card.suit() for card in cards)
        target_suit = None

        for suit, count in suit_counts.items():
            if count >= 5:
                target_suit = suit
                break
        
        if target_suit is None:
            return 0
        
        s_cards = [c for c in cards if c.suit == target_suit]
        
        for i in range(len(s_cards) - 4):
            if s_cards[i].rank() - s_cards[i+4].rank() == 4:
                high_card = s_cards[i]
                
                if high_card == 14:
                    return
                
                return

        wheel_ranks = {14, 5, 4, 3, 2}
        if wheel_ranks.issubset(set(s_cards)):
            return

        return 0
    
    def four_of_kind(self, cards: list):
        rank_counts = Counter(card.rank() for card in cards)
        for rank, count in rank_counts.items():
            if count == 4:
                return
    
    def full_house(self, cards: list):
        rank_counts = Counter(card.rank() for card in cards)

        three_seen = False
        two_seen = False

        for rank, count in rank_counts.items():
            if count == 3:
                three_seen = True
            elif count == 2:
                two_seen = True

        if three_seen and two_seen:
            return
    
    def flush(self, cards: list):
        suit_counts = Counter(card.suit() for card in cards)

        for suit, count in suit_counts.items():
            if count >= 5:
                return
    
    def straight(self, cards: list):
        for i in range(len(cards) - 4):
            if cards[i].rank() - cards[i+4].rank() == 4:
                high_card = cards[i]
                
                return
    
    def three_of_kind(self, cards: list):
        rank_counts = Counter(card.rank() for card in cards)
        for rank, count in rank_counts.items():
            if count == 3:
                return
            
    def two_pair(self, cards: list):
        rank_counts = Counter(card.rank() for card in cards)
        pairs = 0

        for rank, count in rank_counts.items():
            if count == 2:
                pairs += 1
        
        if pairs >= 2:
            return
    
    def pair(self, cards: list):
        rank_counts = Counter(card.rank() for card in cards)

        for rank, count in rank_counts.items():
            if count == 2:
                return
            
    def high_card(self, cards: list):
        ranks = [card.rank() for card in cards]

        return