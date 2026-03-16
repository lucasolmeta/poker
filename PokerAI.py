from pypokerengine.players import BasePokerPlayer
from Card import Card
from Evaluator import Evaluator
import random

class PokerAI( BasePokerPlayer ):
    def __init__(self):
        super().__init__()
        self.evaluator = Evaluator()
        self.opp_folds = 0
        self.opp_actions = 0
        self.fold_frequency = 0.0

    def declare_action(self, valid_actions, hole_card, round_state):

        # Get community cards
    
        community_cards = round_state['community_card']

        # Get pot size

        pot_size = round_state['pot']['main']['amount']

        # Get call amount
        
        call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']

        # Get minimum and maximum raises

        raise_action = [item for item in valid_actions if item['action'] == 'raise']
        can_raise = len(raise_action) > 0 and raise_action[0]['amount']['min'] != -1
        
        if can_raise:
            min_raise = raise_action[0]['amount']['min']
            max_raise = raise_action[0]['amount']['max']

        # Calculate pot odds
        
        pot_odds = 0 if (pot_size + call_amount) == 0 else call_amount / (pot_size + call_amount)

        # Calculate number of active opponents

        active_opps = 0
        for player in round_state['seats']:
            if player['state'] != 'folded' and player['uuid'] != self.uuid:
                active_opps += 1

        # Safety catch for uncontested pots

        if active_opps == 0:
            return 'call', call_amount

        # Convert AI cards and community cards to Card() objects
        
        my_cards = [Card.from_str(c) for c in hole_card]
        board = [Card.from_str(c) for c in community_cards]

        # Calculate equity for current hand

        equity = self.evaluator.hand_equity( my_cards, 1000, active_opps, board=board )

        # Calculate advantage

        advantage = equity - pot_odds

        # Raise, call, and fold logic
        
        if advantage > 0:
            if can_raise:
                if pot_odds == 0:
                    ideal_raise = int(pot_size * 0.5)
                else:
                    ideal_raise = int(equity / pot_odds * call_amount)
            
                raise_amount = max(min_raise, min(ideal_raise, max_raise))
                return 'raise', raise_amount
            else:
                return 'call', call_amount
        elif advantage == 0 or call_amount == 0:
            return 'call', call_amount
        else:
            max_bluff_rate = 0.2

            bluff_threshold = equity / pot_odds * max_bluff_rate * self.fold_frequency

            if random.random() < bluff_threshold and can_raise:
                return 'raise', min_raise
            else:
                return 'fold', 0

    def receive_round_result_message(self, winners, hand_info, round_state):
        for street in round_state['action_histories']:
            for action in round_state['action_histories'][street]:
                if action['uuid'] != self.uuid: 
                    self.opp_actions += 1
                    if action['action'] == 'FOLD':
                        self.opp_folds += 1
                    
                    self.fold_frequency = self.opp_folds / self.opp_actions

    def receive_game_start_message(self, game_info):
        pass
    def receive_round_start_message(self, round_count, hole_card, seats):
        pass
    def receive_street_start_message(self, street, round_state):
        pass
    def receive_game_update_message(self, action, round_state):
        pass