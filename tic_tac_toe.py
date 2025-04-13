import tkinter as tk
from tkinter import messagebox

class Player:
    def __init__(self, name, symbol, color):
        self.name = name
        self.symbol = symbol
        self.color = color
        self.score = 0

class Move:
    def __init__(self, row, col, player):
        self.row = row
        self.col = col
        self.player = player

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.config(bg="#f7f7f7")
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.player1 = Player("Player 1", "X", "#ff6b6b")  # Red
        self.player2 = Player("Player 2", "O", "#4ecdc4")  # Turquoise
        self.current_player = self.player1

        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg="#f7f7f7")
        self.frame.pack(pady=10)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.frame, text="", width=6, height=3,
                    font=("Arial", 28, "bold"),
                    bg="#fff", fg="#333",
                    activebackground="#e0e0e0",
                    command=lambda row=i, col=j: self.handle_click(row, col)
                )
                btn.grid(row=i, column=j, padx=4, pady=4)
                self.buttons[i][j] = btn

        # Score & Turn display
        self.info_frame = tk.Frame(self.root, bg="#f7f7f7")
        self.info_frame.pack(pady=5)

        self.turn_label = tk.Label(self.info_frame, text=self.get_turn_text(), font=("Arial", 16), bg="#f7f7f7", fg=self.current_player.color)
        self.turn_label.pack()

        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Arial", 14), bg="#f7f7f7")
        self.score_label.pack(pady=5)

        # Control buttons
        self.control_frame = tk.Frame(self.root, bg="#f7f7f7")
        self.control_frame.pack(pady=10)

        self.restart_button = tk.Button(self.control_frame, text="🔄 Restart", font=("Arial", 12), command=self.reset_board, bg="#ffe66d", fg="#333")
        self.restart_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = tk.Button(self.control_frame, text="❌ Exit", font=("Arial", 12), command=self.root.quit, bg="#ff6b6b", fg="white")
        self.exit_button.pack(side=tk.LEFT, padx=10)

    def handle_click(self, row, col):
        if self.board[row][col] == "":
            move = Move(row, col, self.current_player)
            self.board[row][col] = move.player.symbol
            self.buttons[row][col].config(text=move.player.symbol, fg=move.player.color)

            if self.check_winner(move.player.symbol):
                self.highlight_winner(move.player.color)
                self.current_player.score += 1
                self.score_label.config(text=self.get_score_text())
                messagebox.showinfo("Game Over", f"{move.player.name} wins!")
                self.disable_board()
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.disable_board()
            else:
                self.toggle_player()

    def check_winner(self, symbol):
        b = self.board
        self.winning_combo = []

        for i in range(3):
            if all(b[i][j] == symbol for j in range(3)):
                self.winning_combo = [(i, j) for j in range(3)]
                return True
            if all(b[j][i] == symbol for j in range(3)):
                self.winning_combo = [(j, i) for j in range(3)]
                return True

        if all(b[i][i] == symbol for i in range(3)):
            self.winning_combo = [(i, i) for i in range(3)]
            return True
        if all(b[i][2 - i] == symbol for i in range(3)):
            self.winning_combo = [(i, 2 - i) for i in range(3)]
            return True

        return False

    def highlight_winner(self, color):
        for row, col in self.winning_combo:
            self.buttons[row][col].config(bg="#caffbf", fg=color)

    def is_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def toggle_player(self):
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2
        self.turn_label.config(text=self.get_turn_text(), fg=self.current_player.color)

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ""
                self.buttons[i][j].config(text="", bg="#fff", fg="#333", state=tk.NORMAL)
        self.current_player = self.player1
        self.turn_label.config(text=self.get_turn_text(), fg=self.current_player.color)

    def disable_board(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.buttons[i][j].config(state=tk.DISABLED)
        self.root.after(1000, self.enable_board)

    def enable_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.NORMAL)

    def get_score_text(self):
        return f"{self.player1.name} (X): {self.player1.score} | {self.player2.name} (O): {self.player2.score}"

    def get_turn_text(self):
        return f"{self.current_player.name}'s Turn ({self.current_player.symbol})"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()
