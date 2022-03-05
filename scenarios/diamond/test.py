
class TestSuper:
    def test_from_A(self):
        from .super import A
        assert list(A().method()) == ['A', 'B', 'C', 'D']

    def test_from_B(self):
        from .super import B
        assert list(B().method()) == ['B', 'D']

    def test_from_C(self):
        from .super import C
        assert list(C().method()) == ['C', 'D']

    def test_from_D(self):
        from .super import D
        assert list(D().method()) == ['D']


class TestParent:
    def test_from_A(self):
        from .parent import A
        assert list(A().method()) == ['A', 'B', 'D', 'C', 'D']

    def test_from_B(self):
        from .parent import B
        assert list(B().method()) == ['B', 'D']

    def test_from_C(self):
        from .parent import C
        assert list(C().method()) == ['C', 'D']

    def test_from_D(self):
        from .parent import D
        assert list(D().method()) == ['D']
