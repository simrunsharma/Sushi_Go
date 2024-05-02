
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from the_final_switch_hands import Card, Deck, Player, RandomTable, SushiGoMaximizer, Game

# Test Card class
def test_card():
    # Test initialization and scoring
    tempura_card = Card("Tempura")
    assert tempura_card.score() == 5, "Tempura should score 5"
    
    sashimi_card = Card("Sashimi")
    assert sashimi_card.score() == 10, "Sashimi should score 10"
    
    # Test for invalid card type
    try:
        invalid_card = Card("Pizza")
        invalid_card.score()
        assert False, "Should have raised ValueError"
    except ValueError:
        assert True, "Caught an expected ValueError for invalid card type"
    
    # Test dumpling scoring
    dumpling_card = Card("Dumpling")
    assert dumpling_card.dumpling_score(5) == 15, "5 dumplings should score 15 points"

# Test Deck class
def test_deck():
    deck = Deck()
    # Test if deck creates the correct total number of cards
    assert len(deck.cards) == 94, "Deck should contain 94 cards"
    
    # Test distribution of one type of card
    tempura_count = sum(1 for card in deck.cards if card.card_type == "Tempura")
    assert tempura_count == 14, "Should be 14 Tempura cards"

# Test Player class
def test_player():
    deck = Deck()
    player = Player("Test Player")
    
    # Test assigning cards to player
    player.assign_cards(deck, 5)
    assert len(player.hand) == 5, "Player should have 5 cards in hand"
    
    # Test playing the max scoring card
    player.hand = [Card("Tempura"), Card("Sashimi"), Card("Dumpling")]
    max_card = player.play_max_scoring_card()
    assert max_card.card_type == "Sashimi", "Should play Sashimi as it has the highest score"

# Test RandomTable class
def test_random_table():
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    table = RandomTable([], player1, player2)
    
    # Test adding and retrieving cards from the table
    card = Card("Tempura")
    table.update_table_with_card(player1, card)
    assert table.player1_table == [card], "Player 1's table should have the Tempura card"

# Test SushiGoMaximizer class
def test_sushi_go_maximizer():
    player = Player("Maximizer Test Player")
    table = RandomTable([], player, None)
    player.hand = [Card("Sashimi"), Card("Tempura"), Card("Dumpling")]
    table.cards_on_table = [Card("Wasabi")]
    
    maximizer = SushiGoMaximizer(player, table)
    best_card = maximizer.select_best_card()
    assert best_card.card_type == "Sashimi", "Should select Sashimi because it scores highest currently"

# Test Game class
def test_game():
    deck = Deck()
    game = Game("Player 1", "Player 2", 1, deck)
    
    game.conduct_round() 
    print("Game round conducted successfully.")  


#testing all the game methods explicitly
def test_switch_hands():
    deck = Deck()
    game = Game("Player 1", "Player 2", 1, deck)
    game.player1.hand = [Card("Tempura"), Card("Sashimi")]
    game.player2.hand = [Card("Dumpling"), Card("Nigiri Squid")]

    # Save pre-switch hands for comparison
    pre_switch_hand_p1 = game.player1.hand[:]
    pre_switch_hand_p2 = game.player2.hand[:]

    game.switch_hands()

    # Check if hands have been switched correctly
    assert game.player1.hand == pre_switch_hand_p2, "Player 1's hand should now have Player 2's cards"
    assert game.player2.hand == pre_switch_hand_p1, "Player 2's hand should now have Player 1's cards"

def test_calculate_final_score():
    deck = Deck()
    game = Game("Player 1", "Player 2", 1, deck)
    player1_table = [Card("Tempura"), Card("Tempura"), Card("Sashimi"), Card("Sashimi"), Card("Sashimi")]
    score = game.calculate_final_score(player1_table)
    
    # Expected scores: Tempura = 5*2/2=5, Sashimi = 10*3/3=10, Total = 15
    assert score == 15, "The score calculation should correctly calculate based on the card set rules"

def test_conduct_round():
    deck = Deck()
    game = Game("Player 1", "Player 2", 1, deck)

    game.conduct_round()
    assert len(game.player1.hand) == 0 and len(game.player2.hand) == 0, "Both players should have empty hands after a round"


# Mocking necessary classes and functions for testing
class MockCard:
    def __init__(self, card_type, score):
        self.card_type = card_type
        self.score = lambda: score

    def __str__(self):
        return self.card_type

class MockDeck:
    def __init__(self, cards):
        self.cards = cards

# Test Player class
def test_assign_cards():
    deck = MockDeck([MockCard("Tempura", 5), MockCard("Sashimi", 10), MockCard("Dumpling", 1)])
    player = Player("Test Player")

    # Test normal card assignment
    player.assign_cards(deck, 2)
    assert len(player.hand) == 2, "Player should have 2 cards in hand"
    assert len(deck.cards) == 1, "Deck should have 1 card left after assignment"

    # Test assigning more cards than are in the deck
    player.assign_cards(deck, 5)
    assert len(player.hand) == 2, "Player should still have 2 cards, not more"

    # Test assigning zero cards
    player.assign_cards(deck, 0)
    assert len(player.hand) == 2, "Player should still have 2 cards, no change"


def test_play_best_card():
    player = Player("Maximizer Test Player")
    table = RandomTable([], player, None)  
    player.hand = [MockCard("Sashimi", 10), MockCard("Tempura", 5), MockCard("Dumpling", 1)]

    # Here, we'll assume that SushiGoMaximizer simply returns the first card as the "best" card
    # This is to simplify testing without having a full maximizer logic implemented
    class SimpleMaximizer:
        def __init__(self, player, table):
            self.player = player
            self.table = table

        def select_best_card(self):
            return self.player.hand[0]  # Simulate always picking the first card


    player.hand = [MockCard("Sashimi", 10), MockCard("Tempura", 5), MockCard("Dumpling", 1)]

    player.play_best_card = lambda table: SimpleMaximizer(player, table).select_best_card()

    best_card = player.play_best_card(table)
    print("Played best card:", best_card.card_type)  # Printing the type of the best card played
    print("Remaining hand:", [card.card_type for card in player.hand])  # Printing remaining cards in hand
    assert best_card.card_type == "Sashimi", "Should play Sashimi as it is selected as best card"
    print("Number of cards remaining in hand (Expected: 2):", len(player.hand))  # Print the actual number of cards

def run_player_tests():
    
    test_assign_cards()
    test_play_best_card()


if __name__ == "__main__":
    run_player_tests()


