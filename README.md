# Texas Hold'em Equity Engine

A high-performance poker equity calculator for Texas Hold'em. It uses Monte Carlo simulation and bitwise-style evaluation to approximate hand strength against multiple opponents.

## Key engineering features

**Bitwise hand evaluation** — Core logic in `src/evaluator.py` packs category and kickers into a single ordered integer using bit shifts. That gives `O(1)` comparisons between hands in the hot loop without hand-specific tie-break sorting.

**Monte Carlo sampling** — `hand_equity` builds one filtered deck pool (all cards not in the hero hand or known board) before the run loop. Each iteration draws every missing street and every opponent hole card with a single `random.sample` call, avoiding repeated deck construction and shuffling.

**Decoupled visualization** — The engine returns raw numbers (equity and an optional running-average series). Plotting lives in `utils/plotting.py`; `notebooks/demo.ipynb` shows a full workflow including convergence charts.

**Packaging** — The repo uses a `src/` layout and `pyproject.toml` with **matplotlib** as a runtime dependency (for plotting) and **pytest** under optional `dev` extras so library installs stay lean.

## Performance and design

The API stays modular around `Card`, `Player`, and `Board` so data flow stays obvious. Efficient sampling plus scalar hand scores keep simulation throughput high while leaving room to extend toward richer game-state or strategy code.

## Installation and usage

### Prerequisites

- Python 3.9+

### Setup

Clone the repository and install with core dependencies:

```bash
pip install .
```

For tests (and typical notebook development):

```bash
pip install ".[dev]"
```

### Quick start

A worked example (including board construction and equity convergence) is in `notebooks/demo.ipynb`.

From the **repository root** (same layout as the notebook):

```python
from src.evaluator import Evaluator
from src.card import Card

evaluator = Evaluator()
hero_hand = [Card(14, 0), Card(14, 1)]  # Ace of Clubs, Ace of Diamonds
equity, tracker = evaluator.hand_equity(hero_hand, sim_num=10000, opps=3)
print(f"Equity: {equity:.2%}")
```

## Testing

Unit tests under `tests/` exercise the evaluator across standard hand categories and kickers, including wheel straights and similar edge cases.

```bash
pytest
```
