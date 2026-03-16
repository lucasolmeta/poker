from pypokerengine.api.game import setup_config, start_poker
from PokerAI import PokerAI
from CallBot import CallBot
from NitBot import NitBot
from TAGBot import TAGBot
from ManiacBot import ManiacBot
from RandomBot import RandomBot

if __name__ == '__main__':

    # Simulation parameters
    
    num_hands = 500
    initial_stack = 1000000000
    small_blind = 10
    big_blind = 20

    # Initialize the PyPokerEngine configuration
    
    config = setup_config(max_round=num_hands, initial_stack=initial_stack, small_blind_amount=small_blind)

    # Register the players
    
    config.register_player(name='EV_Bot', algorithm=PokerAI())
    config.register_player(name='Tight Passive Bot', algorithm=NitBot())
    config.register_player(name='Tight Aggressive Bot', algorithm=TAGBot())
    config.register_player(name='Maniac Bot', algorithm=ManiacBot())
    config.register_player(name='Random Bot', algorithm=RandomBot())

    # Run the simulation
    
    print(f'Starting simulation for {num_hands} hands...')
    game_result = start_poker(config, verbose=0)

    # Extract and calculate final resume metrics
    
    print('\n--- SIMULATION RESULTS ---')
    
    for player in game_result['players']:
        
        name = player['name']
        final_stack = player['stack']
        
        # Calculate raw profit
        
        profit = final_stack - initial_stack
        
        # Calculate BB/100
        
        bb_per_100 = (profit / big_blind) / (num_hands / 100)
        
        print(f'{name}: Final Stack = {final_stack} | Raw Profit = {profit} | BB/100 = {round(bb_per_100, 2)}')