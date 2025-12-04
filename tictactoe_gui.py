import tkinter as tk
from tkinter import messagebox, font
import random
from tictactoe import TicTacToe, MinimaxAI

class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
    def on_enter(self, e):
        self['background'] = '#3498DB'  # Light blue on hover
        
    def on_leave(self, e):
        self['background'] = '#34495E'  # Return to original color

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg='#ECF0F1')  # Light gray background
        
        # Game state
        self.game = TicTacToe()
        self.ai = MinimaxAI('O')
        self.current_player = 'X'
        self.player_score = 0
        self.ai_score = 0
        
        # Style configuration
        self.title_font = ('Segoe UI', 24, 'bold')
        self.button_font = ('Segoe UI', 24, 'bold')
        self.label_font = ('Segoe UI', 14)
        self.button_size = 100
        
        # Create and configure the main frame
        self.main_frame = tk.Frame(root, bg='#ECF0F1')
        self.main_frame.pack(padx=20, pady=20)
        
        # Create title with HTML-like formatting
        title_frame = tk.Frame(self.main_frame, bg='#ECF0F1')
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="Tic Tac Toe",
            font=self.title_font,
            bg='#ECF0F1',
            fg='#2C3E50'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Play against AI",
            font=('Segoe UI', 12),
            bg='#ECF0F1',
            fg='#7F8C8D'
        )
        subtitle_label.pack()
        
        # Create score panel
        score_frame = tk.Frame(self.main_frame, bg='#ECF0F1')
        score_frame.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        self.player_score_label = tk.Label(
            score_frame,
            text="You: 0",
            font=self.label_font,
            bg='#ECF0F1',
            fg='#E74C3C'
        )
        self.player_score_label.pack(side=tk.LEFT, padx=20)
        
        vs_label = tk.Label(
            score_frame,
            text="VS",
            font=('Segoe UI', 12, 'bold'),
            bg='#ECF0F1',
            fg='#7F8C8D'
        )
        vs_label.pack(side=tk.LEFT, padx=20)
        
        self.ai_score_label = tk.Label(
            score_frame,
            text="AI: 0",
            font=self.label_font,
            bg='#ECF0F1',
            fg='#3498DB'
        )
        self.ai_score_label.pack(side=tk.LEFT, padx=20)
        
        # Create status label with modern styling
        self.status_label = tk.Label(
            self.main_frame,
            text="Your turn (X)",
            font=self.label_font,
            bg='#ECF0F1',
            fg='#2C3E50'
        )
        self.status_label.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        
        # Create game board with modern buttons
        self.buttons = []
        for i in range(3):
            for j in range(3):
                button = ModernButton(
                    self.main_frame,
                    text="",
                    font=self.button_font,
                    width=3,
                    height=1,
                    command=lambda row=i, col=j: self.make_move(row, col),
                    bg='#34495E',
                    fg='white',
                    activebackground='#2980B9',
                    relief=tk.FLAT,
                    borderwidth=0
                )
                button.grid(row=i+3, column=j, padx=5, pady=5, ipadx=10, ipady=10)
                self.buttons.append(button)
        
        # Create reset button with modern styling
        self.reset_button = ModernButton(
            self.main_frame,
            text="New Game",
            font=self.label_font,
            command=self.reset_game,
            bg='#E74C3C',
            fg='white',
            activebackground='#C0392B',
            relief=tk.FLAT,
            borderwidth=0
        )
        self.reset_button.grid(row=6, column=0, columnspan=3, pady=(20, 0), ipadx=20, ipady=10)

    def make_move(self, row, col):
        """Handle player's move and AI's response."""
        index = row * 3 + col
        
        if self.game.board[index] != ' ' or self.current_player != 'X':
            return
        
        if self.game.make_move(index, 'X'):
            self.buttons[index].config(text='X', fg='#E74C3C')
            self.update_status()
            
            if self.check_game_end():
                return
            
            self.root.after(500, self.make_ai_move)

    def make_ai_move(self):
        """Handle AI's move."""
        if not self.game.empty_squares():
            return
            
        ai_move = self.ai.get_move(self.game)
        
        if self.game.make_move(ai_move, 'O'):
            self.buttons[ai_move].config(text='O', fg='#3498DB')
            self.update_status()
            self.check_game_end()

    def update_status(self):
        """Update the status label with modern styling."""
        if self.game.current_winner:
            if self.game.current_winner == 'X':
                self.status_label.config(text="🎉 You win! 🎉", fg='#27AE60')
                self.player_score += 1
                self.player_score_label.config(text=f"You: {self.player_score}")
            else:
                self.status_label.config(text="🤖 AI wins! 🤖", fg='#E74C3C')
                self.ai_score += 1
                self.ai_score_label.config(text=f"AI: {self.ai_score}")
        elif not self.game.empty_squares():
            self.status_label.config(text="🤝 It's a tie! 🤝", fg='#F1C40F')
        else:
            self.status_label.config(
                text="Your turn (X)" if self.current_player == 'X' else "AI's turn (O)",
                fg='#2C3E50'
            )

    def check_game_end(self):
        """Check if the game has ended and handle the result."""
        if self.game.current_winner or not self.game.empty_squares():
            if self.game.current_winner == 'X':
                messagebox.showinfo("Game Over", "🎉 Congratulations! You win! 🎉")
            elif self.game.current_winner == 'O':
                messagebox.showinfo("Game Over", "🤖 AI wins! Better luck next time! 🤖")
            else:
                messagebox.showinfo("Game Over", "🤝 It's a tie! 🤝")
            return True
        return False

    def reset_game(self):
        """Reset the game state."""
        self.game = TicTacToe()
        self.current_player = 'X'
        for button in self.buttons:
            button.config(text="", state='normal')
        self.status_label.config(text="Your turn (X)", fg='#2C3E50')

def main():
    root = tk.Tk()
    root.resizable(False, False)
    
    # Set window icon and title
    root.title("Tic Tac Toe - Modern Edition")
    
    app = TicTacToeGUI(root)
    
    # Center the window on the screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == '__main__':
    main() 
