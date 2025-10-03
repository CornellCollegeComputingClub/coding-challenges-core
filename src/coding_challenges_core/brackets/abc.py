from abc import ABC, abstractmethod
from random import Random
from typing import Optional
from dataclasses import dataclass

@dataclass
class SmallMatch:
    """A small match representing where a player can go next."""
    round_num: int
    match_num: int

@dataclass
class Match:
    round_num: int
    match_num: int
    players: Optional[tuple[str, ...]] # None if not yet determined
    sets: list[tuple[int, ...]] # tuple - num = place (0-idx)
    advancements: Optional[tuple[Optional[SmallMatch], ...]] # where each player goes next (None if eliminated). may be None if not yet determined (swiss)
    in_progress: bool = False
    complete: bool = False

    @property
    def wins_by_player(self) -> list[int]:
        # tally up sets!
        assert self.players is not None, "Players are not yet determined."
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
    def placements(self) -> tuple[str, ...]:
        """Returns an ordered list."""
        assert self.complete, "Match is not complete."
        assert self.players is not None, "Players are not yet determined."
        wins_by_player = self.wins_by_player

        max_wins = max(wins_by_player)
        if wins_by_player.count(max_wins) > 1:
            # TODO: handle ties
            raise NotImplementedError

        def keyfn(player: str):
            idx = self.players.index(player) # type: ignore # players is not None here due to assert
            return wins_by_player[idx]
        return tuple(sorted(self.players, key=keyfn, reverse=True))

class Bracket(ABC):
    """Abstract base class for tournament brackets."""

    def __init__(self, seeded_players: list[str], rng_seed: Optional[int] = None):
        self._seeded_players = seeded_players
        self._rng = Random(rng_seed)
        self.__started = False
        self._matches = [] # type: list[Match]
    
    def prepare(self):
        """Prepare the bracket for the tournament."""
        if self.__started:
            raise RuntimeError("Bracket has already started.")
        # self.__gen_bracket()
        self.__started = True
    
    def get_ready_matches(self, include_in_progress: bool = False) -> tuple[Match, ...]:
        """Returns a tuple of matches that are ready to be played (have all players assigned)."""
        if not self.__started:
            raise RuntimeError("Bracket has not been started. Call prepare() first.")
        
        def filter_fn(m: Match):
            # m.players is not None or m.players doen't contain None
            if m.players is None or any(p is None for p in m.players):
                return False
            # if m is not in progress or complete (i.e. hasn't been played yet)
            if include_in_progress:
                return not m.complete
            return not m.in_progress and not m.complete

        return tuple(filter(filter_fn, self._matches))
