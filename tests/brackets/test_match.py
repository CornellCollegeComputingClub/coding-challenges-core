from coding_challenges_core.brackets.abc import Match
from pytest import mark

def test_get_placements_2():
    m = Match(0,0, ("a", "b"), [
        (1,0),
        (0,1),
        (0,1)
    ], None, False, True)
    assert m.wins_by_player == [2, 1]
    assert m.placements == ("a", "b")

def test_get_placements_tied_set():
    m = Match(0,0, ("a", "b"), [
        (0,1),
        (1,0),
        (0,0), # tied!
        (1,0)
    ], None, False, True)
    assert m.wins_by_player == [1, 2]
    assert m.placements == ("b", "a")

@mark.xfail(raises=NotImplementedError)
def test_get_placements_tied_entire():
    m = Match(0,0, ("a", "b"), [
        (0,1),
        (1,0),
        (0,0), # tied!
        (0,0), # tied!!
    ], None, False, True)
    assert m.wins_by_player == [1, 1]
    assert m.placements == ("b", "a")
