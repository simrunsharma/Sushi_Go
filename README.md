# Sushi Go: Biostatistics Final Project
![Logo](Images/sushi_logo.png)

[![checks](https://github.com/simrunsharma/Sushi_Go/actions/workflows/checks.yml/badge.svg)](https://github.com/simrunsharma/Sushi_Go/actions/workflows/checks.yml)
[![Python Test](https://github.com/simrunsharma/Sushi_Go/actions/workflows/python-test.yml/badge.svg)](https://github.com/simrunsharma/Sushi_Go/actions/workflows/python-test.yml)

## Introduction
"Sushi Go!" is a card game of strategy and sushi creation. Our project aims to bring this fun and competitive game to life through simulation. 

The game revolves around players who strategically play their cards to accumulate points, however, on each turn the player switches their hand to the player next to them. The goal of this project is to simulate an enitre game of two players which consists of 3 rounds with 9 cards per player per round. At every round, on each turn all players must play a card and leave it on the table at the same time, and then switch their hand to the player next to them. this will be repeated until all cards are played. At the end of each round the score will be tallied, and at the end of all three rounds special points will be added or substracted depending on the *Cumulative Overall Card*.  This simulation will not only provide an enjoyable virtual experience but also serve as a valuable learning tool for those looking to master the art of Sushi Go! strategy, offering insights and tactics that can be applied in real-life gameplay.

## Type of Cards and Game Rules
![cards](Images/sushi_cards.png)

### Stand-alone Cards
- Squid Nigiri: 3 points
- Salmon Nigiri: 2 points
- Egg Nigiri: 1 point
- Maki 3: 3 points
- Maki 2: 2 points
- Maki 1: 1 point
  
### Multiplier card
In combination with one Stand-Alone cards, multiplies their value by three
- Wasabi card

### Cumulative-No Penalty Cards
Repeated cards multiply the score.
- Dumpling cards:
- 1 card: 1 points
- 2 cards: 3 points
- 3 cards: 6 points
- 4 cards: 10 points
- 5 cards: 15 points
  
### Cumulative-Penalty Cards
A determined number of cards needs to be played to get all points, else 0 points.
- Sashimi: 3 cards, 10 points
- Tempura: 2 cards, 5 points
  
### Game Strategy

Maximizing points of the current play based on the table cards and their current hand before playing a card.

### Classes and Functions in the Sushi Go Game Simulation

#### `Card`
- **`__init__(self, card_type: str)`**: Initializes a new card with a specific type.
- **`__str__(self)`**: Returns the string representation of the card type.
- **`score(self)`**: Assigns and returns a base score to the card based on its type.
- **`dumpling_score(self, count)`**: Calculates and returns the score for Dumpling cards based on the number played.

#### `Deck`
- **`__init__(self)`**: Initializes a new deck of Sushi Go cards.
- **`_create_deck(self)`**: Creates a deck with the correct distribution of Sushi Go cards and shuffles it.

#### `Player`
- **`__init__(self, name)`**: Initializes a new player with a given name.
- **`assign_cards(self, deck, num_cards)`**: Draws a specified number of cards from the deck for the player’s hand.
- **`show_hand(self)`**: Displays the cards currently in the player's hand.
- **`calculate_final_score(self, table, best_card)`**: Calculates and returns the player’s final score based on the cards on the table and a chosen card.

#### `RandomTable`
- **`__init__(self)`**: Initializes an empty table where cards can be drawn for display.
- **`draw_cards(self, deck, cards_for_t)`**: Draws a specified number of cards from the deck to the table.
- **`show_table(self)`**: Displays the cards currently on the table.
- **`show_final_table(self, best_card)`**: Displays the cards on the table including the selected best card.

#### `SushiGoMaximizer`
- **`__init__(self, player, table)`**: Initializes the maximizer with a player and a table of cards.
- **`calculate_possible_scores(self)`**: Calculates potential scores for each card in the player's hand based on the current table setup.
- **`select_best_card(self)`**: Chooses and returns the best card to play from the hand based on potential score calculations.


## Installation Steps 

### Installation Guide for Sushi Go Game Simulation

#### Requirements

- Python 3.6 or higher
- `random` module (included with Python)

#### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/simrunsharma/Sushi_Go.git
   ```
2. Navigate to the repository directory:
    ```bash
    cd Sushi_Go
    ```
#### Running the Code

To run the main simulation:
```bash
python src/sushi_go_game.py
```

To run the tests:
```bash
python -m unittest tests/tests_switch_hands.py
```



  
   

