from abc import ABC, abstractmethod

class Player(ABC):
    valid_moves = ("rock", "paper", "scissors")

    def __init__(self, player_name):
        self._player_name = player_name
        self._score = 0

    @property
    def player_name(self):
        return self._player_name

    @property
    def score(self):
        return self._score

    def increment_score(self):
        self._score += 1

    def reset_score(self):
        self._score = 0

    @abstractmethod
    def get_move(self, chosen_move=None):
        raise NotImplementedError("Child classes must implement get_move().")

    def __str__(self):
        return f"{self._player_name} (Score: {self._score})"
