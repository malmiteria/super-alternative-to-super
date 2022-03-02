
def test_super():
    from .super import A
    assert list(A().method()) == ['A', 'B']

def test_parent():
    from .parent import A
    assert list(A().method()) == ['A', 'B']
