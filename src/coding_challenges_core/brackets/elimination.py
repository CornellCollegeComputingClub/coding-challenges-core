from coding_challenges_core.brackets.abc import Bracket


class SingleEliminationBracket(Bracket):
    """A single elimination tournament bracket. Players are eliminated after a single loss."""
    def __init__(self, seeded_players, rng_seed, consolation=False):
        super().__init__(seeded_players, rng_seed)
        self.__consolation = consolation

class DoubleEliminationBracket(Bracket):
    """A double elimination tournament bracket. Players are eliminated after two losses."""
    def __init__(self, seeded_players, rng_seed):
        super().__init__(seeded_players, rng_seed)


