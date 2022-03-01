from parent import parent, build_parenting_order

class C:
    def method(self):
        yield 'C'

class B:
    def method(self):
        yield 'B'

class A(B,C):
    def method(self):
        yield 'A'
        yield from parent(self, A, B).method()
        yield from parent(self, A, C).method()

print(list(A().method()))
print(build_parenting_order(A))
