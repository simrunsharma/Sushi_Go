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

    """This class assigns values to the different cards and has methods to sum the scores of special cards"""

    def __init__(self, card_type: str):
        """Initialize."""
        self.card_type = card_type

    def __str__(self) -> str:
        """Generate a string view of this object."""
        return self.card_type

    def score(self):
        """Assigns base scores to the cards."""
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
        """Calculate the score for Dumpling based on the number of cards played."""
        if self.card_type == DUMPLING:
            if count == 1:
                return 1
            elif count == 2:
                return 3
            elif count == 3:
                return 6
            elif count == 4:
                return 10
            elif count >= 5:
                return 15
        
        return 0


class Deck:
    """A deck of Sushi Go cards."""

    def __init__(self):
        """Initialize."""
        self.cards = self._create_deck()

    def _create_deck(self):
        """Creates a deck of cards with the appropriate distribution for Sushi Go."""
        cards = []
        cards += [Card(MAKI_ROLLS[0]) for _ in range(6)]
        cards += [Card(MAKI_ROLLS[1]) for _ in range(12)]
        cards += [Card(MAKI_ROLLS[2]) for _ in range(8)]
        cards += [Card(TEMPURA) for _ in range(14)]
        cards += [Card(SASHIMI) for _ in range(14)]
        cards += [Card(DUMPLING) for _ in range(14)]
        cards += [Card(NIGIRI_SQUID) for _ in range(10)]
        cards += [Card(NIGIRI_SALMON) for _ in range(5)]
        cards += [Card(NIGIRI_EGG) for _ in range(5)]
        cards += [Card(WASABI) for _ in range(6)]
        shuffle(cards)
        return cards


class Player:
    """Represents a player in the Sushi Go game."""

    """contains methods for the player to get his hands, calculate final score for the player."""

    def __init__(self, name):
        self.name = name
        self.hand = []

    def assign_cards(self, deck, num_cards):
        """Assigns cards to the player from the deck."""
        if num_cards > len(deck.cards):
            print("Error: Not enough cards in the deck for the player to draw.")
            return False
        if num_cards == 0:
            print("Error: Number of cards in hand cannot be 0.")
            return False
        self.hand = deck.cards[:num_cards]
        deck.cards = deck.cards[num_cards:]
        return True

    def show_hand(self):
        print(f"{self.name}'s hand:")
        for card in self.hand:
            print(card)

    def calculate_final_score(self, table, best_card):
        """Calculates the final score of the player's table"""
        table_cards = table.cards_on_table
        maki_score = 0
        nigiri_score = 0
        tempura_pairs = 0
        sashimi_count = 0
        dumpling_count = 0

        has_wasabi = False
        highest_nigiri_score = 0

        for card in table_cards + [best_card]:
            if (
                card.card_type == "Maki 1"
                or card.card_type == "Maki 2"
                or card.card_type == "Maki 3"
            ):
                maki_score += card.score()
            elif (
                card.card_type == NIGIRI_SQUID
                or card.card_type == NIGIRI_SALMON
                or card.card_type == NIGIRI_EGG
            ):
                nigiri_score += card.score()
                if card.score() > highest_nigiri_score:
                    highest_nigiri_score = card.score()
            elif card.card_type == WASABI:
                has_wasabi = True
            elif card.card_type == TEMPURA:
                tempura_pairs += 1
            elif card.card_type == SASHIMI:
                sashimi_count += 1
            elif card.card_type == DUMPLING:
                dumpling_count += 1

        
        if has_wasabi:
            nigiri_score += highest_nigiri_score * 3

        # Calculate score for tempura pairs
        tempura_score = (tempura_pairs // 2) * 5

        # Calculate score for sashimi sets
        sashimi_score = (sashimi_count // 3) * 10

        # Calculate score for dumplings
        dumpling_score = Card(DUMPLING).dumpling_score(dumpling_count)

        total_score = (
            maki_score + nigiri_score + tempura_score + sashimi_score + dumpling_score
        )
        return total_score


class RandomTable:
    """Cards randomly drawn on the table for the player to interact with."""

    def __init__(self):
        self.cards_on_table = []

    def draw_cards(self, deck, cards_for_t):
        """Draws N number of cards."""
        if len(deck.cards) == 0:
            print("Error: The deck is empty.")
            return False  
        if len(deck.cards) < cards_for_t:
            print("Error: Not enough cards in the deck to draw for the table.")
            return False 
        self.cards_on_table = deck.cards[:cards_for_t]
        deck.cards = deck.cards[cards_for_t:]
        return True


    def show_table(self):
        """Prints the cards on the table."""
        for card in self.cards_on_table:
            print(card)

    def show_final_table(self, best_card):
        """Prints the cards on the table along with the best card."""
        final_table = self.cards_on_table.copy()
        final_table.append(best_card)
        for card in final_table:
            print(card)


class SushiGoMaximizer:
    """Naive Maximizer strategy."""

    """This module defines the best card to by played from the hand based on the card that 
    would bring the highest score. It considers the value of the cards in hand in relation to the cards in table."""

    def __init__(self, player, table):
        self.player = player
        self.table = table

    def calculate_possible_scores(self):
        """Calculate the possible scores for each card in the player's hand in relation to the table cards."""
        possible_scores = {}
        for card in self.player.hand:
            if card.card_type in MAKI_ROLLS:
                possible_scores[card] = [card.score()]
            elif card.card_type in [NIGIRI_SQUID, NIGIRI_SALMON, NIGIRI_EGG]:
                if any(
                    table_card.card_type == WASABI
                    for table_card in self.table.cards_on_table
                ):
                    possible_scores[card] = [card.score() * 3]
                else:
                    possible_scores[card] = [card.score()]
            elif card.card_type == WASABI:
                possible_scores[card] = [0]
                for table_card in self.table.cards_on_table:
                    if table_card.card_type in [
                        NIGIRI_SQUID,
                        NIGIRI_SALMON,
                        NIGIRI_EGG,
                    ]:
                        possible_scores[card].append(table_card.score() * 3)
            elif card.card_type == TEMPURA:
                if any(
                    table_card.card_type == TEMPURA
                    for table_card in self.table.cards_on_table
                ):
                    possible_scores[card] = [5]
                else:
                    possible_scores[card] = [0]
            elif card.card_type == SASHIMI:
                if (
                    len(
                        [
                            table_card
                            for table_card in self.table.cards_on_table
                            if table_card.card_type == SASHIMI
                        ]
                    )
                    >= 2
                ):
                    possible_scores[card] = [10]
                else:
                    possible_scores[card] = [0]
            elif card.card_type == DUMPLING:
                count_dumplings_on_table = sum(
                    1
                    for table_card in self.table.cards_on_table
                    if table_card.card_type == DUMPLING
                )
                possible_scores[card] = [card.dumpling_score(count_dumplings_on_table)]
        return possible_scores

    def select_best_card(self):
        """Select the card with the highest possible score from the possible scores in hand."""
        possible_scores = self.calculate_possible_scores()
        max_score = float("-inf")
        best_card = None
        for card, scores in possible_scores.items():
            if max(scores, default=0) > max_score:
                max_score = max(scores)
                best_card = card
        return best_card

if __name__ == "__main__":
    deck = Deck()
    player = Player("Player 1")
    if not player.assign_cards(deck, 3): 
        print("Execution stopped due to error in assigning cards.")
    else:
        player.show_hand()
        table = RandomTable()
        num_cards_table = 4
        table.draw_cards(deck, num_cards_table)
        if num_cards_table == 0:  
            print("Beginning of the game.")  
        else:
            print("Table cards:")
            table.show_table()

        maximizer = SushiGoMaximizer(player, table)  
        best_card = maximizer.select_best_card()  

        if best_card:
            print(f"{player.name} plays: {best_card}")
            final_score = player.calculate_final_score(table, best_card)
            print(f"Final score for {player.name}: {final_score}")
            print("Final table:")
            table.show_final_table(best_card)
        else:
            print("No card to play.")



