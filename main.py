from pypokerengine.api.game import setup_config, start_poker
from PokerAI import PokerAI
from NitBot import NitBot
from TAGBot import TAGBot
from ManiacBot import ManiacBot

if __name__ == '__main__':

    num_hands = 100000
    initial_stack = 2000  # Exactly 100BB
    small_blind = 10
    big_blind = 20

    # The Master Ledger
    ledger = {
        'Poker AI': 0,
        'Tight Passive Bot': 0,
        'Tight Aggressive Bot': 0,
        'Maniac Bot': 0
    }

    print(f'Running rigorous cash game simulation for {num_hands} hands...')
    
    for i in range(num_hands):
        # Initialize a 1-hand configuration to force a stack reset
        config = setup_config(max_round=1, initial_stack=initial_stack, small_blind_amount=small_blind)

        config.register_player(name='Poker AI', algorithm=PokerAI())
        config.register_player(name='Tight Passive Bot', algorithm=NitBot())
        config.register_player(name='Tight Aggressive Bot', algorithm=TAGBot())
        config.register_player(name='Maniac Bot', algorithm=ManiacBot())

        # Suppress output to run the loop rapidly
        game_result = start_poker(config, verbose=0)

        # Update the master ledger
        for player in game_result['players']:
            profit = player['stack'] - initial_stack
            ledger[player['name']] += profit
            
        if (i + 1) % 100 == 0:
            print(f'Completed {i + 1} hands...')

    # Output Final Metrics
    print('\n--- CASH GAME BENCHMARK RESULTS ---')
    for name, total_profit in ledger.items():
        bb_per_100 = (total_profit / big_blind) / (num_hands / 100)
        print(f'{name}: Raw Profit = {total_profit} | BB/100 = {round(bb_per_100, 2)}')