from typing import Optional


def shuffle_seed(players: list, rng_seed: Optional[int] = None) -> list:
    """Shuffle a list of players with an optional random seed for reproducibility."""
    from random import Random
    rng = Random(rng_seed)
    shuffled_players = players[:]
    rng.shuffle(shuffled_players)
    return shuffled_players

def clamp_list(minimum: int, maximum: int, lst: list) -> list:
    """Clamp the size of the list to be within the given minimum and maximum values, keeping the front intact when possible. Will pad with None if the list is too short."""
    if len(lst) < minimum:
        return lst + [None] * (minimum - len(lst))
    return lst[:maximum]

def power_of_two(n: int) -> int:
    """Return the next power of two greater than or equal to n."""
    if n < 1:
        return 1
    power = 1
    while power < n:
        power *= 2
    return power

def linear(n: int) -> int:
    """A linear function that returns n.
    
    Really just here for symmetry with power_of_two, so function chains can be constructed easily.
    """
    return n
