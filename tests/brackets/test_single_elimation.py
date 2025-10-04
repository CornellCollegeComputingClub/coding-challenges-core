from coding_challenges_core.brackets.elimination import SingleEliminationBracket

def match_to_str(match):
    players = match.players if match.players is not None else ("TBD", "TBD")
    return f"R{match.round_num}M{match.match_num}: {players[0] or 'TBD'} vs {players[1] or 'TBD'}"

def matches_to_str(matches):
    return [match_to_str(match) for match in matches]

def test_gen_bracket_full_8():
    bracket = SingleEliminationBracket(
        seeded_players=["a", "b", "c", "d", "e", "f", "g", "h"],
        rng_seed=42
    )
    bracket._gen_bracket_full()
    bracket.prepare()
    matches = bracket._matches
    assert len(matches) == 7
    assert matches_to_str(matches) == [
        "R0M1: a vs h",
        "R0M2: d vs e",
        "R0M3: b vs g",
        "R0M4: c vs f",
        "R1M1: TBD vs TBD",
        "R1M2: TBD vs TBD",
        "R2M1: TBD vs TBD"
    ]

def test_gen_bracket_full_8_with_consolation():
    bracket = SingleEliminationBracket(
        seeded_players=["a", "b", "c", "d", "e", "f", "g", "h"],
        rng_seed=42,
        consolation=True
    )
    bracket._gen_bracket_full()
    bracket.prepare()
    matches = bracket._matches
    assert len(matches) == 8

def test_gen_bracket_full_7():
    bracket = SingleEliminationBracket(
        seeded_players=["a", "b", "c", "d", "e", "f", "g"],
        rng_seed=42
    )
    bracket._gen_bracket_full()
    bracket.prepare()
    matches = bracket._matches
    assert len(matches) == 6
    assert matches_to_str(matches) == [
        "R0M1: d vs e",
        "R0M2: b vs g",
        "R0M3: c vs f",
        "R1M1: a vs TBD",
        "R1M2: TBD vs TBD",
        "R2M1: TBD vs TBD"
    ]

