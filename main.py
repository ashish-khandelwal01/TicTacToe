import random  # Import random for computer moves

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton  # Import ToggleButton

from tic_tac_toe import *


class TicTacToeGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Add a toggle for game mode selection
        self.mode_toggle = BoxLayout(size_hint_y=None, height=40)
        self.vs_player_button = ToggleButton(text="2 Player", group="mode", state="down")
        self.vs_computer_button = ToggleButton(text="Vs Computer", group="mode")
        self.vs_computer_button.bind(on_press=self.set_game_mode)
        self.vs_player_button.bind(on_press=self.set_game_mode)
        self.mode_toggle.add_widget(self.vs_player_button)
        self.mode_toggle.add_widget(self.vs_computer_button)
        self.add_widget(self.mode_toggle)

        self.status_label = Label(text="Player X's turn", size_hint_y=None, height=40, font_size=24)
        self.add_widget(self.status_label)

        self.grid = GridLayout(cols=3, spacing=10, padding=[10, 10, 10, 10])
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.play_against_computer = False  # Default to 2 Player mode

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = Button(font_size=32, background_color=(0.2, 0.6, 0.8, 1),
                                color=(1, 1, 1, 1),
                                on_press=self.make_move)
                self.grid.add_widget(button)
                row.append(button)
            self.buttons.append(row)

        self.add_widget(self.grid)

    def set_game_mode(self, instance):
        self.play_against_computer = instance.text == "Vs Computer"
        self.reset_game()

    def reset_game(self):
        # Reset the game board and UI
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.status_label.text = "Player X's turn"
        for row in self.buttons:
            for button in row:
                button.text = ''
                button.disabled = False

    def make_move(self, instance):
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j] == instance and self.board[i][j] == ' ':
                    self.board[i][j] = self.current_player
                    instance.text = self.current_player
                    if is_game_finished(self.board, self.current_player):
                        self.status_label.text = f"Player {self.current_player} wins!"
                        self.disable_buttons()
                        return
                    elif all(cell != ' ' for row in self.board for cell in row):
                        self.status_label.text = "It's a tie!"
                        self.disable_buttons()
                        return
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
                    self.status_label.text = f"Player {self.current_player}'s turn"

                    if self.play_against_computer and self.current_player == 'O':
                        self.computer_move()
                    return

    def computer_move(self):
        while True:
            i, j = random.randint(0, 2), random.randint(0, 2)
            if self.board[i][j] == ' ':
                self.board[i][j] = self.current_player
                self.buttons[i][j].text = self.current_player
                if is_game_finished(self.board, self.current_player):
                    self.status_label.text = f"Player {self.current_player} wins!"
                    self.disable_buttons()
                    return
                elif all(cell != ' ' for row in self.board for cell in row):
                    self.status_label.text = "It's a tie!"
                    self.disable_buttons()
                    return
                self.current_player = 'X'
                self.status_label.text = f"Player {self.current_player}'s turn"
                return

    def disable_buttons(self):
        for row in self.buttons:
            for button in row:
                button.disabled = True

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


class TicTacToeApp(App):
    def build(self):
        return TicTacToeGame()


if __name__ == '__main__':
    TicTacToeApp().run()

