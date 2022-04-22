
PB : when an attribute is inherited from multiple parent, the attribute from the second parent is silently ignored

```
class Dad:
    age = 100
class Mom:
    age = 50
class Son(Dad, Mom): pass
```


Son.age is 100, we are not informed that we ignored an attribute from class Mom

In case Mom and Dad are imported from a lib you, the author of Son, don't know, you might not realise you've introduced a bug.
