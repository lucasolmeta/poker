import matplotlib.pyplot as plt
import numpy as np

def plot_equity_convergence(sim_num, equity_tracker, final_equity, cards, opps):
    n_pts = len(equity_tracker)
    n_iterations = np.arange(1, n_pts + 1, dtype=float)

    p_hat = np.asarray(equity_tracker, dtype=float)
    standard_error = np.sqrt(np.maximum(0.0, (p_hat * (1.0 - p_hat)) / n_iterations))

    lower_bound = p_hat - 1.96 * standard_error
    upper_bound = p_hat + 1.96 * standard_error
    
    lower_plot = np.clip(lower_bound, 0.0, 1.0)
    upper_plot = np.clip(upper_bound, 0.0, 1.0)

    plt.plot(n_iterations, p_hat, label=f"Final Hand Equity: {final_equity:.2%}")
    plt.fill_between(
        n_iterations,
        lower_plot,
        upper_plot,
        alpha=0.22,
        color="C0",
        label="Approx. 95% bounds",
    )
    plt.plot(n_iterations, lower_plot, color="C0", linewidth=1.0, linestyle="--", alpha=0.85)
    plt.plot(n_iterations, upper_plot, color="C0", linewidth=1.0, linestyle="--", alpha=0.85)
    plt.xlabel("Simulation #")
    plt.ylabel("Hand Equity")
    plt.title(f'Hand Equity Over Time For {cards[0].to_str()}, {cards[1].to_str()}')
    plt.ylim(0, 1)
    plt.axhline(y=round(1.0 / (1 + opps), 3), color="gray", linestyle="--", alpha=0.7)
    plt.yticks(
        [0, 0.5, 1, round(1.0 / (1 + opps), 3)],
        ["0%", "50%", "100%", f"{round(1.0 / (1 + opps) * 100, 1)}%"],
    )
    plt.legend(handlelength=0.5)
    plt.show()