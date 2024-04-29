# Sushi Go: Biostatistics Final Project
![Logo](Images/sushi_logo.png)

## Introduction
"Sushi Go!" is a card game of strategy and sushi creation. Our project aims to bring this fun and competitive game to life through simulation. 

The game revolves around players who strategically play their cards to accumulate points, however, on each turn the player switches their hand to the player next to them. The goal of this project is to simulate an enitre game of three players which consists of 3 rounds with 9 cards per player per round. At every round, on each turn all players must play a card and leave it on the table at the same time, and then switch their hand to the player next to them. this will be repeated until all cards are played. At the end of each round the score will be tallied, and at the end of all three rounds special points will be added or substracted depending on the *Cumulative Overall Card*.  This simulation will not only provide an enjoyable virtual experience but also serve as a valuable learning tool for those looking to master the art of Sushi Go! strategy, offering insights and tactics that can be applied in real-life gameplay.


## Type of Cards - Game Rules
![cards](Images/sushi_cards.png)

### Stand-alone Cards
- Squid Nigiri: 3 points
- Salmon Nigiri: 2 points
- Egg Nigiri: 1 point

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
- 
### Cumulative-Interactive Cards:
At the end of each round the player that accumulates the most points by summing all their maki cards gets 6 points, second best gets 3 points. 
- Maki Rolls: 1, 2, 3

### Cumulative Overall Card
At the end of the three rounds, the player with the most puddinng cards wins extra points, and the player with less pudding cards loses points.
- Pudding: +6 or -6 points

### Complex Strategy
Each player could strategize based on not only their current hand but also information or probabilities based on previous hands.

Strategy:

Maximizing points of the current play based on the table cards and their current hand before playing a card.


## Skeletal Structure of the Game in Python

### Class Descriptions for the Sushi Go Game Simulation Module

- **Card**: Represents individual Sushi Go cards, providing a method to calculate their base score and a special method for scoring Dumpling cards based on quantity.

- **Deck**: Manages a collection of all possible Sushi Go cards, shuffling them to simulate a deck from which players and the table can draw cards.

- **Player**: Represents a game participant, holding their personal set of cards (hand) and providing methods to draw these cards from the deck, display them, and calculate the player's final score based on game rules.

- **RandomTable**: Represents the collection of cards that are drawn from the deck and placed on the table, visible to all players, allowing interactions such as drawing and displaying these cards.

- **SushiGoMaximizer**: Implements a strategy to maximize points by choosing the best card to play from the player's hand, considering current table cards for optimal scoring.

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
python src/switch_hands.py
```

To run the tests:
```bash
python -m unittest tests/tests_switch_hands.py
```

  
   

