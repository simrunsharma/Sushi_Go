# Sushi Go: Biostatistics Final Project

## Introduction
"Sushi Go!" is a delightful card game of strategy and sushi selection, and our project aims to bring this fun and competitive game to life through simulation. By creating a library with classes like `Game`, `Deck`, `Player`, and `Card`, we are developing a tool for competitive game players who seek to enhance their strategic skills in Sushi Go! The game revolves around a dealer who deals out a hand of cards to each player, and then players strategically play their cards to accumulate points. The goal is to understand each player's gameplay and predict the winner based on their decisions. This simulation will not only provide an enjoyable virtual experience but also serve as a valuable learning tool for those looking to master the art of Sushi Go! strategy, offering insights and tactics that can be applied in real-life gameplay.

## Types of Cards
### Stand-alone Cards
- Squid Nigiri: 3 points
- Salmon Nigiri: 2 points
- Egg Nigiri: 1 point

### Cumulative (No Penalty) Cards
Repeated cards multiply the score.
- Dumpling cards: 1, 2, 6, 9

### Cumulative (Penalty) Cards
A determined number of cards needs to be played to get all points, else 0 points.
- Sashimi: 3 cards, 5 points
- Tempura: 2 cards, 5 points

### Cumulative Overall Card
- Pudding: At the end of 3 rounds, the player with the most cards wins extra points, and the player with fewer cards loses points.

### Complex Strategy
Each player could strategize based on not only their current deck but also information or probabilities based on previous rounds.

Each player needs a defined strategy of either:
1. Maximizing points of the current play based on the table cards (comparing their score and other players' scores) before playing a card.
2. Maximizing points based on the probability of getting the cumulative cards in subsequent rounds to maximize cards of this card.

### Danger Zone Strategy
- Chopstick card: When played, the player can play two cards together in the next round after playing this card.

Each player could strategize based on not only their current deck but also information or probabilities based on previous or go decks.

## Skeletal Structure of the Game in Python
We plan to have multiple classes - `Card`, `Deck`, `Player`, and `Game` - that account for different features of the game and then calculate the winner based on the highest number of points. In this simulation, the game is structured around multiple rounds where players try to maximize their points by collecting and playing sets of cards efficiently, with the end goal of having the highest score at the conclusion of all rounds.

Here is a brief overview of the function of each class in our library:

### Class: Card
Represents a single sushi-themed playing card. Each card has a type indicating its category, such as "Tempura" or "Sashimi".

### Class: Deck
Manages a collection of cards used in the game. This class is responsible for creating a full deck of cards, shuffling them, and distributing them among players to start the game.

### Class: Player
Describes a participant in the game. This includes managing the player's hand of cards, recording which cards have been played, calculating scores based on the rules of the game, and tracking specific scoring combinations.

### Class: Game
Coordinates the overall gameplay. It initializes the deck and players, handles the flow of the game across multiple rounds, determines the scores after each round, and at the end, identifies the winner of the game. Each round involves players drawing and playing a card from their hand according to strategic goals.
