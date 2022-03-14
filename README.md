Motivation :
the super builtin works in misterious ways, this projects attempts at crafting a better solution.

The problems :
 - In case of multiple inheritance, super would not always point to the direct parent
 - the MRO (method resolution order) algorithm, doesn't match the zen of python's guidelines, mainly :
   - errors shouldn't pass silently
   - explicit is better than implicit


A little explanation

1. What is MRO:

Inheritance implies that a child class would inherit parent methods. For example
```
class B:
    def method(self):
        print('B')
class A(B):
    pass

A().method() # prints B
```

In case of multiple inheritance, such as : 
```
class C:
    def method(self):
        print('C')
class B:
    def method(self):
        print('B')
class A(B,C):
    pass
```
It is unclear what ```A().method()``` should print.

Or in other term, there is a conflict between the parents method when a child instance tries to inherit a method that both parent seem to have.

The MRO algorithm comes as a solution to this problem, by linearising the inheritance trees, which in term allows to resolve the method of instance A as the method of the first parent in MRO order capable to deliver this method.

This linearisation comes with a few meaningful rules, such as:
 - child < parent
 - parent_to_the_left < parent_to_the_right
 - no duplicates

I do not know if there are more rules into MRO.

This also means that some inheritance trees are not allowed, such as:
```
class X:
    pass
class Y:
    pass
class A(X,Y): # X < Y
    pass
class B(Y,X): # Y < X
    pass
class Problem(A,B): # X < Y AND Y < X, can't resolve MRO, raise a TypeError and refuses to create the class
    pass
```

In python, MRO is used to resolve attributes too.

If you are curious to know what the mro of a class is, just print ```<the_class_you're_curious_about>.__mro__```

2. What is super

super is a builtin method that acts as a proxy that can be used (not exclusively) when a child class wants to access it's parent class context.

The most common use is in case of inheritance, when the child class extends a parent method:
```
class B:
    def method(self):
        print('B')
class A(B):
    def method(self):
        print('A')
        super().method()

A().method() # prints A then prints B
```

In case of multiple inheritance, super visits the next class in line:
```
class C:
    def method(self):
        print('C')
class B:
    def method(self):
        print('B')
class A(B,C):
    def method(self):
        print('A')
        super().method()

A().method() # prints A then prints B (and never prints C)
```

in this exemple, if you want `A().method()` to print A B C using `super`, you have two options, both are not reliable:
option 1, which is consistent with the argumentless syntax of `super`, but make it impossible to use B().method() as it now would raise an error.:
```
class C:
    def method(self):
        print('C')
class B:
    def method(self):
        print('B')
        super().method() # HERE
class A(B,C):
    def method(self):
        print('A')
        super().method()
```
option 2, which would still allow `B().method()` to run properly, but some inheritance trees including A could fail:
```
class C:
    def method(self):
        print('C')
class B:
    def method(self):
        print('B')
class A(B,C):
    def method(self):
        print('A')
        super().method()
        super(B, self).method() # HERE
class D(B):
    def method(self):
        print('D')
class E(A,D):
    def method(self):
        print('E')
        super().method()
        super(A, self).method()

E().method() # prints E A D C D (despite E.__mro__ presenting no duplicates, and A B C order is lost)
```

3. The flaws

The mro as it stands is flawed in four ways in my opinion:
 - the order in which parents of a class A are visited isn't reliable, and can be altered by A's childs, despite the fact that A's definition doesn't involve A's child at all. It is not possible to garantee any mro will be preserved in any context.
 - The mro hides what really should be an error by trying to solve it, and refuses developper the opportunity solve it case by case, when it would emerge
 - the mro can't solve the problem it pretends to in all context, and then assumes the error to be too critical to allow developpers to plug in their solutions. (mro failure leads to class definition being not allowed)
 - it doesn't allows for duplicates, assuming that no one would want that.

`super()` as it stands is flawed in two ways in my opinion:
 - it relies on mro, so it brings in all mro flaws with it
 - it adds a level of indirection by giving the context of the next in mro line instead of the context of the class passed as argument : ```super(A, self)``` is a proxy to the parent of A, not of A.


4. The good parts

The mro is a solution to a possible conflict between multiple parents methods. As much as i would prefer the error to not be silenced, a solution should still be provided.
It works very well for simple cases, and any other solutions should probably do as well on those simple cases.

`super()` acts as a proxy to the class it points to, meaning we don't have to pass the instance as first argument of any method accessed through super.


5. what would be an ideal solution

I think it can be boiled down to those features
 - *straightforward case* : when a class "A" has a method "method", no matter if A has any parents, `A().method` should resolve to the method "method" of class "A"
 - *can't be found* : when a class A *doesn't* have a method "method", and *all* it's parent raise a "MethodDoesNotExist" error, `A().method` should raise a "MethodDoesNotExist" error.
 - *only one parent has it* : when a class "A" *doesn't* have a method "method", inherits from class "B" which can resolve a method "method", and also inherits from 0 to n other classes, *all* of which raising a "MethodDoesNotExist" error when looking for the method "method", `A().method` should resolve to the method "method" of class "B"
 - *multiple parents have it* : when a class "A" *doesn't* have a method "method", and inherits from multiple parent, at least two of which can resolve a method "method", `A().method` should raise a `ConcurentMethodResolutionError`, stating that explicit inheritance order is required
 - *transmitting errors* : when a class "A" *doesn't* have a method "method", if any parent raises a `ConcurentMethodResolutionError`, `A().method` should raise a `ConcurentMethodResolutionError`

Any `ConcurentMethodResolutionError` on method "method" of class "A"could then be solved by adding the method "method" in class "A".
Obviously, inside the definition of this method, it should be possible to point to one of the parents method, or multiple.
Such a feature could be accomplished by a method as such:
```
def __as_parent__(self, parent_class):
    #return the same kind of proxy super does, on class parent_class
```
