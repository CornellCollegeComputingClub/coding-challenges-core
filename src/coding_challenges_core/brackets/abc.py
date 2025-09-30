from abc import ABC, abstractmethod
from random import Random
from typing import Optional
from dataclasses import dataclass

@dataclass
class Match:
    players: list[str]
    sets: list[tuple[int, ...]] # tuple - num = place (0-idx)
    
    @property
    def wins_by_player(self) -> list[int]:
        # tally up sets!
        wins = [0] * len(self.players)
        for set in self.sets:
            if set.count(0) > 1:
                # TODO: handle ties
                # for now, since this is wins, do nothing
                continue
            else:
                wins[set.index(0)] += 1
        return wins
    
    @property
    def placements(self) -> list[str]:
        """Returns an ordered list."""
        winners = self.players[:]
        wins_by_player = self.wins_by_player

        max_wins = max(wins_by_player)
        if wins_by_player.count(max_wins) > 1:
            # TODO: handle ties
            raise NotImplementedError

        def keyfn(player: str):
            idx = self.players.index(player)
            return wins_by_player[idx]
        winners.sort(key=keyfn, reverse=True)
        return winners

class Bracket(ABC):
    """Abstract base class for tournament brackets."""

    def __init__(self, seeded_players: list[str], rng_seed: Optional[int] = None):
        self.__seeded_players = seeded_players
        self.__rng = Random(rng_seed)
        self.__current_round = 0
        self.__rounds = {}
