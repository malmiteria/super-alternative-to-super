
class TestSuper:
    def test_from_A(self):
        from .super import A
        assert list(A().method()) == ['A', 'B', 'C']

    def test_from_B(self):
        from .super import B
        assert list(B().method()) == ['B']

    def test_from_C(self):
        from .super import C
        assert list(C().method()) == ['C']

class TestParent:
    def test_from_A(self):
        from .parent import A
        assert list(A().method()) == ['A', 'B', 'C']

    def test_from_B(self):
        from .parent import B
        assert list(B().method()) == ['B']

    def test_from_C(self):
        from .parent import C
        assert list(C().method()) == ['C']
