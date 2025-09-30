from coding_challenges_core.brackets.abc import Bracket


class SwissBracket(Bracket):
    """A Swiss tournament bracket. Players are paired based on their current scores, but never play the same opponent twice."""
    def __init__(self, seeded_players, rng_seed):
        super().__init__(seeded_players, rng_seed)
