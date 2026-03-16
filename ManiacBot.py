from pypokerengine.players import BasePokerPlayer
import random

class ManiacBot( BasePokerPlayer ):
    
    def declare_action(self, valid_actions, hole_card, round_state):
        
        call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']

        raise_action = [item for item in valid_actions if item['action'] == 'raise']
        can_raise = len(raise_action) > 0 and raise_action[0]['amount']['min'] != -1

        action_roll = random.random()

        if can_raise and action_roll < 0.50:
            min_raise = raise_action[0]['amount']['min']
            max_raise = raise_action[0]['amount']['max']
            cap = min(max_raise, min_raise * 3)
            raise_amnt = random.randint(min_raise, cap)
            return 'raise', raise_amnt
            
        elif action_roll < 0.80:
            return 'call', call_amount
            
        else:
            if call_amount == 0:
                return 'call', 0
            return 'fold', 0

    def receive_game_start_message(self, game_info): pass
    def receive_round_start_message(self, round_count, hole_card, seats): pass
    def receive_street_start_message(self, street, round_state): pass
    def receive_game_update_message(self, action, round_state): pass
    def receive_round_result_message(self, winners, hand_info, round_state): pass