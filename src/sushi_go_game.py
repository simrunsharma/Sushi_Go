"""This module presents a simulation of a Sushi- Go game.

The simulation runs a game of three rounds between two players.
On each round the players are given 9 cards:
- On each turn of the round, the player draws one card to the table:
    - The players draw their cards based on the card that will give
      them the most points.
    - The  best card depends on its value and the possible score in combination
      to the cards on the player's table
    - After each turn, the players switch hands with each other
- After the three rounds the points are added.
"""

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

    """This class assigns values to the different cards and has methods to sum 
    the scores of special cards"""

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
        """Calculate the score for Dumpling based on the number of cards."""
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
        """Creates a deck of cards with distribution of Sushi Go."""
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

    def __init__(self, name):
        """Initializes name and hand"""
        self.name = name
        self.hand = []

    def assign_cards(self, deck, num_cards):
        """Assings cards."""
        if num_cards > len(deck.cards):
            print("Error: Not enough cards in the deck.")
            return
        if num_cards == 0:
            print("Error: Number of cards in hand cannot be 0.")
            return
        self.hand = deck.cards[:num_cards]
        deck.cards = deck.cards[num_cards:]

    def show_hand(self):
        """Prints hand."""
        print(
            f"{self.name}'s hand: {', '.join(str(card) for card in self.hand)}"
        )
        # for card in self.hand:
        #     print(card)

    def play_max_scoring_card(self):
        "Plays the best card for the first turn."
        if not self.hand:
            print(f"{self.name} has no cards to play.")
            return None

        max_scoring_card = max(self.hand, key=lambda card: card.score())
        self.hand.remove(max_scoring_card)
        return max_scoring_card

    def play_best_card(self, table):
        """Plays best card with the maximizer strategy."""
        maximizer = SushiGoMaximizer(self, table)
        best_card = maximizer.select_best_card()
        if best_card:
            self.hand.remove(best_card)
            return best_card
        else:
            print("No card to play.")
            return None


class RandomTable:
    """Builds table for players with the cards drawn."""

    def __init__(self, cards_on_table, player1, player2):
        """Initializes."""
        self.cards_on_table = (
            cards_on_table if cards_on_table is not None else []
        )
        self.player1 = player1
        self.player2 = player2
        self.player1_table = []
        self.player2_table = []
        # self.card_type=card_type

    def show_table(self, player):
        """Prints table."""
        if player == self.player1:
            print([str(card) for card in self.player1_table])
        elif player == self.player2:
            print([str(card) for card in self.player2_table])
        else:
            raise ValueError("Invalid player")

    def update_table_with_card(self, player, card):
        """Adds a card to the player's table."""
        if player == self.player1:
            self.player1_table.append(card)
        elif player == self.player2:
            self.player2_table.append(card)
        else:
            raise ValueError("Invalid player")

        return self


class SushiGoMaximizer:
    """Naive Maximizer strategy."""

    def __init__(self, player, table):
        self.player = player
        self.table = table

    def calculate_possible_scores(self):
        """Calcualtes the possible score of each card on hand.

        It calculates the p.s. of each card on hand by matching it with each
        card on table and applying the combination rules from the game.
        """
        possible_scores = {}
        for card in self.player.hand:
            possible_scores[card] = [card.score()]
            if card.card_type in [NIGIRI_SQUID, NIGIRI_SALMON, NIGIRI_EGG]:
                if any(
                    c.card_type == WASABI for c in self.table.cards_on_table
                ):
                    possible_scores[card].append(card.score() * 3)
            elif card.card_type == WASABI:
                for table_card in self.table.cards_on_table:
                    if table_card.card_type in [
                        NIGIRI_SQUID,
                        NIGIRI_SALMON,
                        NIGIRI_EGG,
                    ]:
                        possible_scores[card].append(table_card.score() * 3)
            elif card.card_type == TEMPURA:
                possible_scores[card].append(
                    5
                    if any(
                        c.card_type == TEMPURA
                        for c in self.table.cards_on_table
                    )
                    else 0
                )
            elif card.card_type == SASHIMI:
                possible_scores[card].append(
                    10
                    if sum(
                        1
                        for c in self.table.cards_on_table
                        if c.card_type == SASHIMI
                    )
                    >= 2
                    else 0
                )
            elif card.card_type == DUMPLING:
                dumplings = sum(
                    1
                    for c in self.table.cards_on_table
                    if c.card_type == DUMPLING
                )
                possible_scores[card].append(card.dumpling_score(dumplings))
        return possible_scores

    def select_best_card(self):
        """Selects the card with the max score from the possible scores."""
        possible_scores = self.calculate_possible_scores()
        best_card = max(
            possible_scores, key=lambda x: max(possible_scores[x], default=0)
        )
        return best_card


class Game:
    def __init__(self, player1_name, player2_name, rounds, deck):
        """Initalizes Game."""
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        self.rounds = rounds
        self.deck = deck
        self.table = RandomTable(
            [], self.player1, self.player2
        )  # Initialize an empty table for cards played during the game

    def switch_hands(self):
        """Switches hands of players."""
        print("Switch Hands - Sushi Go!")
        self.player1.hand, self.player2.hand = (
            self.player2.hand,
            self.player1.hand,
        )

    def conduct_round(self):
        """Plays a round of Sushi go."""
        overall_scores1 = []
        overall_scores2 = []

        for _ in range(self.rounds):
            round_winners = []
            final_scores1 = []
            final_scores2 = []
            # Assign cards and show hands
            self.player1.assign_cards(self.deck, 3)
            self.player2.assign_cards(self.deck, 3)

            print()
            print(f"Round {_ + 1}")
            print()
            self.player1.show_hand()
            self.player2.show_hand()
            print()

            # Player 1 plays first card and table is updated
            first_card_1 = self.player1.play_max_scoring_card()
            self.table.update_table_with_card(self.player1, first_card_1)
            print("Player 1 plays:", first_card_1)

            # Player 2 plays first card and table is updated
            first_card_2 = self.player2.play_max_scoring_card()
            self.table.update_table_with_card(self.player2, first_card_2)
            print("Player 2 plays:", first_card_2)
            print()

            # Switch hands
            self.switch_hands()
            print()
            self.player1.show_hand()
            self.player2.show_hand()
            print()

            # Players continue to play cards until they have no cards left
            while self.player1.hand:
                best_card1 = self.player1.play_best_card(self.table)
                print("Player 1 plays:", best_card1)
                self.table.update_table_with_card(self.player1, best_card1)

                best_card2 = self.player2.play_best_card(self.table)
                print("Player 2 plays:", best_card2)
                print()
                self.table.update_table_with_card(self.player2, best_card2)

                # Switch hands again for next turn
                self.switch_hands()
                print()
                self.player1.show_hand()
                self.player2.show_hand()
                print()

            # Calculate final scores using the method below
            final_score1 = self.calculate_final_score(self.table.player1_table)
            final_score2 = self.calculate_final_score(self.table.player2_table)

            print(
                f"Player 1's table: {', '.join(str(card) for card in self.table.player1_table)}"
            )
            print(
                f"Player 2's table: {', '.join(str(card) for card in self.table.player2_table)}"
            )
            print()

            print(f"Player 1's final score: {final_score1}")

            print(f"Player 2's final score: {final_score2}")
            print()

            final_scores1.append(final_score1)
            final_scores2.append(final_score2)

            # Reset the table for the next round
            self.table = RandomTable([], self.player1, self.player2)

            # Store the scores of the round
            overall_scores1.append(final_score1)
            overall_scores2.append(final_score2)

            # Determine the winner of the round
            if final_score1 > final_score2:
                print("Player 1 wins the round!")
                round_winners.append(self.player1.name)
            elif final_score2 > final_score1:
                print("Player 2 wins the round!")
                round_winners.append(self.player2.name)
            else:
                print("The round is a tie!")
                round_winners.append("Tie")

        # Determine the overall game winner
        total_score1 = sum(overall_scores1)
        total_score2 = sum(overall_scores2)
        if total_score1 > total_score2:
            print("\nOverall game winner: Player 1\n")
        elif total_score2 > total_score1:
            print("\nOverall game winner: Player 2\n")
        else:
            print("\nOverall game is a tie!\n")

    def calculate_final_score(self, table_cards):
        """Calculates the final score of the player's table."""
        maki_score = 0
        nigiri_score = 0
        tempura_pairs = 0
        sashimi_count = 0
        dumpling_count = 0

        has_wasabi = False
        highest_nigiri_score = 0

        for card in table_cards:
            if card.card_type in ["Maki 1", "Maki 2", "Maki 3"]:
                maki_score += card.score()
            elif card.card_type in [NIGIRI_SQUID, NIGIRI_SALMON, NIGIRI_EGG]:
                nigiri_score += card.score()
                highest_nigiri_score = max(highest_nigiri_score, card.score())
            elif card.card_type == WASABI:
                has_wasabi = True
            elif card.card_type == TEMPURA:
                tempura_pairs += 1
            elif card.card_type == SASHIMI:
                sashimi_count += 1
            elif card.card_type == DUMPLING:
                dumpling_count += 1

        if has_wasabi:
            nigiri_score += (
                highest_nigiri_score * 3
            )  # Assuming there is a nigiri card to apply wasabi

        # Calculate scores for card sets
        tempura_score = (tempura_pairs // 2) * 5
        sashimi_score = (sashimi_count // 3) * 10
        dumpling_score = Card(DUMPLING).dumpling_score(dumpling_count)

        total_score = (
            maki_score
            + nigiri_score
            + tempura_score
            + sashimi_score
            + dumpling_score
        )
        return total_score


if __name__ == "__main__":
    deck = Deck()  # Initialize the deck of cards
    game = Game("Player 1", "Player 2", 2, deck)
    game.conduct_round()
