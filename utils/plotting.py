import matplotlib.pyplot as plt

def plot_equity_convergence(sim_num, equity_tracker, final_equity, cards, opps):
    plt.plot(range( 1 , sim_num + 1 ), equity_tracker, label=f'Final Win Percentage: {final_equity:.2%}')
    plt.xlabel('Simulation #')
    plt.ylabel('Hand Equity')
    plt.title(f'Hand Equity Over Time For {cards[0].to_str()}, {cards[1].to_str()}')
    plt.ylim(0, 1)
    plt.axhline(y=round(1.0/(1+opps), 3), color='gray', linestyle='--', alpha=0.7)
    plt.yticks([0, 0.5, 1, round(1.0/(1+opps), 3)], ['0%', '50%', '100%', f'{round(1.0/(1+opps)*100, 1)}%'])
    plt.legend(handlelength=0.5)     
    plt.show()