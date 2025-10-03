from coding_challenges_core.brackets.abc import Bracket, Match, SmallMatch
import math
import itertools
import functools

class SingleEliminationBracket(Bracket):
    """A single elimination tournament bracket. Players are eliminated after a single loss."""
    def __init__(self, seeded_players, rng_seed, consolation=False):
        super().__init__(seeded_players, rng_seed)
        self.__consolation = consolation
        self.__started = False
    
    def _gen_bracket_full(self):
        """Generate a full single elimination bracket with byes as needed."""
        matches = self._matches

        exponent = math.log2(len(self._seeded_players))
        remainder = round(2 ** exponent) % (2 ** math.floor(exponent))
        bracket = [1, 2] if exponent < 2 else [1, 4, 2, 3]
        for i in range(3, math.floor(exponent) + 1):
            j = 0
            while j < len(bracket):
                bracket.insert(j + 1, 2 ** i + 1 - bracket[j])
                j += 2
        
        current_round = 0
        if remainder != 0:
            for i in range(remainder):
                matches.append(Match(
                    round_num=current_round,
                    match_num=i+1,
                    players=None, # we'll fill this in later!
                    sets=[], # TODO: make this a defaultdict(list)?
                    advancements=None, # we'll fill this in later!
                ))
            current_round += 1

        match_exponent = math.floor(exponent) - 1
        iterated = False    
        while current_round < math.ceil(exponent):
            for i in range(2 ** match_exponent):
                matches.append(Match(
                    round_num=current_round,
                    match_num=i+1,
                    players=None, # we'll fill this in later!
                    sets=[], # TODO: make this a defaultdict(list)?
                    advancements=None, # we'll fill this in later!
                ))
            if not iterated:
                iterated = True
            else:
                for match in filter(lambda m: m.round_num == current_round - 1, matches):
                    match.advancements = (
                        SmallMatch(round_num=current_round, match_num=math.ceil(match.match_num / 2)),
                        None
                    )
            current_round += 1
            match_exponent -= 1
        
        start_round = 0 if remainder == 0 else 1
        for i, match in enumerate(filter(lambda m: m.round_num == start_round, matches)):
            match.players = (
                self._seeded_players[bracket[2*i] - 1],
                self._seeded_players[bracket[2*i + 1] - 1]
            )
        if remainder != 0:
            initial_round = tuple(filter(lambda m: m.round_num == 0, matches))
            counter = 0
            for match in filter(lambda m: m.round_num == 1, matches):
                assert match.players
                indexes = tuple(map(self._seeded_players.index, match.players))
                if indexes[0] >= math.pow(2, math.floor(exponent)) - remainder:
                    initial_match = initial_round[counter]
                    initial_match.players = (
                        match.players[0],
                        self._seeded_players[round(math.pow(2, math.ceil(exponent)) - indexes[0] - 1)]
                    )
                    initial_match.advancements = (
                        SmallMatch(round_num=current_round, match_num=math.ceil(initial_match.match_num / 2)),
                        None
                    )
                    match.players = (None, match.players[1]) # type: ignore
                    counter += 1
                if indexes[1] >= math.pow(2, math.floor(exponent)) - remainder:
                    initial_match = initial_round[counter]
                    initial_match.players = (
                        match.players[1], # type: ignore
                        self._seeded_players[round(math.pow(2, math.ceil(exponent)) - indexes[1] - 1)]
                    )
                    initial_match.advancements = (
                        SmallMatch(round_num=current_round, match_num=math.ceil(initial_match.match_num / 2)),
                        None
                    )
                    match.players = (match.players[0], None) # type: ignore
                    counter += 1
        if self.__consolation:
            last_round = max(matches, key=lambda m: m.round_num).round_num
            last_match = max(filter(lambda m: m.round_num == last_round, matches), key=lambda m: m.match_num).match_num
            matches.append(Match(
                round_num=last_round,
                match_num=last_match + 1,
                players=None,
                sets=[],
                advancements=None,
            ))
            # TODO: set lastRound-1 advancements to this match

class DoubleEliminationBracket(Bracket):
    """A double elimination tournament bracket. Players are eliminated after two losses."""
    def __init__(self, seeded_players, rng_seed):
        super().__init__(seeded_players, rng_seed)

if __name__ == "__main__":
    bracket = SingleEliminationBracket(
        seeded_players=["a", "b", "c", "d", "e", "f", "g", "h"],
        rng_seed=42
    )
    bracket._gen_bracket_full()
    bracket.prepare()
    matches = bracket._matches
    print(matches)
