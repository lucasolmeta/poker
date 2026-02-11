from Player import Player
from Board import Board
from collections import Counter

class Evaluator:
    def __init__(self):
        pass

    def evaluate_hand(self, player: Player, board: Board):
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
            return
        
        s_cards = [c for c in cards if c.suit == target_suit]
        
        for i in range(len(s_cards) - 4):
            if s_cards[i].rank() - s_cards[i+4].rank() == 4:
                high_card = s_cards[i]
                
                if high_card == 14:
                    return 9 << 40
                
                return (8 << 40) + (high_card << 32)

        wheel_ranks = {14, 5, 4, 3, 2}
        if wheel_ranks.issubset(set(s_cards)):
            return (8 << 40) + (5 << 32)

        return 0
    
    def four_of_kind(self, cards: list):
        rank_counts = Counter(card.rank() for card in cards)
        for rank, count in rank_counts.items():
            if count == 4:
                kicker = max(c.rank() for c in cards if c.rank() != rank)
                return (7 << 40) + (rank << 32) + (kicker << 24)
    
    def full_house(self, cards: list):
        rank_counts = Counter(card.rank() for card in cards)

        threes = sorted([r for r, c in rank_counts.items() if c == 3], reverse=True)
        twos = sorted([r for r, c in rank_counts.items() if c >= 2], reverse=True)
        
        if threes and len(twos) > 1:
            pair_rank = twos[1] if twos[0] == threes[0] else twos[0]
            return (6 << 40) + (threes[0] << 32) + (pair_rank << 24)
    
    def flush(self, cards: list):
        suit_counts = Counter(card.suit() for card in cards)

        for suit, count in suit_counts.items():
            if count >= 5:
                suited = sorted([c.rank() for c in cards if c.suit() == suit], reverse=True)[:5]
                score = 5 << 40
                for i, rank in enumerate(suited):
                    score += rank << (8 * (4 - i))
                return score
    
    def straight(self, cards: list):
        for i in range(len(cards) - 4):
            if cards[i].rank() - cards[i+4].rank() == 4:
                high_card = cards[i]
                
                return (8 << 40) + (high_card << 32)
            
        wheel_ranks = {14, 5, 4, 3, 2}
        if wheel_ranks.issubset(set(cards)):
            return (8 << 40) + (5 << 32)
    
    def three_of_kind(self, cards: list):
        rank_counts = Counter(card.rank() for card in cards)
        three_rank = next((r for r, c in rank_counts.items() if c == 3), None)

        if three_rank:
            kickers = sorted([r for r in rank_counts.keys() if r != three_rank], reverse=True)[:2]
            score = (3 << 40) + (three_rank << 32)
            score += (kickers[0] << 24) + (kickers[1] << 16)
            return score
        
        return 0
            
    def two_pair(self, cards: list):
        rank_counts = Counter(card.rank() for card in cards)
        pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
    
        if len(pairs) >= 2:
            high_pair = pairs[0]
            low_pair = pairs[1]
            kicker = max(r for r in rank_counts.keys() if r != high_pair and r != low_pair)
            
            return (2 << 40) + (high_pair << 32) + (low_pair << 24) + (kicker << 16)
        return 0
    
    def pair(self, cards: list):
        rank_counts = Counter(card.rank() for card in cards)
        pair_rank = next((r for r, c in rank_counts.items() if c == 2), None)
        
        if pair_rank:
            kickers = sorted([r for r in rank_counts.keys() if r != pair_rank], reverse=True)[:3]
            score = (1 << 40) + (pair_rank << 32)
            for i, rank in enumerate(kickers):
                score += rank << (8 * (3 - i))
            return score
        return 0
            
    def high_card(self, cards: list):
        ranks = cards[:5]

        score = 0
        for i, rank in enumerate(ranks):
            score += rank << (8 * (4 - i))
        return score