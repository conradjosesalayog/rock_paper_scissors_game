from random import choice

import tkinter as tk
from tkinter import messagebox, simpledialog

from rock_paper_scissors_class import Player

move_emojis = {
    "rock": "🪨 Rock",
    "paper": "📄 Paper",
    "scissors": "✂️ Scissors",
}


class HumanPlayer(Player):
    def get_move(self, chosen_move=None):
        if chosen_move not in self.valid_moves:
            raise ValueError(f"Invalid move received from GUI: {chosen_move}")
        return chosen_move


class ComputerPlayer(Player):
    def get_move(self, chosen_move=None):
        return choice(self.valid_moves)


class GameReferee:
    outcome_tie = "tie"

    _winning_moves = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper",
    }

    @classmethod
    def determine_winner(cls, human_player, computer_player, human_move, computer_move):
        if human_move == computer_move:
            return cls.outcome_tie

        if cls._winning_moves[human_move] == computer_move:
            human_player.increment_score()
            return human_player.player_name

        computer_player.increment_score()
        return computer_player.player_name


class RockPaperScissorsApp:
    def __init__(self, root_window):
        self._root_window = root_window
        self._root_window.title("Rock Paper Scissors")
        self._root_window.geometry("420x420")
        self._root_window.resizable(False, False)

        player_name = self._ask_for_player_name()

        self._human_player = HumanPlayer(player_name)
        self._computer_player = ComputerPlayer("Computer")

        self._build_widgets()

    def _ask_for_player_name(self):
        player_name = simpledialog.askstring(
            "Welcome!", "Please enter your name:", parent=self._root_window
        )
        return player_name.strip() if player_name else "Player"

    def _build_widgets(self):
        title_label = tk.Label(
            self._root_window,
            text=f"Welcome, {self._human_player.player_name}!",
            font=("Helvetica", 18, "bold"),
        )
        title_label.pack(pady=15)

        self._score_label = tk.Label(self._root_window, font=("Helvetica", 13))
        self._score_label.pack(pady=5)
        self._update_score_label()

        instructions_label = tk.Label(
            self._root_window, text="Choose your move:", font=("Helvetica", 12)
        )
        instructions_label.pack(pady=10)

        buttons_frame = tk.Frame(self._root_window)
        buttons_frame.pack(pady=5)

        for move_name, move_label in move_emojis.items():
            move_button = tk.Button(
                buttons_frame,
                text=move_label,
                font=("Helvetica", 12),
                width=10,
                command=lambda chosen_move=move_name: self._play_round(chosen_move),
            )
            move_button.pack(side=tk.LEFT, padx=8)

        self._result_label = tk.Label(
            self._root_window, text="", font=("Helvetica", 13), wraplength=380, justify="center"
        )
        self._result_label.pack(pady=20)

        reset_button = tk.Button(
            self._root_window, text="Reset Scores", command=self._reset_scores
        )
        reset_button.pack(pady=5)

    def _update_score_label(self):
        self._score_label.config(
            text=(
                f"{self._human_player.player_name}: {self._human_player.score}   |   "
                f"{self._computer_player.player_name}: {self._computer_player.score}"
            )
        )

    def _play_round(self, chosen_move):
        human_move = self._human_player.get_move(chosen_move)
        computer_move = self._computer_player.get_move()

        winner_name = GameReferee.determine_winner(
            self._human_player, self._computer_player, human_move, computer_move
        )

        if winner_name == GameReferee.outcome_tie:
            result_text = "It's a TIE!"
        else:
            result_text = f"{winner_name} wins this round!"

        self._result_label.config(
            text=(
                f"You chose {move_emojis[human_move]}\n"
                f"Computer chose {move_emojis[computer_move]}\n\n"
                f"{result_text}"
            )
        )
        self._update_score_label()

    def _reset_scores(self):
        self._human_player.reset_score()
        self._computer_player.reset_score()
        self._result_label.config(text="")
        self._update_score_label()
        messagebox.showinfo("Scores Reset", "Scores have been reset to zero.")
