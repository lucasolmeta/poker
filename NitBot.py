from pypokerengine.players import BasePokerPlayer
import random

class NitBot( BasePokerPlayer ):
    
    def declare_action(self, valid_actions, hole_card, round_state):
        
        call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']

        if call_amount == 0:
            return 'call', 0

        # Pre-flop: Only play pairs or broadway cards (T, J, Q, K, A)
        
        ranks = [c[1] for c in hole_card]
        is_pair = ranks[0] == ranks[1]
        high_cards = all(r in 'TJQKA' for r in ranks)

        if round_state['street'] == 'preflop':
            if is_pair or high_cards:
                return 'call', call_amount
            else:
                return 'fold', 0

        # Post-flop: Extremely passive. Folds to bets 80% of the time.
        
        if random.random() < 0.20:
            return 'call', call_amount
            
        return 'fold', 0

    def receive_game_start_message(self, game_info): pass
    def receive_round_start_message(self, round_count, hole_card, seats): pass
    def receive_street_start_message(self, street, round_state): pass
    def receive_game_update_message(self, action, round_state): pass
    def receive_round_result_message(self, winners, hand_info, round_state): pass