from pypokerengine.players import BasePokerPlayer
import random

class RandomBot( BasePokerPlayer ):
    
    def declare_action(self, valid_actions, hole_card, round_state):
        
        # Pick a random valid action
        
        action = random.choice(valid_actions)
        
        if action['action'] == 'fold':
            return 'fold', 0
            
        elif action['action'] == 'call':
            return 'call', action['amount']
            
        else:
            min_raise = action['amount']['min']
            max_raise = action['amount']['max']
            
            # If raising is illegal, default to call
            
            if min_raise == -1:
                call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']
                return 'call', call_amount
                
            raise_amnt = random.randint(min_raise, max_raise)
            return 'raise', raise_amnt

    # Required PyPokerEngine placeholder methods
    
    def receive_game_start_message(self, game_info): pass
    def receive_round_start_message(self, round_count, hole_card, seats): pass
    def receive_street_start_message(self, street, round_state): pass
    def receive_game_update_message(self, action, round_state): pass
    def receive_round_result_message(self, winners, hand_info, round_state): pass