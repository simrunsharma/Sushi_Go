
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from single_player_automated import *

def test_card_scoring():
    # Check scoring for each card type
    assert Card(TEMPURA).score() == 5, "Tempura score should be 5"
    assert Card(SASHIMI).score() == 10, "Sashimi score should be 10"
    assert Card(DUMPLING).score() == 1, "Dumpling score should be 1"
    assert Card(NIGIRI_SQUID).score() == 3, "Squid Nigiri score should be 3"
    assert Card(NIGIRI_SALMON).score() == 2, "Salmon Nigiri score should be 2"
    assert Card(NIGIRI_EGG).score() == 1, "Egg Nigiri score should be 1"
    assert Card(WASABI).score() == 0, "Wasabi score should be 0"
    # Testing Maki rolls which depend on their position in the list
    assert Card("Maki 1").score() == 1, "Maki 1 score should be 1"
    assert Card("Maki 2").score() == 2, "Maki 2 score should be 2"
    assert Card("Maki 3").score() == 3, "Maki 3 score should be 3"
    print("Test Card Scoring passed.")

def test_dumpling_scoring():
    # Dumpling scores based on quantity
    dumpling_card = Card(DUMPLING)
    assert dumpling_card.dumpling_score(1) == 1, "1 Dumpling should score 1"
    assert dumpling_card.dumpling_score(2) == 3, "2 Dumplings should score 3"
    assert dumpling_card.dumpling_score(3) == 6, "3 Dumplings should score 6"
    assert dumpling_card.dumpling_score(4) == 10, "4 Dumplings should score 10"
    assert dumpling_card.dumpling_score(5) == 15, "5 or more Dumplings should score 15"
    print("Test Dumpling Scoring passed.")

def test_player_card_assignment():
    deck = Deck()  # Assume a full deck
    player = Player("Tester")
    # Test assigning zero cards
    player.assign_cards(deck, 0)
    assert len(player.hand) == 0, "No cards should be assigned"
    # Test assigning more cards than available
    player.assign_cards(deck, 100)  # Assuming the deck has fewer than 100 cards
    assert len(player.hand) == 0, "Not enough cards in deck should prevent assignment"
    print("Test Player Card Assignment passed.")

def test_game_flow():
    deck = Deck()
    player = Player("Tester")
    player.assign_cards(deck, 5)  # A normal number of cards
    assert len(player.hand) == 5, "Player should have 5 cards"
    table = RandomTable()
    table.draw_cards(deck, 3)
    assert len(table.cards_on_table) == 3, "Table should have 3 cards"
    print("Test Game Flow passed.")


def test_invalid_card_type():
    try:
        invalid_card = Card("Invalid Type")
        invalid_card.score()
        assert False, "Should have raised an error for an invalid card type"
    except ValueError:
        print("Correctly handled invalid card type.")
    except Exception as e:
        assert False, f"Unexpected error type for invalid card: {str(e)}"

def test_sushi_go_maximizer():
    # Create a deck but don't shuffle for predictability in tests
    deck = Deck()
    deck.cards = [Card(NIGIRI_SQUID), Card(WASABI), Card(NIGIRI_SALMON), Card(TEMPURA), Card(SASHIMI)]

    # Create a player and assign specific cards
    player = Player("Test Player")
    player.hand = [deck.cards[0], deck.cards[1], deck.cards[2]]  # Squid Nigiri, Wasabi, Salmon Nigiri

    # Setup table with specific cards that interact with player's hand
    table = RandomTable()
    table.cards_on_table = [deck.cards[3], deck.cards[4]]  # Tempura, Sashimi

    # Initialize the maximizer
    maximizer = SushiGoMaximizer(player, table)

    # Execute the best card selection
    best_card = maximizer.select_best_card()

    # Determine if the selected card is the expected one
    expected_best_card = player.hand[0]  
    assert best_card == expected_best_card, f"Expected {expected_best_card.card_type}, but got {best_card.card_type}"
    print("Test passed: Correct best card selected.")


def test_zero_cards_on_table():
    deck = Deck()  # Assume the deck is properly initialized and shuffled
    player = Player("Test Player")
    table = RandomTable()

    # Make sure there are enough cards for the player
    assert player.assign_cards(deck, 3), "Failed to assign cards to player when there should be enough cards."

    # Test drawing 0 cards for the table
    table.draw_cards(deck, 0)  # This should simulate the beginning of the game
    assert len(table.cards_on_table) == 0, "Test failed: There should be 0 cards on the table."

    print("Test passed: Drawing 0 cards for the table handled correctly.")

def test_zero_cards_in_hand():
    deck = Deck()  # Assume the deck is initialized and shuffled
    player = Player("Test Player")
    table = RandomTable()

    # Try assigning 0 cards to player, which should fail
    assert not player.assign_cards(deck, 0), "Test failed: Assigning 0 cards should not be allowed."

    print("Test passed: Assigning 0 cards in hand handled correctly.")
    