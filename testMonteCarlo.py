from Card import Card
from Deck import Deck
from Player import Player
from Evaluator import Evaluator

deck = Deck()
evaluator = Evaluator()
player = Player( deck.deal(2) )

num_sims = 10000
num_opps = 5
equity = evaluator.hand_equity( [Card(9,1),Card(9,2)], num_sims, num_opps, graph=True )

print(f'{round(equity * 100,2)}% Equity')