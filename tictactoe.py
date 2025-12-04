import random
from colorama import init, Fore, Style
import os

# Initialize colorama
init()

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        """Print the current state of the board with colors and position numbers."""
        print("\n")
        for i in range(3):
            print(" " + " | ".join(self.board[i*3:(i+1)*3]))
            if i < 2:
                print("-----------")
        print("\n")

    def print_board_nums(self):
        """Print the board with position numbers for reference."""
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print(" " + " | ".join(row))
            if row != number_board[-1]:
                print("-----------")

    def available_moves(self):
        """Return a list of available moves (indices where the board is empty)."""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        """Return True if there are empty squares on the board."""
        return ' ' in self.board

    def num_empty_squares(self):
        """Return the number of empty squares on the board."""
        return self.board.count(' ')

    def make_move(self, square, letter):
        """Make a move on the board if the square is available."""
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        """Check if the last move resulted in a win."""
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True

        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Check diagonal
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False

class MinimaxAI:
    def __init__(self, letter):
        self.letter = letter
        self.opponent_letter = 'X' if letter == 'O' else 'O'

    def get_move(self, game):
        """Get the best move using minimax algorithm with alpha-beta pruning."""
        if len(game.available_moves()) == 9:
            # If it's the first move, choose a random corner or center
            return random.choice([0, 2, 4, 6, 8])
        
        return self.minimax(game, self.letter, float('-inf'), float('inf'))['position']

    def minimax(self, game, player, alpha, beta):
        """Minimax algorithm with alpha-beta pruning."""
        available_moves = game.available_moves()

        # Terminal conditions
        if game.current_winner == self.opponent_letter:
            return {'position': None, 'score': -1 * (game.num_empty_squares() + 1)}
        elif game.current_winner == self.letter:
            return {'position': None, 'score': 1 * (game.num_empty_squares() + 1)}
        elif not game.empty_squares():
            return {'position': None, 'score': 0}

        if player == self.letter:
            best = {'position': None, 'score': float('-inf')}
        else:
            best = {'position': None, 'score': float('inf')}

        for possible_move in available_moves:
            # Make a move
            game.make_move(possible_move, player)

            # Recursive call
            sim_score = self.minimax(game, self.opponent_letter if player == self.letter else self.letter, alpha, beta)

            # Undo move
            game.board[possible_move] = ' '
            game.current_winner = None
            sim_score['position'] = possible_move

            # Update best score
            if player == self.letter:
                if sim_score['score'] > best['score']:
                    best = sim_score
                alpha = max(alpha, best['score'])
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                beta = min(beta, best['score'])

            if beta <= alpha:
                break

        return best

def play(game, x_player, o_player, print_game=True):
    """Play the game."""
    if print_game:
        print(Fore.CYAN + "Welcome to Tic-Tac-Toe!" + Style.RESET_ALL)
        print(Fore.YELLOW + "You are 'X' and the AI is 'O'" + Style.RESET_ALL)
        print("\nHere's the board with position numbers:")
        game.print_board_nums()
        print("\nLet's begin!\n")

    letter = 'X'  # Starting player

    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = None
            while square is None:
                try:
                    square = int(input(Fore.GREEN + f"{letter}'s turn. Input move (1-9): " + Style.RESET_ALL)) - 1
                    if square not in game.available_moves():
                        raise ValueError
                except ValueError:
                    print(Fore.RED + "Invalid move! Try again." + Style.RESET_ALL)
                    square = None

        if game.make_move(square, letter):
            if print_game:
                print(f"\n{letter} makes a move to square {square + 1}")
                game.print_board()
                print("")

            if game.current_winner:
                if print_game:
                    if letter == 'X':
                        print(Fore.GREEN + "Congratulations! You win!" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "AI wins! Better luck next time!" + Style.RESET_ALL)
                return letter

            letter = 'O' if letter == 'X' else 'X'

    if print_game:
        print(Fore.YELLOW + "It's a tie!" + Style.RESET_ALL)
    return None

def main():
    """Main game loop."""
    while True:
        game = TicTacToe()
        ai = MinimaxAI('O')
        play(game, None, ai, print_game=True)
        
        while True:
            play_again = input(Fore.CYAN + "\nWould you like to play again? (y/n): " + Style.RESET_ALL).lower()
            if play_again in ['y', 'n']:
                break
            print(Fore.RED + "Please enter 'y' or 'n'" + Style.RESET_ALL)
        
        if play_again == 'n':
            print(Fore.YELLOW + "\nThanks for playing! Goodbye!" + Style.RESET_ALL)
            break
        
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    main() 
