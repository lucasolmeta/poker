"""Unit tests for Evaluator: score_hand, each hand category, and bit-packed scores."""

import pytest

from src.board import Board
from src.card import Card
from src.evaluator import Evaluator
from src.player import Player


def C(rank: int, suit: int) -> Card:
    """Short constructor for test readability."""
    return Card(rank, suit)


def board_flop_turn_river(cards: list[Card]) -> Board:
    """Build a Board with all five community cards set."""
    if len(cards) != 5:
        raise ValueError("Need exactly 5 board cards")
    b = Board(cards[:3])
    b.set_turn(cards[3])
    b.set_river(cards[4])
    return b


@pytest.fixture
def ev() -> Evaluator:
    return Evaluator()


# --- Bit-level expected scores (match Evaluator shifting) ---


def test_straight_flush_royal_returns_nine_at_top_bits(ev: Evaluator):
    """Royal straight flush uses 9 << 40 (distinct from other SF scores)."""
    # A K Q J T all spades (3)
    cards = [
        C(14, 3),
        C(13, 3),
        C(12, 3),
        C(11, 3),
        C(10, 3),
        C(2, 0),
        C(3, 0),
    ]
    assert ev.straight_flush(cards) == 9 << 40


def test_straight_flush_non_royal_high_card_in_bits(ev: Evaluator):
    """Non-royal SF: (8 << 40) + (high_straight_rank << 32)."""
    # 9-high SF: 9-8-7-6-5 clubs (0)
    cards = [
        C(9, 0),
        C(8, 0),
        C(7, 0),
        C(6, 0),
        C(5, 0),
        C(14, 1),
        C(2, 2),
    ]
    assert ev.straight_flush(cards) == (8 << 40) + (9 << 32)


def test_straight_flush_wheel_uses_five_high(ev: Evaluator):
    """Wheel SF: A-2-3-4-5 same suit scores as 5-high straight flush."""
    cards = [
        C(14, 2),
        C(5, 2),
        C(4, 2),
        C(3, 2),
        C(2, 2),
        C(9, 0),
        C(10, 0),
    ]
    assert ev.straight_flush(cards) == (8 << 40) + (5 << 32)


def test_straight_flush_picks_highest_when_extra_suited_cards(ev: Evaluator):
    """Extra suited connector should still yield top straight flush only."""
    # Spades: T,9,8,7,6,5 — best SF is T-high
    cards = [
        C(10, 3),
        C(9, 3),
        C(8, 3),
        C(7, 3),
        C(6, 3),
        C(5, 3),
        C(2, 0),
    ]
    assert ev.straight_flush(cards) == (8 << 40) + (10 << 32)


def test_four_of_kind_rank_and_kicker_bits(ev: Evaluator):
    """Four of a kind: (7 << 40) + (quad_rank << 32) + (kicker << 24)."""
    cards = [
        C(8, 0),
        C(8, 1),
        C(8, 2),
        C(8, 3),
        C(14, 0),
        C(7, 1),
        C(2, 2),
    ]
    expected = (7 << 40) + (8 << 32) + (14 << 24)
    assert ev.four_of_kind(cards) == expected


def test_four_of_kind_kicker_not_from_quads(ev: Evaluator):
    """Kicker must be highest rank not part of the four."""
    cards = [
        C(5, 0),
        C(5, 1),
        C(5, 2),
        C(5, 3),
        C(11, 0),
        C(9, 1),
        C(3, 2),
    ]
    assert ev.four_of_kind(cards) == (7 << 40) + (5 << 32) + (11 << 24)


def test_full_house_trips_and_pair_bits(ev: Evaluator):
    """Full house: (6 << 40) + (triple << 32) + (pair << 24)."""
    cards = [
        C(14, 0),
        C(14, 1),
        C(14, 2),
        C(13, 0),
        C(13, 1),
        C(2, 2),
        C(3, 3),
    ]
    assert ev.full_house(cards) == (6 << 40) + (14 << 32) + (13 << 24)


def test_full_house_double_trips_uses_higher_trips(ev: Evaluator):
    """K K K J J J: best full house is kings full of jacks."""
    cards = [
        C(13, 0),
        C(13, 1),
        C(13, 2),
        C(12, 0),
        C(12, 1),
        C(12, 2),
        C(2, 3),
    ]
    assert ev.full_house(cards) == (6 << 40) + (13 << 32) + (12 << 24)


def test_flush_top_five_ranks_packed_in_bytes(ev: Evaluator):
    """Flush: (5 << 40) + sum(rank << 8*(4-i)) for top five suited ranks."""
    # Hearts: A K Q J 9 plus two offsuit low cards
    cards = [
        C(14, 2),
        C(13, 2),
        C(12, 2),
        C(11, 2),
        C(9, 2),
        C(14, 0),
        C(13, 0),
    ]
    suited = [14, 13, 12, 11, 9]
    expected = 5 << 40
    for i, rank in enumerate(suited):
        expected += rank << (8 * (4 - i))
    assert ev.flush(cards) == expected


def test_flush_ignores_lower_suited_rank_when_sixth_suited_card(ev: Evaluator):
    """Six diamonds: score uses five highest diamond ranks."""
    cards = [
        C(10, 1),
        C(9, 1),
        C(8, 1),
        C(7, 1),
        C(6, 1),
        C(5, 1),
        C(2, 0),
    ]
    suited = [10, 9, 8, 7, 6]
    expected = 5 << 40
    for i, rank in enumerate(suited):
        expected += rank << (8 * (4 - i))
    assert ev.flush(cards) == expected


def test_straight_broadway_bits(ev: Evaluator):
    """Broadway straight: (4 << 40) + (14 << 32)."""
    cards = [
        C(14, 0),
        C(13, 1),
        C(12, 2),
        C(11, 3),
        C(10, 0),
        C(2, 1),
        C(3, 2),
    ]
    assert ev.straight(cards) == (4 << 40) + (14 << 32)


def test_straight_wheel_five_high(ev: Evaluator):
    """Wheel uses ace as low; high card for scoring is 5."""
    cards = [
        C(14, 0),
        C(5, 1),
        C(4, 2),
        C(3, 3),
        C(2, 0),
        C(9, 1),
        C(10, 2),
    ]
    assert ev.straight(cards) == (4 << 40) + (5 << 32)


def test_straight_six_high_beats_wheel(ev: Evaluator):
    """6-high straight score is greater than wheel straight score."""
    wheel = [C(14, 0), C(5, 1), C(4, 2), C(3, 3), C(2, 0), C(9, 1), C(10, 2)]
    six_high = [C(6, 0), C(5, 1), C(4, 2), C(3, 3), C(2, 0), C(14, 1), C(9, 2)]
    assert ev.straight(six_high) > ev.straight(wheel)


def test_three_of_kind_trips_and_two_kicker_ranks(ev: Evaluator):
    """Three of a kind: (3<<40) + trip<<32 + k1<<24 + k2<<16 from top two other ranks."""
    cards = [
        C(7, 0),
        C(7, 1),
        C(7, 2),
        C(14, 0),
        C(13, 1),
        C(5, 2),
        C(4, 3),
    ]
    assert ev.three_of_kind(cards) == (3 << 40) + (7 << 32) + (14 << 24) + (13 << 16)


def test_two_pair_high_low_and_kicker(ev: Evaluator):
    """Two pair: (2<<40) + high<<32 + low<<24 + kicker<<16."""
    cards = [
        C(14, 0),
        C(14, 1),
        C(13, 0),
        C(13, 1),
        C(12, 2),
        C(5, 2),
        C(3, 3),
    ]
    assert ev.two_pair(cards) == (2 << 40) + (14 << 32) + (13 << 24) + (12 << 16)


def test_two_pair_kicker_tiebreak(ev: Evaluator):
    """Same two pair; kicker rank decides the score."""
    low_kicker = [
        C(14, 0),
        C(14, 1),
        C(13, 0),
        C(13, 1),
        C(9, 2),
        C(5, 2),
        C(3, 3),
    ]
    high_kicker = [
        C(14, 0),
        C(14, 1),
        C(13, 0),
        C(13, 1),
        C(12, 2),
        C(5, 2),
        C(3, 3),
    ]
    assert ev.two_pair(high_kicker) > ev.two_pair(low_kicker)


def test_pair_and_three_kickers_by_byte(ev: Evaluator):
    """Pair: (1<<40) + pair<<32 + three kicker ranks at <<24, <<16, <<8."""
    cards = [
        C(14, 0),
        C(14, 1),
        C(13, 2),
        C(12, 3),
        C(11, 0),
        C(5, 1),
        C(3, 2),
    ]
    expected = (1 << 40) + (14 << 32) + (13 << 24) + (12 << 16) + (11 << 8)
    assert ev.pair(cards) == expected


def test_pair_kicker_ordering(ev: Evaluator):
    """Better side cards produce strictly larger pair scores."""
    worse = [
        C(10, 0),
        C(10, 1),
        C(9, 2),
        C(8, 3),
        C(4, 0),
        C(3, 1),
        C(2, 2),
    ]
    better = [
        C(10, 0),
        C(10, 1),
        C(9, 2),
        C(8, 3),
        C(7, 0),
        C(3, 1),
        C(2, 2),
    ]
    assert ev.pair(better) > ev.pair(worse)


def test_high_card_five_ranks_shifted(ev: Evaluator):
    """high_card packs first five cards (caller must pass score_hand order)."""
    cards_sorted = [
        C(14, 3),
        C(13, 2),
        C(12, 1),
        C(11, 0),
        C(9, 3),
        C(5, 0),
        C(4, 0),
    ]
    expected = (14 << 32) + (13 << 24) + (12 << 16) + (11 << 8) + 9
    assert ev.high_card(cards_sorted) == expected


def test_category_prefixes_order_strength(ev: Evaluator):
    """Sanity: monotonic ordering of category bits for representative hands."""
    royal_sf = [
        C(14, 3),
        C(13, 3),
        C(12, 3),
        C(11, 3),
        C(10, 3),
        C(2, 0),
        C(3, 0),
    ]
    quads = [
        C(8, 0),
        C(8, 1),
        C(8, 2),
        C(8, 3),
        C(14, 0),
        C(7, 1),
        C(2, 2),
    ]
    boat = [
        C(14, 0),
        C(14, 1),
        C(14, 2),
        C(13, 0),
        C(13, 1),
        C(2, 2),
        C(3, 3),
    ]
    flush_cards = [
        C(14, 2),
        C(13, 2),
        C(12, 2),
        C(11, 2),
        C(9, 2),
        C(14, 0),
        C(13, 0),
    ]
    straight_cards = [
        C(14, 0),
        C(13, 1),
        C(12, 2),
        C(11, 3),
        C(10, 0),
        C(2, 1),
        C(3, 2),
    ]
    trips = [
        C(7, 0),
        C(7, 1),
        C(7, 2),
        C(14, 0),
        C(13, 1),
        C(5, 2),
        C(4, 3),
    ]
    two = [
        C(14, 0),
        C(14, 1),
        C(13, 0),
        C(13, 1),
        C(12, 2),
        C(5, 2),
        C(3, 3),
    ]
    one = [
        C(14, 0),
        C(14, 1),
        C(13, 2),
        C(12, 3),
        C(11, 0),
        C(5, 1),
        C(3, 2),
    ]
    high = [
        C(14, 3),
        C(13, 2),
        C(12, 1),
        C(11, 0),
        C(9, 3),
        C(5, 0),
        C(4, 0),
    ]

    scores = [
        ev.straight_flush(royal_sf),
        ev.four_of_kind(quads),
        ev.full_house(boat),
        ev.flush(flush_cards),
        ev.straight(straight_cards),
        ev.three_of_kind(trips),
        ev.two_pair(two),
        ev.pair(one),
        ev.high_card(high),
    ]
    assert scores == sorted(scores, reverse=True)


# --- score_hand integration (Player + full Board) ---


def test_score_hand_straight_flush_wheel(ev: Evaluator):
    player = Player([C(14, 2), C(5, 2)])
    board = board_flop_turn_river(
        [C(4, 2), C(3, 2), C(2, 2), C(9, 0), C(10, 0)]
    )
    assert ev.score_hand(player, board) == (8 << 40) + (5 << 32)


def test_score_hand_royal_straight_flush(ev: Evaluator):
    player = Player([C(14, 3), C(13, 3)])
    board = board_flop_turn_river(
        [C(12, 3), C(11, 3), C(10, 3), C(2, 0), C(3, 0)]
    )
    assert ev.score_hand(player, board) == 9 << 40


def test_score_hand_four_of_kind_over_full_house(ev: Evaluator):
    """Quads on board + pocket pair completes quads vs full house possibility."""
    player = Player([C(8, 0), C(8, 1)])
    board = board_flop_turn_river(
        [C(8, 2), C(8, 3), C(13, 0), C(13, 1), C(13, 2)]
    )
    assert ev.score_hand(player, board) == (7 << 40) + (8 << 32) + (13 << 24)


def test_score_hand_flush_beats_straight_when_both_present(ev: Evaluator):
    player = Player([C(14, 1), C(13, 1)])
    board = board_flop_turn_river(
        [C(12, 1), C(11, 1), C(6, 1), C(10, 0), C(9, 0)]
    )
    # Flush in diamonds; board also completes broadway straight in mixed suits
    assert ev.score_hand(player, board) == ev.flush(
        player.cards() + board.cards()
    )


def test_score_hand_straight_beats_three_of_kind(ev: Evaluator):
    player = Player([C(10, 0), C(9, 0)])
    board = board_flop_turn_river(
        [C(8, 1), C(7, 2), C(6, 3), C(14, 0), C(2, 1)]
    )
    assert ev.score_hand(player, board) == (4 << 40) + (10 << 32)


def test_score_hand_pair_kicker_ev(ev: Evaluator):
    """Same pair rank; better kickers should yield higher score_hand."""
    better = Player([C(14, 0), C(14, 1)])
    board_better = board_flop_turn_river(
        [C(13, 2), C(12, 2), C(11, 2), C(5, 3), C(3, 3)]
    )
    worse = Player([C(14, 2), C(14, 3)])
    board_worse = board_flop_turn_river(
        [C(13, 0), C(12, 0), C(9, 0), C(5, 1), C(3, 1)]
    )
    assert ev.score_hand(better, board_better) > ev.score_hand(worse, board_worse)


def test_score_hand_wheel_straight_not_misread_as_broadway_missing(ev: Evaluator):
    """Explicit wheel on board + suited junk that does not make SF."""
    player = Player([C(14, 0), C(2, 1)])
    board = board_flop_turn_river(
        [C(5, 2), C(4, 2), C(3, 2), C(9, 3), C(10, 3)]
    )
    assert ev.score_hand(player, board) == (4 << 40) + (5 << 32)


def test_straight_flush_returns_zero_when_flush_but_no_straight(ev: Evaluator):
    """Five suited cards without a straight should not score as straight flush."""
    cards = [
        C(14, 0),
        C(12, 0),
        C(10, 0),
        C(8, 0),
        C(6, 0),
        C(2, 1),
        C(3, 1),
    ]
    assert ev.straight_flush(cards) == 0


def test_four_of_kind_returns_zero_when_only_trips(ev: Evaluator):
    cards = [
        C(9, 0),
        C(9, 1),
        C(9, 2),
        C(14, 0),
        C(13, 1),
        C(5, 2),
        C(4, 3),
    ]
    assert ev.four_of_kind(cards) == 0


def test_full_house_returns_zero_when_only_trips_and_no_pair(ev: Evaluator):
    cards = [
        C(8, 0),
        C(8, 1),
        C(8, 2),
        C(14, 0),
        C(13, 1),
        C(12, 2),
        C(11, 3),
    ]
    assert ev.full_house(cards) == 0


def test_flush_returns_zero_when_best_suit_only_four(ev: Evaluator):
    cards = [
        C(14, 2),
        C(13, 2),
        C(12, 2),
        C(11, 2),
        C(10, 0),
        C(9, 0),
        C(8, 0),
    ]
    assert ev.flush(cards) == 0


def test_straight_returns_zero_when_gap(ev: Evaluator):
    cards = [
        C(14, 0),
        C(13, 1),
        C(12, 2),
        C(10, 3),
        C(9, 0),
        C(2, 1),
        C(3, 2),
    ]
    assert ev.straight(cards) == 0


def test_two_pair_returns_zero_when_only_one_pair(ev: Evaluator):
    cards = [
        C(14, 0),
        C(14, 1),
        C(13, 0),
        C(12, 1),
        C(11, 2),
        C(5, 2),
        C(3, 3),
    ]
    assert ev.two_pair(cards) == 0


def test_pair_returns_zero_when_no_pair(ev: Evaluator):
    cards = [
        C(14, 0),
        C(13, 1),
        C(12, 2),
        C(11, 3),
        C(9, 0),
        C(7, 1),
        C(5, 2),
    ]
    assert ev.pair(cards) == 0