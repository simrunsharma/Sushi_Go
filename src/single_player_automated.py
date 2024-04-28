
"""Version 0. This module presents a simulation of a naive maximizer decision for a sushi go game."""

from random import shuffle

# CARDS
TEMPURA = "Tempura"
SASHIMI = "Sashimi"
DUMPLING = "Dumpling"
NIGIRI_SQUID = "Squid Nigiri"
NIGIRI_SALMON = "Salmon Nigiri"
NIGIRI_EGG = "Egg Nigiri"
WASABI = "Wasabi"
MAKI_ROLLS = ["Maki 1", "Maki 2", "Maki 3"]

class Card:
    """Playing cards for Sushi Go."""
    def __init__(self, card_type: str):
        self.card_type = card_type

    def __str__(self):
        return self.card_type

    def __eq__(self, other):
        return self.card_type == other.card_type if isinstance(other, Card) else False

    def __hash__(self):
        return hash(self.card_type)

    def score(self):
        if self.card_type in MAKI_ROLLS:
            return MAKI_ROLLS.index(self.card_type) + 1
        elif self.card_type == TEMPURA:
            return 5
        elif self.card_type == SASHIMI:
            return 10
        elif self.card_type == DUMPLING:
            return 1
        elif self.card_type == NIGIRI_SQUID:
            return 3
        elif self.card_type == NIGIRI_SALMON:
            return 2
        elif self.card_type == NIGIRI_EGG:
            return 1
        elif self.card_type == WASABI:
            return 0
        else:
            raise ValueError(f"Invalid card type: {self.card_type}")

    def dumpling_score(self, count):
        if self.card_type == DUMPLING:
            return [1, 3, 6, 10, 15][min(count, 5) - 1]
        return 0

    
class Deck:
    """A deck of Sushi Go cards."""
    def __init__(self):
        self.cards = self._create_deck()

    def _create_deck(self):
        """Creates a deck of cards with the appropriate distribution for Sushi Go."""
        cards = []
        # Correctly multiply each Maki Roll card by its count
        cards.extend([Card(mr) for mr in MAKI_ROLLS for _ in range([6, 12, 8][MAKI_ROLLS.index(mr)])])
        cards.extend([Card(TEMPURA) for _ in range(14)])
        cards.extend([Card(SASHIMI) for _ in range(14)])
        cards.extend([Card(DUMPLING) for _ in range(14)])
        cards.extend([Card(NIGIRI_SQUID) for _ in range(10)])
        cards.extend([Card(NIGIRI_SALMON) for _ in range(5)])
        cards.extend([Card(NIGIRI_EGG) for _ in range(5)])
        cards.extend([Card(WASABI) for _ in range(6)])
        shuffle(cards)
        return cards

class Player:
    """Represents a player in the Sushi Go game."""
    def __init__(self, name):
        self.name = name
        self.hand = []

    def assign_cards(self, deck, num_cards):
        if num_cards > len(deck.cards):
            print("Error: Not enough cards in the deck.")
            return
        if num_cards == 0:
            print("Error: Number of cards in hand cannot be 0.")
            return
        self.hand = deck.cards[:num_cards]
        deck.cards = deck.cards[num_cards:]

    def show_hand(self):
        print(f"{self.name}'s hand:")
        for card in self.hand:
            print(card)

    def calculate_final_score(self, table, best_card):
        table_cards = table.cards_on_table
        maki_score = sum(card.score() for card in table_cards if card.card_type in ["Maki 1", "Maki 2", "Maki 3"])
        nigiri_scores = [card.score() for card in table_cards if card.card_type in [NIGIRI_SQUID, NIGIRI_SALMON, NIGIRI_EGG]]
        tempura_count = sum(1 for card in table_cards if card.card_type == TEMPURA)
        sashimi_count = sum(1 for card in table_cards if card.card_type == SASHIMI)
        dumpling_count = sum(1 for card in table_cards if card.card_type == DUMPLING)
        wasabi_applied = any(card.card_type == WASABI for card in table_cards)

        # Calculate scores
        tempura_score = (tempura_count // 2) * 5
        sashimi_score = (sashimi_count // 3) * 10
        dumpling_score = Card(DUMPLING).dumpling_score(dumpling_count)
        highest_nigiri = max(nigiri_scores, default=0)
        nigiri_score = sum(nigiri_scores) + (3 * highest_nigiri if wasabi_applied else 0)

        total_score = maki_score + nigiri_score + tempura_score + sashimi_score + dumpling_score
        return total_score

class RandomTable:
    """Cards randomly drawn on the table for the player to interact with."""
    def __init__(self):
        self.cards_on_table = []

    def draw_cards(self, deck, cards_for_t):
        if len(deck.cards) < cards_for_t:
            print("Error: Not enough cards in the deck to draw.")
            return
        if cards_for_t == 0:
            print("Error: Number of cards on the table cannot be 0.")
            return
        self.cards_on_table = deck.cards[:cards_for_t]
        deck.cards = deck.cards[cards_for_t:]

    def show_table(self):
        for card in self.cards_on_table:
            print(card)

    def show_final_table(self, best_card):
        final_table = self.cards_on_table + [best_card]
        for card in final_table:
            print(card)

class SushiGoMaximizer:
    """Naive Maximizer strategy."""
    def __init__(self, player, table):
        self.player = player
        self.table = table

    def calculate_possible_scores(self):
        possible_scores = {}
        for card in self.player.hand:
            possible_scores[card] = [card.score()]
            if card.card_type in [NIGIRI_SQUID, NIGIRI_SALMON, NIGIRI_EGG]:
                if any(c.card_type == WASABI for c in self.table.cards_on_table):
                    possible_scores[card].append(card.score() * 3)
            elif card.card_type == WASABI:
                for table_card in self.table.cards_on_table:
                    if table_card.card_type in [NIGIRI_SQUID, NIGIRI_SALMON, NIGIRI_EGG]:
                        possible_scores[card].append(table_card.score() * 3)
            elif card.card_type == TEMPURA:
                possible_scores[card].append(5 if any(c.card_type == TEMPURA for c in self.table.cards_on_table) else 0)
            elif card.card_type == SASHIMI:
                possible_scores[card].append(10 if sum(1 for c in self.table.cards_on_table if c.card_type == SASHIMI) >= 2 else 0)
            elif card.card_type == DUMPLING:
                dumplings = sum(1 for c in self.table.cards_on_table if c.card_type == DUMPLING)
                possible_scores[card].append(card.dumpling_score(dumplings))
        return possible_scores

    def select_best_card(self):
        possible_scores = self.calculate_possible_scores()
        best_card = max(possible_scores, key=lambda x: max(possible_scores[x], default=0))
        return best_card

if __name__ == "__main__":

    deck = Deck()  # Correctly create a Deck object which initializes its own cards
    player = Player("Player 1")
    player.assign_cards(deck, 3)  # Ensure to pass the deck's cards list
    player.show_hand()
    table = RandomTable()
    table.draw_cards(deck, 3)
    print("Table cards:")
    table.show_table()
    maximizer = SushiGoMaximizer(player, table)
    best_card = maximizer.select_best_card()
    if best_card:
        print(f"{player.name} plays: {best_card}")
        final_score = player.calculate_final_score(table, best_card)
        print(f"Final score for {player.name}: {final_score}")
        table.show_final_table(best_card)
    else:
        print("No card to play.")
