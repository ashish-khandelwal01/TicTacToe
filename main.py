import random
import platform
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.lang import Builder
import os


LabelBase.register(name="MyFont", fn_regular="fonts/NotoColorEmoji.ttf")

# Load KV file
KV_PATH = os.path.join(os.path.dirname(__file__), "myapp.kv")
Builder.load_file(KV_PATH)

def has_contestant_won(board, symbol):
    for i in range(3):
        if all(board[i][j] == symbol for j in range(3)):
            return True
        if all(board[j][i] == symbol for j in range(3)):
            return True
    if all(board[i][i] == symbol for i in range(3)):
        return True
    if all(board[i][2 - i] == symbol for i in range(3)):
        return True
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

class TicTacToeGame(BoxLayout):
    board = [" "] * 9
    current_player = "X"
    play_against_computer = False
    game_over = False

    def set_game_mode(self, instance):
        self.play_against_computer = "Computer" in instance.text
        self.reset_game()

    def reset_game(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.game_over = False
        self.ids.status_label.text = "🎮 Player X's turn"
        self.ids.status_label.color = (0.2, 0.5, 0.8, 1)
        for i in range(9):
            btn = self.ids[f"btn_{i}"]
            btn.text = ""
            btn.background_color = (0.9, 0.95, 1, 1)
            btn.color = (0.2, 0.3, 0.7, 1)
            btn.disabled = False

    def make_move(self, idx):
        if self.game_over or self.board[idx] != " ":
            return

        self.board[idx] = self.current_player
        btn = self.ids[f"btn_{idx}"]
        btn.text = self.current_player
        btn.color = (0.85, 0.2, 0.2, 1) if self.current_player == "X" else (0.2, 0.6, 0.8, 1)
        btn.disabled = True

        if has_contestant_won(self._board_matrix(), self.current_player):
            self.ids.status_label.text = f"🏆 Player {self.current_player} Wins!"
            self.ids.status_label.color = (0.2, 0.7, 0.2, 1)
            self.game_over = True
            self.highlight_winner()
            return

        if is_board_full(self._board_matrix()):
            self.ids.status_label.text = "🤝 It's a Tie!"
            self.ids.status_label.color = (0.8, 0.6, 0.2, 1)
            self.game_over = True
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        if self.play_against_computer and self.current_player == "O":
            self.ids.status_label.text = "🤖 Computer thinking..."
            Clock.schedule_once(lambda dt: self.computer_move(), 0.5)
        else:
            self.ids.status_label.text = f"🎮 Player {self.current_player}'s turn"

    def computer_move(self):
        moves = [i for i, cell in enumerate(self.board) if cell == " "]
        if moves:
            self.make_move(random.choice(moves))

    def _board_matrix(self):
        return [self.board[i*3:(i+1)*3] for i in range(3)]

    def highlight_winner(self):
        for i, cell in enumerate(self.board):
            if cell != " ":
                btn = self.ids[f"btn_{i}"]
                btn.background_color = (1, 0.95, 0.7, 1)

class TicTacToeApp(App):
    def build(self):
        self.title = "Tic Tac Toe"
        return TicTacToeGame()

if __name__ == "__main__":
    TicTacToeApp().run()
