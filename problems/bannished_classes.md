
PB : some class inheritance trees aren't permitted in python, due to C3 limitations.


```
class Reoc: pass
class Middle(Reoc): pass
class Bot(Reoc, Middle): pass # raises a TypeError
```
