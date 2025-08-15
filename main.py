import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.clock import Clock
from kivy.animation import Animation


def has_contestant_won(board, symbol):
    for i in range(3):
        if all(board[i][j] == symbol for j in range(3)): return True
        if all(board[j][i] == symbol for j in range(3)): return True
    if all(board[i][i] == symbol for i in range(3)): return True
    if all(board[i][2 - i] == symbol for i in range(3)): return True
    return False


def is_board_full(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))


class TicTacToeGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 15
        self.padding = [20, 20, 20, 20]

        # Gradient background
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # Title
        self.title_label = Label(
            text="🎯 Tic Tac Toe Deluxe 🎯",
            size_hint_y=None,
            height=60,
            font_size=36,
            color=(0.15, 0.25, 0.45, 1),
            bold=True
        )
        self.add_widget(self.title_label)

        # Mode selection
        self.mode_container = BoxLayout(size_hint_y=None, height=50, spacing=10)
        mode_label = Label(text="Mode:", size_hint_x=None, width=70, color=(0.3, 0.3, 0.3, 1), font_size=18)
        self.mode_container.add_widget(mode_label)

        self.vs_player_button = ToggleButton(
            text="👥 Players",
            group="mode",
            state="down",
            background_color=(0.3, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size=16
        )
        self.vs_computer_button = ToggleButton(
            text="🤖 Computer",
            group="mode",
            background_color=(0.8, 0.4, 0.4, 1),
            color=(1, 1, 1, 1),
            font_size=16
        )
        self.vs_player_button.bind(on_press=self.set_game_mode)
        self.vs_computer_button.bind(on_press=self.set_game_mode)
        self.mode_container.add_widget(self.vs_player_button)
        self.mode_container.add_widget(self.vs_computer_button)
        self.add_widget(self.mode_container)

        # Status
        self.status_label = Label(
            text="🎮 Player X's turn",
            size_hint_y=None,
            height=50,
            font_size=22,
            color=(0.2, 0.5, 0.8, 1),
            bold=True
        )
        self.add_widget(self.status_label)

        # Grid
        self.grid = GridLayout(cols=3, spacing=10, size_hint=(1, 0.7))
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.play_against_computer = False
        self.game_over = False
        self.buttons = []

        for i in range(3):
            row = []
            for j in range(3):
                btn = Button(
                    font_size=48,
                    background_color=(0.95, 0.95, 0.95, 1),
                    color=(0.2, 0.3, 0.7, 1),
                    bold=True
                )
                btn.bind(on_press=self.make_move)
                row.append(btn)
                self.grid.add_widget(btn)
            self.buttons.append(row)

        self.add_widget(self.grid)

        # Reset
        self.reset_button = Button(
            text="🔄 New Game",
            size_hint_y=None,
            height=50,
            background_color=(0.4, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            bold=True,
            on_press=lambda x: self.reset_game()
        )
        self.add_widget(self.reset_button)

    def _update_bg(self, instance, value):
        self.bg.size = instance.size
        self.bg.pos = instance.pos

    def set_game_mode(self, instance):
        self.play_against_computer = instance.text == "🤖 Computer"
        self.reset_game()

    def reset_game(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.status_label.text = "🎮 Player X's turn"
        self.status_label.color = (0.2, 0.5, 0.8, 1)
        for row in self.buttons:
            for btn in row:
                btn.text = ''
                btn.disabled = False
                btn.background_color = (0.95, 0.95, 0.95, 1)
                btn.color = (0.2, 0.3, 0.7, 1)

    def make_move(self, instance):
        if self.game_over: return
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j] == instance and self.board[i][j] == ' ':
                    self._place_symbol(i, j)
                    return

    def _place_symbol(self, i, j):
        self.board[i][j] = self.current_player
        btn = self.buttons[i][j]
        btn.text = self.current_player
        btn.color = (0.85, 0.2, 0.2, 1) if self.current_player == 'X' else (0.2, 0.6, 0.8, 1)
        btn.disabled = True
        Animation(scale=1.2, d=0.1) + Animation(scale=1, d=0.1)  # pulse animation

        if has_contestant_won(self.board, self.current_player):
            self.status_label.text = f"🏆 Player {self.current_player} Wins!"
            self.status_label.color = (0.2, 0.7, 0.2, 1)
            self.game_over = True
            self.highlight_winner()
            return
        if is_board_full(self.board):
            self.status_label.text = "🤝 It's a Tie!"
            self.status_label.color = (0.8, 0.6, 0.2, 1)
            self.game_over = True
            return

        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.status_label.text = f"🎮 Player {self.current_player}'s turn"

        if self.play_against_computer and self.current_player == 'O':
            self.status_label.text = "🤖 Computer thinking..."
            Clock.schedule_once(lambda dt: self.computer_move(), 0.5)

    def computer_move(self):
        if self.game_over: return
        moves = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']
        if moves:
            i, j = random.choice(moves)
            self._place_symbol(i, j)

    def highlight_winner(self):
        for row in self.buttons:
            for btn in row:
                if btn.text:
                    btn.background_color = (1, 0.95, 0.7, 1)  # glow effect


class TicTacToeApp(App):
    def build(self):
        self.title = "Tic Tac Toe"
        return TicTacToeGame()


if __name__ == '__main__':
    TicTacToeApp().run()
