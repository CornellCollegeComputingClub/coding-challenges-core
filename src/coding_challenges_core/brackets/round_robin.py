from coding_challenges_core.brackets.abc import Bracket


class RoundRobinBracket(Bracket):
    """A round robin tournament bracket. Each player plays every other player exactly once."""
    def __init__(self, seeded_players, rng_seed):
        super().__init__(seeded_players, rng_seed)
