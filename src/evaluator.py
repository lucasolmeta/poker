from collections import Counter

from .board import Board
from .deck import Deck
from .player import Player

class Evaluator:
    def __init__(self):
        pass

    def score_hand(self, player: Player, board: Board):
        """
        Returns score used to evaluate strength of hand
        """

        cards = player.cards() + board.cards()
        cards.sort(key=lambda card: (card.rank(), card.suit()), reverse=True)
        
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
        """
        Scores hand as straight flush or returns zero if straight flush not found
        """

        suit_counts = Counter(card.suit() for card in cards)
        target_suit = None

        for suit, count in suit_counts.items():
            if count >= 5:
                target_suit = suit
                break
        
        if target_suit is None:
            return
        
        s_cards = [c for c in cards if c.suit() == target_suit]
        unique_ranks = sorted(list(set(c.rank() for c in s_cards)), reverse=True)  

        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i+4] == 4:
                high_card = unique_ranks[i]
                
                if high_card == 14:
                    return 9 << 40
                
                return (8 << 40) + (high_card << 32)

        wheel_ranks = {14, 5, 4, 3, 2}
        if wheel_ranks.issubset(set(unique_ranks)):
            return (8 << 40) + (5 << 32)

        return 0
    
    def four_of_kind(self, cards: list):
        """
        Scores hand as four of a kind or returns zero if no four of a kind is found
        """

        rank_counts = Counter(card.rank() for card in cards)
        for rank, count in rank_counts.items():
            if count == 4:
                kicker = max(c.rank() for c in cards if c.rank() != rank)
                return (7 << 40) + (rank << 32) + (kicker << 24)
            
        return 0
    
    def full_house(self, cards: list):
        """
        Scores hand as full house or returns zero if no full house is found
        """

        rank_counts = Counter(card.rank() for card in cards)

        threes = sorted([r for r, c in rank_counts.items() if c == 3], reverse=True)
        twos = sorted([r for r, c in rank_counts.items() if c >= 2], reverse=True)
        
        if threes and len(twos) > 1:
            pair_rank = twos[1] if twos[0] == threes[0] else twos[0]
            return (6 << 40) + (threes[0] << 32) + (pair_rank << 24)
        
        return 0
    
    def flush(self, cards: list):
        """
        Scores hand as flush or returns zero if no flush is found
        """
         
        suit_counts = Counter(card.suit() for card in cards)

        for suit, count in suit_counts.items():
            if count >= 5:
                suited = sorted([c.rank() for c in cards if c.suit() == suit], reverse=True)[:5]
                score = 5 << 40
                for i, rank in enumerate(suited):
                    score += rank << (8 * (4 - i))
                return score
            
        return 0
    
    def straight(self, cards: list):
        """
        Scores hand as straight or returns zero if no straight is found
        """

        unique_ranks = sorted(list(set(c.rank() for c in cards)), reverse=True)

        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i+4] == 4:
                high_card = unique_ranks[i]
                
                return (4 << 40) + (high_card << 32)
            
        wheel_ranks = {14, 5, 4, 3, 2}
        if wheel_ranks.issubset(set(unique_ranks)):
            return (4 << 40) + (5 << 32)
        
        return 0
    
    def three_of_kind(self, cards: list):
        """
        Scores hand as three of a kind or returns zero if no three of a kind is found
        """

        rank_counts = Counter(card.rank() for card in cards)
        three_rank = next((r for r, c in rank_counts.items() if c == 3), None)

        if three_rank:
            kickers = sorted([r for r in rank_counts.keys() if r != three_rank], reverse=True)[:2]
            score = (3 << 40) + (three_rank << 32)
            score += (kickers[0] << 24) + (kickers[1] << 16)
            return score
        
        return 0
            
    def two_pair(self, cards: list):
        """
        Scores hand as two pair or returns zero if two pairs not found
        """

        rank_counts = Counter(card.rank() for card in cards)
        pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
    
        if len(pairs) >= 2:
            high_pair = pairs[0]
            low_pair = pairs[1]
            kicker = max(r for r in rank_counts.keys() if r != high_pair and r != low_pair)
            
            return (2 << 40) + (high_pair << 32) + (low_pair << 24) + (kicker << 16)
        
        return 0
    
    def pair(self, cards: list):
        """
        Scores hand as pair or returns zero if pair not found
        """

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
        """
        Scores hand as high card
        """
         
        ranks = [card.rank() for card in cards[:5]]

        score = 0
        for i, rank in enumerate(ranks):
            score += rank << (8 * (4 - i))
        return score

    def hand_equity( self, cards: list, sim_num: int, opps: int, board=None ):
        """
        Runs a monte-carlo simulation to approximate equity of a given hand with a given board
        """

        # Default the board to nothing if no parameter passed

        if board is None:
            board = []

        # Track equity over time

        total_equity = 0
        equity_tracker = []

        # Run the simulation sim_num times

        for i in range( sim_num ):

            # Make a new deck excluding player's cards and those on the board

            deck = Deck( cards + board )

            # Create the simulation board

            if len(board) == 0:
                sim_board = Board( deck.deal(3) )
                sim_board.set_turn( deck.deal(1) )
                sim_board.set_river( deck.deal(1) )
            elif len(board) == 3:
                sim_board = Board( board[:3] )
                sim_board.set_turn( deck.deal(1) )
                sim_board.set_river( deck.deal(1) )
            elif len(board) == 4:
                sim_board = Board( board[:3] )
                sim_board.set_turn( board[3] )
                sim_board.set_river( deck.deal(1) )
            elif len(board) == 5:
                sim_board = Board( board[:3] )
                sim_board.set_turn( board[3] )
                sim_board.set_river( board[4] )

            # Create hands for each player and score each of their hands

            players = [Player( deck.deal(2) ) for _ in range(opps)]
            odds = [self.score_hand(player, sim_board) for player in players]

            # Initialize player object with passed hand and score it

            player = Player(cards)
            score = self.score_hand(player, sim_board)

            # Find the highest score among the opponents

            max_opp_score = max(odds)

            # Recalculate total equity, print progress, and append to equity tracker

            if score >= max_opp_score:
                total_equity += 1.0 / ( 1.0 + odds.count(score) )

            equity_tracker.append(total_equity / (i + 1))

            if sim_num >= 10 and (i + 1) % (sim_num // 10) == 0:
                print(f'{round(100 * (i + 1) / sim_num, 2)}% Complete')

        # Calculate and return average equity per hand

        final_equity = total_equity / sim_num

        # Return final win and tie probabilities

        return final_equity, equity_tracker