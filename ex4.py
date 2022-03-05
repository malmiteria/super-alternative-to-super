from parent import Parenting

class C(Parenting):
    def method(self):
        print(__class__)

class B(Parenting):
    def method(self):
        print(__class__)

class A(B,C):
    def method(self):
        print(__class__)
        A.__as_parent__(B, self).method()
        A.__as_parent__(C, self).method()

A().method()
