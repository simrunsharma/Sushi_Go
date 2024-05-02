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
        cards.extend(
            [
                Card(mr)
                for mr in MAKI_ROLLS
                for _ in range([6, 12, 8][MAKI_ROLLS.index(mr)])
            ]
        )
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

    def play_max_scoring_card(self):
        if not self.hand:
            print(f"{self.name} has no cards to play.")
            return None

        max_scoring_card = max(self.hand, key=lambda card: card.score())
        self.hand.remove(max_scoring_card)
        return max_scoring_card

    def play_best_card(self, table):
        maximizer = SushiGoMaximizer(self, table)
        best_card = maximizer.select_best_card()
        if best_card:
            print(f"{self.name} plays: {best_card}")
            self.hand.remove(best_card)
            return best_card
        else:
            print("No card to play.")
            return None

    def calculate_final_score(self, table, best_card):
        table_cards = table.cards_on_table
        maki_counts = [
            card.score()
            for card in table_cards
            if card.card_type in ["Maki 1", "Maki 2", "Maki 3"]
        ]
        maki_score = 0
        if maki_counts:
            max_maki = max(maki_counts)
            maki_score = 6 if maki_counts.count(max_maki) == 1 else 3
            if maki_counts.count(max_maki) > 1:
                maki_counts = [count for count in maki_counts if count != max_maki]
            if maki_counts:
                second_max_maki = max(maki_counts)
                maki_score += 3 if maki_counts.count(second_max_maki) == 1 else 1

        nigiri_scores = [
            card.score()
            for card in table_cards
            if card.card_type in [NIGIRI_SQUID, NIGIRI_SALMON, NIGIRI_EGG]
        ]

        tempura_count = sum(1 for card in table_cards if card.card_type == TEMPURA)
        sashimi_count = sum(1 for card in table_cards if card.card_type == SASHIMI)
        dumpling_count = sum(1 for card in table_cards if card.card_type == DUMPLING)
        wasabi_applied = any(card.card_type == WASABI for card in table_cards)

        # Calculate scores
        tempura_score = (tempura_count // 2) * 5
        sashimi_score = (sashimi_count // 3) * 10
        dumpling_score = Card(DUMPLING).dumpling_score(dumpling_count)
        highest_nigiri = max(nigiri_scores, default=0)
        nigiri_score = sum(nigiri_scores) + (
            3 * highest_nigiri if wasabi_applied else 0
        )

        total_score = (
            maki_score + nigiri_score + tempura_score + sashimi_score + dumpling_score
        )
        return total_score


class RandomTable:
    """Cards randomly drawn on the table for the player to interact with."""

    def __init__(self, cards_on_table, player1, player2):
        self.cards_on_table = cards_on_table if cards_on_table is not None else []
        self.player1 = player1
        self.player2 = player2
        self.player1_table = []
        self.player2_table = []

    def show_table(self, player):
        if player == self.player1:
            print([str(card) for card in self.player1_table])
        elif player == self.player2:
            print([str(card) for card in self.player2_table])
        else:
            raise ValueError("Invalid player")

    # def draw_cards(self, deck, cards_for_t):
    #     if len(deck.cards) < cards_for_t:
    #         print("Error: Not enough cards in the deck to draw.")
    #         return
    #     if cards_for_t == 0:
    #         print("Error: Number of cards on the table cannot be 0.")
    #         return
    #     self.cards_on_table = deck.cards[:cards_for_t]
    #     deck.cards = deck.cards[cards_for_t:]

    def add_card(self, card):
        self.cards_on_table.append(card)

    def show_table(self):
        for card in self.cards_on_table:
            print(card)

    def update_table_with_card(self, player, card):
        """
        This function adds a card to the player's table.
        """
        if player == self.player1:
            self.player1_table.append(card)
        elif player == self.player2:
            self.player2_table.append(card)
        else:
            raise ValueError("Invalid player")

        return self

    # def show_final_table(self, best_card):
    #     final_table = self.cards_on_table + [best_card]
    #     for card in final_table:
    #         print(card)


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
                    if table_card.card_type in [
                        NIGIRI_SQUID,
                        NIGIRI_SALMON,
                        NIGIRI_EGG,
                    ]:
                        possible_scores[card].append(table_card.score() * 3)
            elif card.card_type == TEMPURA:
                possible_scores[card].append(
                    5
                    if any(c.card_type == TEMPURA for c in self.table.cards_on_table)
                    else 0
                )
            elif card.card_type == SASHIMI:
                possible_scores[card].append(
                    10
                    if sum(
                        1 for c in self.table.cards_on_table if c.card_type == SASHIMI
                    )
                    >= 2
                    else 0
                )
            elif card.card_type == DUMPLING:
                dumplings = sum(
                    1 for c in self.table.cards_on_table if c.card_type == DUMPLING
                )
                possible_scores[card].append(card.dumpling_score(dumplings))
        return possible_scores

    def select_best_card(self):
        possible_scores = self.calculate_possible_scores()
        best_card = max(
            possible_scores, key=lambda x: max(possible_scores[x], default=0)
        )
        return best_card


class Game:
    def __init__(self, player1_name, player2_name, rounds, deck):
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        self.rounds = rounds
        self.deck = deck
        self.final_table = RandomTable(None, self.player1, self.player2)

    def switch_hands(self):
        self.player1.hand, self.player2.hand = self.player2.hand, self.player1.hand

    def conduct_round(self):
        for _ in range(self.rounds):
            # Assign cards and show hands
            self.player1.assign_cards(self.deck, 3)
            self.player2.assign_cards(self.deck, 3)
            self.player1.show_hand()
            self.player2.show_hand()

            # Player 1 plays first card and table is initialized with it
            first_card_1 = self.player1.play_max_scoring_card()
            self.table = RandomTable([first_card_1], self.player1, self.player2)
            print("Player 1's table:")
            self.table.show_table()
            self.player1.show_hand()

            first_card_2 = self.player2.play_max_scoring_card()
            self.table = RandomTable([first_card_2], self.player1, self.player2)
            print("Player 2's table:")
            self.table.show_table()
            self.player2.show_hand()

            # Switch hands
            self.switch_hands()

            # Player 1 and Player 2 play cards until they have no cards left

            while self.player1.hand:
                # Player 2 selects best card and updates table
                best_card = self.player2.play_best_card(self.table)
                self.table.update_table_with_card(self.player2, best_card)
                print(
                    f"Player 2's table: {[str(card) for card in self.table.player2_table]}"
                )
                self.player2.show_hand()

                # Player 1 selects best card and updates table
                best_card = self.player1.play_best_card(self.table)
                self.table.update_table_with_card(self.player1, best_card)
                print(
                    f"Player 1's table: {[str(card) for card in self.table.player1_table]}"
                )
                self.player1.show_hand()

                # Switch hands
                self.switch_hands()

                print(
                    f"Player 1's table: {[str(card) for card in self.table.player1_table]}"
                )
                print(
                    f"Player 2's table: {[str(card) for card in self.table.player2_table]}"
                )

            final_score1 = self.player1.calculate_final_score(
                self.final_table, first_card_1
            )
            final_score2 = self.player2.calculate_final_score(
                self.final_table, first_card_2
            )
            print(f"Player 1's final score: {final_score1}")
            print(f"Player 2's final score: {final_score2}")
            print("\nEnd of game\n")


if __name__ == "__main__":
    deck = Deck()  # Set the deck size here
    game = Game("Player 1", "Player 2", 1, deck)
    game.conduct_round()

    # deck = Deck()  # Correctly create a Deck object which initializes its own cards
    # player_1 = Player("Player 1")
    # player_1.assign_cards(deck, 3)  # Ensure to pass the deck's cards list
    # player_1.show_hand()
    # # player_2 = Player("Player 2")
    # # player_2.assign_cards(deck, 3)
    # # player_2.show_hand()

    # first_card = player_1.play_max_scoring_card()
    # table_1 = RandomTable(first_card)
    # # table_1.draw_cards(deck, 3)
    # print("Table 1 cards:")
    # table_1.show_table()
    # player_1.show_hand()
    # while player_1.hand:
    #     table_1.update_table(player_1)
    #     print("Table 1 cards:")
    #     table_1.show_table()
    # player_1.show_hand()
    # player_1.calculate_final_score
    # maximizer = SushiGoMaximizer(player, table)
    # best_card = maximizer.select_best_card()
    # if best_card:
    #     print(f"{player.name} plays: {best_card}")
    #     final_score = player.calculate_final_score(table, best_card)
    #     print(f"Final score for {player.name}: {final_score}")
    #     table.show_final_table(best_card)
    # else:
    #     print("No card to play.")