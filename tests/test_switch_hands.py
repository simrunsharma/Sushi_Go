"""docstring to describe tests."""

import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from sushi_go_game import (
    Card,
    Deck,
    Game,
    Player,
    RandomTable,
    SushiGoMaximizer,
)


def test_card() -> None:
    """Test the Card class for initialization, scoring, and error handling."""
    tempura_card = Card("Tempura")
    assert tempura_card.score() == 5, "Tempura should score 5"

    sashimi_card = Card("Sashimi")
    assert sashimi_card.score() == 10, "Sashimi should score 10"

    try:
        invalid_card = Card("Pizza")
        invalid_card.score()
        assert False, "Should have raised ValueError"
    except ValueError:
        assert True, "Caught an expected ValueError for invalid card type"

    dumpling_card = Card("Dumpling")
    assert (
        dumpling_card.dumpling_score(5) == 15
    ), "5 dumplings should score 15 points"


def test_deck() -> None:
    """Test the Deck classto ensure it contains the correct number of cards."""
    deck = Deck()
    assert len(deck.cards) == 94, "Deck should contain 94 cards"

    tempura_count = sum(
        1 for card in deck.cards if card.card_type == "Tempura"
    )
    assert tempura_count == 14, "Should be 14 Tempura cards"


def test_player() -> None:
    """Test the Player class to ensure proper card handling."""
    deck = Deck()
    player = Player("Test Player")

    player.assign_cards(deck, 5)
    assert len(player.hand) == 5, "Player should have 5 cards in hand"

    player.hand = [Card("Tempura"), Card("Sashimi"), Card("Dumpling")]
    max_card = player.play_max_scoring_card()
    assert (
        max_card.card_type == "Sashimi"
    ), "Should play Sashimi as it has the highest score"


def test_random_table() -> None:
    """Test the RandomTable class for adding and retrieving cards correctly."""
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    table = RandomTable([], player1, player2)

    card = Card("Tempura")
    table.update_table_with_card(player1, card)
    assert table.player1_table == [
        card
    ], "Player 1's table should have the Tempura card"


def test_sushi_go_maximizer() -> None:
    """Test the SushiGoMaximizer class to ensure it selects."""
    """highest scoring card."""
    player = Player("Maximizer Test Player")
    table = RandomTable([], player, None)
    player.hand = [Card("Sashimi"), Card("Tempura"), Card("Dumpling")]
    table.cards_on_table = [Card("Wasabi")]

    maximizer = SushiGoMaximizer(player, table)
    best_card = maximizer.select_best_card()
    assert (
        best_card.card_type == "Sashimi"
    ), "Should select Sashimi because it scores highest currently"


def test_game() -> None:
    """Test the Game class to ensure proper gameplay mechanics."""
    deck = Deck()
    game = Game("Player 1", "Player 2", 1, deck)

    game.conduct_round()
    print("Game round conducted successfully.")
