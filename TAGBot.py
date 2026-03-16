from pypokerengine.players import BasePokerPlayer
import random

class TAGBot( BasePokerPlayer ):
    
    def declare_action(self, valid_actions, hole_card, round_state):
        
        call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']

        raise_action = [item for item in valid_actions if item['action'] == 'raise']
        can_raise = len(raise_action) > 0 and raise_action[0]['amount']['min'] != -1

        ranks = [c[1] for c in hole_card]
        is_pair = ranks[0] == ranks[1]
        playable = is_pair or any(r in 'TJQKA' for r in ranks)

        if not playable:
            if call_amount == 0: 
                return 'call', 0
            return 'fold', 0

        if can_raise and random.random() < 0.60:
            min_raise = raise_action[0]['amount']['min']
            max_raise = raise_action[0]['amount']['max']
            ideal_raise = min_raise * 2 
            return 'raise', max(min_raise, min(ideal_raise, max_raise))

        return 'call', call_amount

    def receive_game_start_message(self, game_info): pass
    def receive_round_start_message(self, round_count, hole_card, seats): pass
    def receive_street_start_message(self, street, round_state): pass
    def receive_game_update_message(self, action, round_state): pass
    def receive_round_result_message(self, winners, hand_info, round_state): pass