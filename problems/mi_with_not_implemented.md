
PB : multiple class inheriting a common parent class which raises NotImplemented errors in some of it's methods can't be properly used in MI.

```
class DAD:
    def method(self):
        raise NotImplementedError

class C1(DAD):
    def method(self):
        # operation C1

class C2(DAD):
    def method(self):
        # operation C2

class C3(DAD):
    def method(self):
        # operation C3

class C4(DAD):
    def method(self):
        # operation C4
```

```
class MIXER(C1, C2, C3, C4):
    def method(self):
        # would require multiple calls to super, or class.method, to visit all its parent methods
```

If we were to call super in any Cn class, it would make it impossible to use any instances of this class, as their call to method would now raise a NotImplementedError.

It is not possible to integrate those classes together while making use of super.
