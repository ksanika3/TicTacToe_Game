# Tic-Tac-Toe with AI

This is an implementation of the classic Tic-Tac-Toe game where you can play against an AI opponent. The AI uses the Minimax algorithm with Alpha-Beta Pruning to make optimal moves, making it virtually unbeatable.

## Features

- Play against an AI opponent that uses Minimax algorithm with Alpha-Beta Pruning
- Clean command-line interface with colored output
- Interactive game board display
- Clear game state feedback

## Requirements

- Python 3.6 or higher
- colorama package

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game using:
```bash
python tictactoe.py
```

- You will play as 'X' and the AI will play as 'O'
- Enter your moves by specifying the position (1-9) as shown on the board
- The positions are numbered from left to right, top to bottom:
```
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9
```

## How it Works

The AI uses the Minimax algorithm with Alpha-Beta Pruning to evaluate all possible moves and choose the optimal one. This makes the AI unbeatable - the best you can do is draw the game.

- Minimax Algorithm: Evaluates all possible game states to find the best move
- Alpha-Beta Pruning: Optimizes the search by eliminating branches that won't affect the final decision
- The AI always plays as 'O' and tries to minimize the player's score while maximizing its own 
