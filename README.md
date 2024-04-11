# Sushi Go: Biostatistics Final Project
![UML Diagram](https://private-user-images.githubusercontent.com/141798228/321368094-26724e4b-869d-4002-9b3d-38a2245eb292.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTI3NzUzNTIsIm5iZiI6MTcxMjc3NTA1MiwicGF0aCI6Ii8xNDE3OTgyMjgvMzIxMzY4MDk0LTI2NzI0ZTRiLTg2OWQtNDAwMi05YjNkLTM4YTIyNDVlYjI5Mi5wbmc\_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwNDEwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDQxMFQxODUwNTJaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0xMTA2MGYzOTFkZDYwNzgyZmUyNzA3OWQ2NmJlMmUzMjFlM2VjMzRmZmFjNTA2MGQ4MGU4Njk4Y2YxMGNjMzUyJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.5HtstFJbYv2_f_WtZOtrYotexpZDFz6sPqutAcmaDF0)

## Introduction
"Sushi Go!" is a card game of strategy and sushi creation. Our project aims to bring this fun and competitive game to life through simulation. 

The game revolves around players who strategically play their cards to accumulate points, however, on each turn the player switches their hand to the players next to them. The goal of this project is to simulate an enitre play which consists on 3 rounds with 9 cards played by each player on each round. This simulation will not only provide an enjoyable virtual experience but also serve as a valuable learning tool for those looking to master the art of Sushi Go! strategy, offering insights and tactics that can be applied in real-life gameplay.

By creating a library with classes like `Game`, `Deck`, `Player`, and `Card`, we are developing a tool for competitive game players who seek to enhance their strategic skills in Sushi Go! 

![Alt Text](https://private-user-images.githubusercontent.com/141798228/321367429-b02c0d88-13a3-4160-8ae6-db51f0c2d67a.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTI3NzUxOTksIm5iZiI6MTcxMjc3NDg5OSwicGF0aCI6Ii8xNDE3OTgyMjgvMzIxMzY3NDI5LWIwMmMwZDg4LTEzYTMtNDE2MC04YWU2LWRiNTFmMGMyZDY3YS5wbmc\_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwNDEwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDQxMFQxODQ4MTlaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT02OTkwMDRiMWE2OWE4OTAwODgzM2MxNjRiOTAyYTg0NTg5YWQ1OTVmOTdlMjU2MzRiYWM4NzJiYTMwN2JmMjkyJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.OtkdQbk9HLb5b75RiKTDq6YyRk5RXxe4agao66HFlF4)

## Types of Cards
### Stand-alone Cards
- Squid Nigiri: 3 points
- Salmon Nigiri: 2 points
- Egg Nigiri: 1 point

### Cumulative (No Penalty) Cards
Repeated cards multiply the score.
- Dumpling cards: 1, 3, 6, 9

### Cumulative (Penalty) Cards
A determined number of cards needs to be played to get all points, else 0 points.
- Sashimi: 3 cards, 5 points
- Tempura: 2 cards, 5 points
- 
### Cumulative Player Cards:
At the end of each round the players that accumulates the most points of this card compared to the other players gets 6 points, second best gets 3 points. 
- Maki Rolls: 1, 2, 3

### Cumulative Overall Card
- Pudding: At the end of the three rounds, the player with the most puddinng cards wins extra points, and the player with fewer cards loses points.

### Complex Strategy
Each player could strategize based on not only their current hand but also information or probabilities based on previous hands.

Each player needs a defined strategy of either:
1. Maximizing points of the current play based on the table cards and theri current hand before playing a card.
2. Maximizing points based on the probability of getting the cumulative cards in subsequent rounds to maximize cards of this card.

### Danger Zone Strategy (very complex type of card)
- Chopstick card: When played, the player can play two cards together in the next round after playing this card.


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

### Class:Score
Adds the points at the end of each round according to cumulative cards, non cumulative cards and cumulative-interaction cards
Adds points at the end of the three rounds

# Class: Sushi platter
Generates image of the winning player sushi plater according to all the cards he played
