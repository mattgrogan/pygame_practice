import pytest

from scroll2 import ReelStepper

def test_simple():
    steps = 100
    tgt = 40
    pos = 20

    rs = ReelStepper(total_steps=steps)
    rs.set_target(pos, tgt)
    assert rs.steps_remaining == 20

    s = rs.step(1)
    assert s == 1
    assert rs.steps_remaining == 19

    s = rs.step(19)
    assert s == 19
    assert rs.steps_remaining == 0

    with pytest.raises(ValueError):
        rs.step(1)

def test_complex():
    steps = 100
    tgt = 40
    pos = 80

    rs = ReelStepper(total_steps=steps)
    rs.set_target(pos, tgt)
    assert rs.steps_remaining == 60

    s = rs.step(10)
    assert s == 10
    assert rs.steps_remaining == 50

    s = rs.step(20)
    assert s == 20
    assert rs.steps_remaining == 30

    s = rs.step(50)
    assert s == 30
    assert rs.steps_remaining == 0

def test_revs():
    steps = 100
    tgt = 40
    pos = 80
    revs = 2

    rs = ReelStepper(total_steps=steps)
    rs.set_target(pos, tgt, revs)
    assert rs.steps_remaining == 260
