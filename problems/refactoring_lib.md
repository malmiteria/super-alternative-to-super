
PB : As a library author, refactoring multiple class you provide to your users by extracting a common parent and the inverse refactoring are breaking change.

### EXTRACT PARENT CLASS
BEFORE REFACTO:
lib :
```
class A:
    def method(self):
        # operation O
        # operation A

class B:
    def method(self):
        # operation O
        # operation B
```

user :
```
class C(A, B):
    def method(self):
        super().method()
        # operation C

C().method() does operation O, A, and C
```

AFTER REFACTO:
lib :
```
class O:
    def method(self):
        # operation O

class A(O):
    def method(self):
        super().method()
        # operation A

class B(0):
    def method(self):
        super().method()
        # operation B
```

user : (unchanged)
```
class C(A, B):
    def method(self):
        super()
        # operation C

C().method() does operation O, B, A, and C (changed behavior, despite no change in code)
```


As you can see, the user's code's behavior changed, from operations O, A, C, to operations O, B, A ,C, despite the user's code not changing at all.

The opposite refactoring will produce the opposite change in the user's code.
