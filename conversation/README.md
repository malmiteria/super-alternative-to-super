
current state of MRO + super is being used in multiple ways.
No explicit feature is isolated for any of those use cases.

Let's list those feature. I'll dive in more depth about illustrating them, and my thoughts about them later.

feature 1 (of super alone): proxying the parent.
What most people think super does (and expect it to do):
it allows to call method from *the* (most people don't think of multiple inheritance) parent.
It can be used by working around MRO to proxy any parent directly.
I'd argue this isn't reliable, which makes it an incomplete feature, but that's still a use made of super
If i had to specify only one problem i have with super today :
 it's use in simple inheritance hints at a behavior of super, which turns out to be widely different from its actual behavior.
 a feature more consistent on that regard would make the langage much easier to learn, for everyone.

feature 2 (of super + MRO): sideway specialization / mixins
It however can jump sideways in the inheritance tree.
allowing for same level class to still specialize one another.
For this scenario, today, we rely on the order in which class are inherited.
This is usefull when for some reason it is not possible to make a class inherit from another at definition time.

feature 3 (of super + MRO): dependency injection / inheritance tree alteration
If you wanna inject a class wherever in some pre existing class inheritance tree, you can through the use of some clever new classes.
If you wanna deny its parent to one class, and essentially prune of branch off the inheritance tree, you can too.

feature 4 (of MRO alone): method resolution
when trying to resolve a method / attribute of a class, if not present in its definition, looks up the parent(s) to come up with an answer.
If no parent can resolve it, you get the attribute error, if at least one does, you get it.
I'd argue that it makes it possible to silently ignore a parent method when multiple parent define such a method. Which makes it especially painfull to debug those scenarios, which makes it an incomplete feature.
On top of that, it renders some class definition invalid, when really, the method resolution shouldn't break more than the method resolution. This should be a gettribute error, not a class definition error.


"feature" 5 : diamond problem.
Not really a feature, more a lack of feature. Today's diamond problem is solved by making the top layer appear only once in scpecialisation, which is a direct consequence of ordering the inheritance tree. Whatever changes we decide on the 4 previous features, the impact on the diamond problem will either be null, or make the top layer be specialsed by all it's chilren. Either strategies aren't covering all needs. This requires an extra dedicated feature.

Also, as mentionned, i'd argue that some of those feature aren't fully delivering what they promise.
Essentially, they compromise for the extra feature, which in the context of a lack of properly isolated implementation for those feature seems fair.



# Why am i here?

What motivated me first here was the few problems with the feature 1 (proxying the parent) and feature 4 (method resolution) which I consider to be suboptimal.
Of course, the different use cases made out of the current super + MRO should be preserved.
Essentially, I do *not* intend to lose any strength / any use case of the langage
Listing all the use cases made out of current super + MRO matters then. And I think i already cover the most important ones with the 4 features i described.
If you feel I'm missing something, please let me know.

## My goal :
essentially, producing features for parent proxying and method resolution that wouldn't exhibit the flaws of their current version is my goal.
I also (of course) wanna preserve all current use case made out of the current version.
Since MRO is the base building block on which super relies, and MRO + super are the bases for those extra feature, it follows that I need to provide alternative for those feature.
Those changes would be massive, and require a lot of effort / time to make their ways into python, so it also matters to take this into consideration, at some point.
As much as possible, I don't wanna change the external behavior / API of the code. If my alternative looks the same, it should behave the same. If it behaves the same, it should look the same. Some amount of changes are needed of course, but my goal is to make it an easy transition, as much as possible.


Breaking changes?

feature 1 (proxying the parents)
  Any alternative that don't rely on MRO is bound to make the other features break, so I guess there's no way out this being a breaking change, if not for spreading alternative not reliant on MRO for those other extra features. But it would be possible to have a non breaking change that introduce the alternatives feature 2 and 3, followed after transition of code to those feature by another non breaking change of this feature 1, which would help the migration. However, unmigrated features 2 and 3 are bound to break.

feature 2 (sideway specialization) 
  Introducing an alternative without removing the old ways of doing things won't be a breaking change. This could be published in a first batch, with time to let every new commers learn to use it, and old timers switch to it. It would obviously need to be robust enough to suit everyones need, but that's only a matter of designing the feature.
  Removing the current version of this feature would come from removing / drasitcally change MRO + super current behavior, and can't really be done without such a change, so I'd say that feature 2 new alternative can be done without breaking change.
  Feature 1 breaking change would also break the current version of feature 2

feature 3 (dependency injection / inheritance tree alteration) :
  Same as for feature 2.

feature 4 (method resolution)
  Any alternative to it is bound to breaking changes, since MRO is so tightly coupled with feature 1 2 3.
  Those features alternative should come first. If possible, let's limit it to one breaking change total :p
  Once the alternatives to feature 2 and 3 are here, an alternative to feature 1 can be produced, without removing the current version of feature 1 2 and 3.
  unlike for feature 1 2 and 3, I don't think it's possible to produce an alternative to feature 4 without replacing it. I might be wrong tho, at least for part of the feature.

Essentially : produce alternatives to feature 1 2 and 3 (most urgently 2 and 3) without removing the current version of those feature, then the alternative to feature 4 can be done, which would be the *only* breaking change 


# code examples:

## diamond tree, repeat top
CONTEXT : This exemple makes use of today's features.
No replacement feature is used there
The goal is to showcase today's behavior, and add my remarks.

```
class HighGobelin:
    def scream(self):
        print("raAaaaAar")

class CorruptedGobelin(HighGobelin):
    def scream(self):
        print("my corrupted soul makes me wanna scream")
        super().scream()

class ProudGobelin(HighGobelin):
    def scream(self):
        print("I ... can't ... contain my scream!")
        super().scream()


class HalfBreed(ProudGobelin, CorrupteGobelin):
    def scream(self):
        # 50% chance to call ProudGobelin scream, 50% chance to call CorruptedGobelin scream
```

when writing down the class HalfBreed, we expect the behavior of HalfBreed().scream() to be one of its parent behavior, selected at random with 50% chance each.
with the use of super, it could look like that, intuitively


```
class HalfBreed(ProudGobelin, CorrupteGobelin):
    def scream(self):
        if random.choices([True, False]):
            super(HalfBreed, self).scream()
        else:
            super(ProudGobelin, self).scream()
```
However, super(HalfBreed, self) does not deliver ProudGoeblin behavior, but a mix of ProudGobelin, CorrupteGobelin, and HighGobelinBehavior.

We would expect the output to be : 

"I ... can't ... contain my scream!"
"raAaaaAar"

But it is :

"I ... can't ... contain my scream!"
"my corrupted soul makes me wanna scream"
"raAaaaAar"

Getting the correct behavior requires to let go of super, in such a way:


```
class HalfBreed(ProudGobelin, CorrupteGobelin):
    def scream(self):
        if random.choices([True, False]):
            ProudGobelin.scream(self)
        else:
            CorrupteGobelin.scream(self)
```

Which is an option multiple of you pointed out to me.
This options however is flawed in muliple ways, mainly because it looses 3 of the 4 features i describe earlier.
 - we lose the proxy feature, which to be fair, is aqueen to syntactic sugar. But this is still a feature loss.
 - we lose the sideway specialisation, coming from super's behavior, which, in this case, is the goal, so we're not complaining.
 - we lose the possibility of class dependency injection, since today, it relies on a consistent use of super.

As some of you mentionned (with pain and agony, for some of you ;) ), loss of feature is a big problem. I think at least for this scenario, assuming that we indeed managed to produce an alternative to all those feature, we are gaining the feature you are defending, not losing it.

## Can't assume on parent's more specialised.
CONTEXT : This exemple makes use of today's features.
No replacement feature is used there
The goal is to showcase today's behavior, and add my remarks.

```
class Glider:
    def push(self)
        print("I can't move so good on the ground")

    def jump(self):
        print("I'm free! I can fly now!")

class Wheel:
    def push(self)
        print("let's roll !")

    def jump(self):
        print("oh damn, i'm falling fast!")

class WheelGlider(Wheel, Glider):
    def push(self):
        # calls Wheel push method first
        # calls Glider push method second

    def jump(self):
        # calls Glider push method first
        # calls Wheel push method second
```

In this example, we expect WheelGlider push method to output :
"let's roll !"
"I can't move so good on the ground"

and we expect WheelGlider jump method to output :
"I'm free! I can fly now!"
"oh damn, i'm falling fast!"


this could be achieved in such a way:
```
class WheelGlider(Wheel, Glider):
    def push(self):
        super().push()
        super(Wheel, self).push()

    def jump(self):
        super(Wheel, self).jump()
        super().jump()
```

This raises a lot of questions
 - how do those jump and push method behave in case Wheel and Glider are refactored to inherit from a parent?
   - If this refactoring introduces the diamond case, we're back at the problem showcased in the diamond tree example
   - If no diamond case (no parent is shared by both, no matter how deep in the inheritance tree), then it would behave consistently with what's expected now.
 - How do those jump and push method behave in case WheelGlider is used as a parent of another class, which might or might not inherit from Wheel or Glider?
 - The API here is suboptimal, to say the least, since we have to pass arguments to super that will then be processed for us to reach our target. super(Wheel, self) proxies Glider, which is far from being obvious.
 - How does one uses all the features of super + MRO here? I don't see a case where you'd want sideway specialisation in this scenario, but it doesn't mean it wouldn't happen. But what about dependency injection / inheritance tree alteration?

Let's investigate :
Let's say you wanna make use of dependency injection to mock WheelGlider parents in a unit test setting.
The way to reach this goal today is simple, make use of super "weird" behavior in diamond scenario cases to inject your class in the middle.

```
class MockedWheel(Wheel):
    def push(self):
        print("mocked wheel push")
    def jump(self):
        print("mocked wheel jump")

class MockedGlider(Glider):
    def push(self):
        print("mocked glider push")
    def jump(self):
        print("mocked glider jump")

class MockedWheelGlider(WheelGlider, MockedWheel, MockedGlider):
d    def push(self):
        print("mocked WG push")
        super().push()
    def jump(self):
        print("mocked WG jump")
        super().jump()
```

To get some bird eye view of this inheritance tree, we know MRO will order it like that:
(1) MockedWheelGlider < WheelGlider < MockedWheel < MockedGlider
(2) WheelGlider < Wheel < Glider
(3) MockedWheel < Wheel
(4) MockedGlider < Glider

after a quick sandbox test, the complete mro is:
MockedWheelGlider < WheelGlider < MockedWheel < Wheel < MockedGlider < Glider (< object)

This happens to work fine:
```
MockedWheelGlider.jump() # prints "mocked WG jump", then "mocked glider jump", then "mocked wheel jump"
MockedWheelGlider.push() # prints "mocked WG push", then "mocked wheel push", then "mocked glider push"
```

If one of the super were replaced by the class.method approach, the MockedWheelGlider would fail to fully mock Wheel and Glider.
But as far as i'm concerned, this feature is quite robust in this scenario (when super is consistently used).

For deeper inheritance tree alteration, such as removing a branch (can be done by messing with __bases__), they could break some super calls (which is to be expected anyways)

Other than that, I would argue that for the sake of symetry, it would probably be preferable for super to allow / disallow the exact same API for the use of super, no matter the parent it targets.
Since in this scenario, we explicitely *don't* think of one parent as coming after the other (in term of specialisation, that is), it shows a disconnect between the feature and its use. Which i take as a hint that there is a feature to produce to match this need more accurately.


## Way too big combinatory possibilities
CONTEXT : This exemple makes use of today's features.
No replacement feature is used there
The goal is to showcase today's behavior, and add my remarks.

let's say you're making a web framework.

You might wanna provide a few View classes:

```
class View:
    def render(self):
        # does some generic view stuff
        print("view")
class ListView(View):
    def render(self):
        # does some list view specific stuff
        print("list view")
        super().render()
class FormView(View):
    def render(self):
        # does some form view specific stuff
        print("list view")
        super().render()
```

That's just an example, but you might get more of those View classes depending on the scenarios you wanna cover

You might also end up providing more features, that relate to the View, such as a LoginRequiredMixin, and a PermissionMixin
```
class LoginRequiredMixin:
    def render(self):
        # does login specific stuff
        super().render() # notice the call to super, despite the class not having parents

class PermissionMixin:
    def render(self):
        # does permission specific stuff
        super().render() # notice the call to super, despite the class not having parents
```

Again, those are just examples, you might end up needing more of those mixins.

Now, each View class would benefit from a variant with the permission mixin's behavior, a variant with the login required mixin, and a variant with both.
Add more mixins, and the combinatory explodes. And you'd want to produce all those classes variant for each View classes.

The "proper" way to produce those variant would be through inheritance. After all, those variant are simply "more specialised" variants of the base class.
In order to do it, you would have to produce a LoginRequiredView which inherit from View, a PermissionView inheriting from View, and a LoginRequiredPermissionView which would maybe inherit from PermissionView?

But the problem would then be, how do you not repeat yourself a million time, writting down the login specialisation code in each variant that requires it?
You can't really, if you wanna stick with inheritance at this stage.


However, the use of mixin, such as describe in the code blocks allows a DRY approach, if used correctly by whoever integrates those classes later on.

For an end user, such an integration could look like:

```
class MyView(LoginRequiredMixin, PermissionMixin, View):
    # would call render in some appropriate method, but not necesserly redefine it.
```

which would provide the expected behavior, with no need for the framework editor to produce all the possible combination, and allows for a DRY approach.


Essentially tho, this is a use case of multiple inheritance to provide the behavior of what really could have been simple inheritance.

The inheritance tree in this scenario is:

Login    Permission    View

     \        |       /

           MyView

When it fact it was meant to be

View
  |
Permission
  |
Login
  |
MyView


The practical reason is valid however, it is to me a symptom of a missing feature.

Turns out it is not possible today (or at least, not properly integrated in the langage) for a class to be defined without knowing its parent, and later on to be attributed parents.
It is also not possible to define deep layers of it's inheritance tree when defining it.
I'll be making a proposal for that later on.




# Let's talk about the features

## Proxying the parent
CONTEXT : I'm talking here *exclusively* about the parent proxying feature.
I will talk about the other features on their dedicated sections.
I'm describing the current state of this feature, to the best of my understanding.
I'll also add my remarks on what we would wanna keep / get rid of for an optimal feature.
But i am not at this point proposing an alternative.


This feature allows to proxy a class, which render it's method (and attributes to some extent) accessible from the parent to the child, "as" the parent.

```
class Dad:
    def say_hi(self):
        print("Good morning")

class Child(Dad):
    def say_hi(self):
        print("....")
        super().say_hi("Good morning")
```

This is a way to access the parent method as if through an instance of it.

It is made to be used inside class method definitions, more than anything else, but can be used to define child attribute based on parent attributes.

```
class Dad:
    age = 100

class Son(Dad):
    # super().age fails with a RuntimeError (no argument)
    # super(Son, Son) fails here with a NameError (Son is not defined yet)
    pass

Son.age = super(Son, Son).age - 30
```

The 'syntactic sugar' aspect of super's proxying feature is that calls to parent methods through super don't require to pass the instance as first argument, which makes for less redundant code. This should be kept in the alternative feature.

There is a 'disconnect' between the argument passed to super (when needed) and the class it will target to be a proxy of.
super(Son) is not a proxy of class Son, it is a proxy on the next in MRO (it feels redundant saying MRO order, but weird just saying in MRO ...) So in cases where the automatic solve of the argumentless super doesn't suits our needs, such as in the exemples above, there is some mental gymnastic, and knowledge to be known to reach our goal. This should be simplified in the alternative feature.

The possiblity of calling super with no argument is quite handy, and should probably be kept too.

In case of multiple inheritence, the argumentless expression of super does lack explicitness to me. I would wanna make the use of the alternative more explicit, in this scenario.

TLDR:
 - keep :
  - syntactic sugar
  - argumentless option in case of simple inheritance
 - don't keep:
  - argument and proxy target being not the same
  - argumentless syntax in multiple inheritance


## Sideway specialisation / Mixins
CONTEXT : I'm talking here *exclusively* about the sideway specialisation / mixin feature.
I will talk about the other features on their dedicated sections.
I'm describing the current state of this feature, to the best of my understanding.
I'll also add my remarks on what we would wanna keep / get rid of for an optimal feature.
But i am not at this point proposing an alternative.


Today, it is possible to have a class designed to inherite from another, but without having it explicitely inherit from it, when defined.

This is useful in case the specialistion class should be applied to multiple base class, especially when more specialisation classes exists, and all combination of the specialisations should be provided.
This is showcased in the "way too many combinatory" exemple i gave earlier.

If you have those base classes :
```
class View1:
    def render(self):
        # ...

...

class View10:
    def render(self):
        # ...
```

And those specilaser mixins:
```
class Spec1:
    def render(self):
        # ...
        super().render()
        # ...

...


class Spec10:
    def render(self):
        # ...
        super().render()
        # ...
```

The amount of combination is insanely huge, something like, if i'm not mistaken:

for n in range(amount of spec):
    (amount of views) * [(amount of specs)!/(n!)]

which in this case gives 62353000
Anyone attempting to manually do that would be insane. Obviouly, it's rare to have 10 specs, but the number is still high with 3 specs : 90
More accessible, but definitely not a fun task

How is it done then? Through multiple inheritance.
```
class MyView(Spec1, Spec4, View3):
    pass
```
is a class that inherits from what would have been the combination Spec1 inherits from Spec4 inherits from View3, would it have been possible to define such inheritance between the specs and view.
Since MRO in this case is MyView < Spec1 < Spec4 < View3, any call to super from Spec1 will proxy Spec4, and any call to super from Spec4 will proxy View3.


Today's super allows to provide all those combinations, without having to explicitely define any combination
This feature is a must keep

I would argue tho, that today's solution produces a multiple inheritance tree, when all it need in fact is a simple inheritance tree.
It essentially "forget" about the inheritance it meant to provide, but falls back into working thanks to the ability of super to side jump.
An alternative would probably benefit from rendering the inheritance feature explicit. Today, those scenarios are simply denying the inheritance they really meant to benefit from. Let's make them actual inheritance.

I would also argue that multiple the inheritance syntax is definitely not appropriate, as it is very not clearly keeping track of the order of classes the child inherits from.
I've seen people try to reorder the classes in such a scenario, because it was weird to them to have mixins come after the view class. Which is the most important one, so they felt it made sense to have it placed first. Of course our automated tests made it clear it wasn't working, but it also means that had we not have tests, testing the mixin features, we would have silently lost this feature.
And testing those feature was debated in our team, since those are essentially the web framework responsibility, not ours.
I can see this bug reaching production for this reason.
As much as this is an UX consideration, this is definitely a must get rid of. An alternative should be designed to make it clear there is an order.

TLDR:
 - keep:
  - Not having to explicitely define all combinations of (n) mixins + feature class
 - don't keep:
  - Loss of simple inheritance when it's the dedicated feature for this need
  - Current UX for this scenario lack of explicit order


## Dependency injection / inheritance tree alteration
CONTEXT : I'm talking here *exclusively* about the dependency injection / inheritance tree alteration feature.
I will talk about the other features on their dedicated sections.
I'm describing the current state of this feature, to the best of my understanding.
I'll also add my remarks on what we would wanna keep / get rid of for an optimal feature.
But i am not at this point proposing an alternative.


Today's MRO + super allows for dependency injection.
Let's take the "Can't assume on parent's more specialised." example:
```
class Glider:
    def push(self)
        print("I can't move so good on the ground")

    def jump(self):
        print("I'm free! I can fly now!")

class Wheel:
    def push(self)
        print("let's roll !")

    def jump(self):
        print("oh damn, i'm falling fast!")

class WheelGlider(Wheel, Glider):
    def push(self):
        super().push()
        super(Wheel, self).push()

    def jump(self):
        super(Wheel, self).jump()
        super().jump()
```

MRO for WheelGlider here is : WheelGlider < Wheel < Glider

This order will never change, however, it is possible to squeeze between any two consecutively ordered classes by making use of a good understanding of MRO:

MockedWheelGlider < WheelGlider < MockedWheel < Wheel < MockedGlider < Glider
implies:
WheelGlider < Wheel < Glider

This new order can be obtained with:
```
class MockedWheel(Wheel):
    def push(self):
        print("mocked wheel push")
    def jump(self):
        print("mocked wheel jump")

class MockedGlider(Glider):
    def push(self):
        print("mocked glider push")
    def jump(self):
        print("mocked glider jump")

class MockedWheelGlider(WheelGlider, MockedWheel, MockedGlider):
d    def push(self):
        print("mocked WG push")
        super().push()
    def jump(self):
        print("mocked WG jump")
        super().jump()
```

This features essentially allows to reparent any class, anywhere in any inheritance tree, this is definitely a must keep.

I would argue that, as much as this feature is very reliable today, it relies on super and MRO which don't always cover developpers needs. Today's alternative class.method does most definitely not allow for proper dependency injection, as super calls implictely target the next in MRO, and class.method are hardcoded to target the same method no matter MRO, so the dependency injection dependance on super and MRO is a downfall of this feature.

This feature also requires to create a new class, inheriting from the class to inject dependency on, meaning it is not an inplace change.This should probably be kept like that. Although, i guess it doesn't hurt to give the option to the developper to have the change inplace or not.

The current state of this feature UX is quite poor tho, as the amount of knowledge you have to pour into the code to make it work like you'd expect is quite high. Making this feature not accessible to most developpers. The alternative would most definitely benefit from a simpler API.

On the topic of the link between dependency injection and super + MRO, it is important to note that any slight change on MRO + super could have an impact on this feature, essentially locking super and MRO in their current state.

TLDR:
 - keep:
  - the ability to reparent any class anywhere in any inheritance tree.
  - the not inplace change.
 - don't keep:
  - the reliance on super + MRO
  - the amount of knowledge needed to make use of this feature


## Method resolution
CONTEXT : I'm talking here *exclusively* about the method resolution feature.
I will talk about the other features on their dedicated sections.
I'm describing the current state of this feature, to the best of my understanding.
I'll also add my remarks on what we would wanna keep / get rid of for an optimal feature.
But i am not at this point proposing an alternative.


Method resolution is the feature that allow child class to access parent method as if it was their own, assuming they do not override it with a method with the same name.
```
class Dad:
    def joke(self):
        print("I'm afraid for the calendar. Its days are numbered.")

class Son(Dad):
    pass
```
In this exemple ```Son().joke()``` will resolve to joke method defined in Dad

However:
```
class Dad:
    def joke(self):
        print("I'm afraid for the calendar. Its days are numbered.")

class Son(Dad):
    def joke(self):
        print("*UNO reverse card sound* Hi dad, I'm son.")
```
In this exemple ```Son().joke()``` will resolve to the joke method defined in Son
Had Dad not have a joke method, an AttributeError would have been raised

In case of multiple inheritance, we still want the child to be able to inherit its parent methods.
```
class Dad:
    def joke(self):
        print("I'm afraid for the calendar. Its days are numbered.")

class Mom:
    def joke(self):
        print("What do you call a small mom? Minimum.")

class Son(Dad, Mom):
    pass
```
In this exemple the use of a method resolution *order* comes into play. Since multiple parent have a joke method to provide, and Son method resolution can only resolve to one of them, it is resolved to the first in order capable of delivering the method.
Here, ```Son().joke()``` resolves to the joke method of Dad.
Had Mom not have a joke method, nothing would change.
Had Dad not have a joke method, ```Son().joke()``` would have resolved to the joke method of Mom.
Had both Mom and Dad not have a joke method, an AttributeError would have been raised

Method resolution is also applied to class attributes. Essentially, a method bound class can be considered a callable attribute of this class, there's no specification of non callable attributes that would make them not need a method resolution algorithm.


I would argue that it is less than optimal that one parent method can be silently ignored by the method resolution on the pretext that another parent had a method with the same name "before". In some case, as the mixin case, such an order matches the need, but in the generic case, it is too speicifc of an assumption.

The ability for the child to resolve its parent method should be kept in, obviously (that's what inheritance is in the end)
However in case of multiple inheritance, and maybe more specifically, multiple resolution, a "manual" merge in the child class definition should be requested.
This goes for method and attributes, as of today, it is assumed one method is prefered, but other strategies might be the more viable ones. This assumption is something i disagree with. We should allow for multiple strategy, instead of enforcing one, and request a strategy when the default one can't provide a result.

The ability for the child to resolve automatically one of its parent method when only one parent can provide it is a viable default method, and should be kept as the default one, in this scenario.

Today's MRO doesn't allow for all possible class inheritance trees, as some can't be ordered, or would have inconsistent order.
such as :
```
class A: pass
class B(A): pass # B < A
class C(A,B): pass # A > B
```

TLDR:
 - keep:
  - resolution on class body method first
  - resolution implicit on parent method (if not present in own class body) when only one parent has it
 - don't keep
  - implicit resolution when multiple parent can resolve it
  - assumption of an order of parents. One might be more specialised than the other, but does not have to.


## Diamond problem

The diamond problem is essentially the question, should methods from a class which appears multiple time in an inheritance tree be called multiple time, or only once.
Essentially, multiple answers are possible, depending on your specific needs.
You might wanna want the bottom class inherit from the full behavior of all of it's parent classes, in which case, you'd call the grandparent method each time.
You might also want the grandparent class method to be called only once, after all other specialisation provided by all the parents.

Today, the only option provided by super + MRO is or the grandparent to be called only once.

I'd argue this is not enough.
We should be able to chose the strategy ourself, depending on our needs.

The diamond problem illustrate the problem when a class appears multiple time in an inheritance tree, but this shape doesn't have to be diamond.

For example:
```
class Top: pass

class Side(Top): pass

class Bottom(Side, Top): pass
```

TLDR:
allow for multiple inheritance strategies, instead of enforcing one.


## the weird case of __slots__
Someone mentionned __slots__

I didn't consider it at first, and now i'm weirded out by it.
(I'm running those exemples in python 3.6, according to more probing on my part, __slots__ behaves differently on python 2.7)

```
class A:
    __slots__ = ['a']
class B:
    __slots__ = ['b']
class C(B,A): pass
```
This code raises an error:
TypeError: multiple bases have instance lay-out conflict

Turns out, C doesn't like that A and B both define __slots__
So, my intuition was that redefining __slots__ in C would fix the issue
```
class A:
    __slots__ = ['a']
class B:
    __slots__ = ['b']
class C(B,A):
    __slots__ = ['c']
```
This raises the exact same error.

Multiple inheritance works for __slots__, at the strict condition that only one parent defines __slots__:
```
class A:
    pass
class B:
    __slots__ = ['b']
class C(B,A):
    pass
```
This doesn't raise an error.

Essentially, it seems the default method resolution, when applied to this __slots__ attribute wasn't satisfactory to whoever built it. They then decided to change the method resolution on this method to not allow implicit method resolution for multiple inheritance.
But, somehow, redefining __slots__ in the child isn't allowed either. Which should be an option to allows proper method resolution here.

In case of simple inheritance, more strange behavior occur.

```
class A: __slots__ = ['A']
class B(A): __slots__ = ['B']
```

This works, and now, B.__slots__ is equal to ['B']. Over riding works in this case.

I'm assuming this feature is still evolving, and testing in higher version of python would lead to different behaviors.

I feel the current features of method resolution wasn't satisfactory to __slots__, so they implemented their own strategy.


### My proposal

CONTEXT : I'll be exposing possible alternatives, but not go into much depths about the implementations.
I'll be proposing them in the order i think they should be introduced, so each new one can benefit from previous ones.


1) Alterhitance
CONTEXT: I'm assuming this proposal to be the first to be implemented.
No other proposal has to come first.
I will still try to pay attention to the final product.
However, this proposal is independant of any other coming proposal.
As such, it should be evaluated for the values it bring on its own first, and for the value it brings in the complete update (with all my other proposal) second.

This is the dedicated feature for dependency injection / inheritance tree alteration.
This could be a dedicated module, hosting the few utils functions allowing for easy access / use of the feature.

This one is fairly straightforward, the key idea is that i don't wanna rely on super or MRO, not so much at least.
It is possible to simply set the value of __bases__ of any class, so that would be my way to go.

In the same example as before :
```
class Glider:
    def push(self)
        print("I can't move so good on the ground")

    def jump(self):
        print("I'm free! I can fly now!")

class Wheel:
    def push(self)
        print("let's roll !")

    def jump(self):
        print("oh damn, i'm falling fast!")

class WheelGlider(Wheel, Glider):
    def push(self):
        super().push()
        super(Wheel, self).push()

    def jump(self):
        super(Wheel, self).jump()
        super().jump()
```

The way to inject the mocked class in would be:
```
from alterhitance import Alter

class MockedWheel(Wheel):
    def push(self):
        print("mocked wheel push")
    def jump(self):
        print("mocked wheel jump")

WithMockedWheel = Alter(WheelGlider).replace(parent=Wheel, new_parent=MockedWheel)

class MockedGlider(Glider):
    def push(self):
        print("mocked glider push")
    def jump(self):
        print("mocked glider jump")

WithMockedWheelAndGlider = Alter(WithMockedWheel).replace(parent=Glider, new_parent=MockedGlider)

class MockedWheelGlider(WithMockedWheelAndGlider):
d    def push(self):
        print("mocked WG push")
        super().push()
    def jump(self):
        print("mocked WG jump")
        super().jump()
```

This highlight the ability of this feature to produce each new class with a Mocked parent with relative ease.
Note that contrary to what we have to do now, MockedWheelGlider only needs to inherit from one class.

The way i've illustrated it here showcases that each class can be injected at once, without having to one shot everything.
If you were to create the mock of WheelGlider first, and wanted to mock one of it's parent down the inheritance tree, it could be doable like that:

```
from alterhitance import Alter

class MockedWheel(Wheel):
    def push(self):
        print("mocked wheel push")
    def jump(self):
        print("mocked wheel jump")

class MockedGlider(Glider):
    def push(self):
        print("mocked glider push")
    def jump(self):
        print("mocked glider jump")

class MockedWheelGlider(WheelGlider):
d    def push(self):
        print("mocked WG push")
        super().push()
    def jump(self):
        print("mocked WG jump")
        super().jump()

WithMockedWheel = Alter(MockedWheelGlider).replace(child=WheelGlider, parent=Wheel, new_parent=MockedWheel)
WithMockedWheelAndGlider = Alter(WithMockedWheel).replace(child=WheelGlider, parent=Glider, new_parent=MockedGlider)
```

Note that in this example, we not only define each mock in accordance *only* to what class they are mocking, but we still have a very simple interface for the bottom class MockedWheelGlider. It too only needs to inherit from WheelGlider.

Finally, having to call the replace method twice feels a bit redundant, maybe a syntax such as:
```
FullyMockedWheelGlider = Alter(MockedWheelGlider).replace(child=WheelGlider, remap={Wheel: MockedWheel, Glider: MockedGlider})
```
would be a nicer API.

What's to know :
Alter class from the alterhitance module take a class at initialisation.
all later operation it will run will happen on this class inheritance tree.

Assuming we're in the Alter(Example) instance:
the replace method takes a few arguments :
 - child, which is the class in the inheritance tree of Example (all occurence of this class, not only the first one, might need more argument to select one in particular if it is present multiple times today)
 - parent, which is supposed to be present in the __bases__ of child
 - new_parent, which is gonna take the place of parent in __bases__ of child (same index)
 - remap, which is essentially a dict of parent : new_parent.

I'm not sure if the argument child is needed, as finding out the child class in the inheritance tree is essentially the same problem as finding the parent class in the inheritance tree.
However, it could be a way to lock the remap only to parent in the __bases__ of the correct child class. This argument should probably be optional tho.


Alter could provide more methods, such as prune, and add_branch
We could also want to be able to select only a branch from the inheritance tree, which would help inspection of the class.
That could turn out usefull for dynamically generated classes, for example, classes altered by Alter itself.



Pros of this solution:
 - It makes it easier to mock classes individually as seen in the exemple. In general, it make dependency injection step by step possible.
 - The API as presented here allows to name each responsibility (Alter, replace, prune, add_branch) , which today's solution do not provide. This makes this feature much more accessible than today's very roundabout ways.
 - No knowledge of MRO or super is required.
 - it relies on __bases__, which is a little bit more straightforward (this is essentially the value that defines a class parents), and would make this feature more resilient to changes on MRO and super (no matter how MRO resolves anything, alterhitance updates the __bases__, so MRO will find the replacment at the same time it found the original).
 - does most definitely *not* need to change anything with current MRO + super to work.

Open questions:
 - I don't know exactly if we need to keep track of the remapping in inheritance trees that have been reworked. super's argument being classes, that we might be remapping or not, should super be changed to account for the new target? I think it works fine now, but in the long term goal of switching to a feature that would take the target of proxying as argument, that would turn out to be needed.
 - I'm not fixed on any method names, or the overall structure, with the Alter class, alterhitance module, and so on.
 - I'm not fixed either on methods signatures either
 - I'm not exactly sure how to cover remap of classes that appear multiple times in the inheritance tree. I'd want a way to target a specific appearance alone, this would allow to "undiamond" diamond cases. I also don't know how much this is needed or not.


2) Postponed / Delayed inheritance OR deep inheritance definition.
I'm not fixed on the name yet.

CONTEXT: I'm assuming this proposal comes in second.
I'm assuming the altheritance proposal was accepted, and implemented first.
I will still try to pay attention to the final product.
However, this proposal is independant of any other coming proposal.
As such, it should be evaluated for the values it bring on its own first, and for the value it brings in the complete update (with all my other proposal) second.

The example "Too many combinatory":
```
class View:
    def render(self):
        # do smthg
class ListView(View):
    def render(self):
        # do smthg
class DetailView(View):
    def render(self):
        # do smthg
...

class Permission:
    def render(self):
        # do smthg
        super().render()
        # do smthg
class LoginRequired:
    def render(self):
        # do smthg
        super().render()
        # do smthg
```

Showcases a usecase where we really want inheritance, but in practice, can't be reasonably expected.
The two reasons being:
 - there's way too many combinations
 - it's not really possible to reuse a child for another parent.

I propose that such scenarios would be able to define the inheritance links between the View classes and the mixins after their definition, when themselves inhreited from:

```
class MyView(
    LoginRequired(
        Permission(
            View
        )
    )
):
    pass
```

would be a valid syntax.

Essentially, the idea is that, at definition, the syntax ```Son(Dad)``` means Son inherits from Dad.
So, in the example above, it would mean :
MyView inherits from LoginRequired, which inherits from Permission, which inherits from View.


On its own, this syntax doesn't account well for cases where a mixin would be inheriting from multiple parents.
So it might be beneficial to add a Placeholder class like that :

```
class Permission(placeholder as view, placeholder as template):
    ...


class MyView(
    Permission(
        view = View,
        template = Template
    )
):
```

Thinking about the long term full proposal, having a way to tell which class replaces which without relying on the order of their declaration is relevant, as the proxy feature will likely have to account for remapping.


This feature could probably (partially at least) be provided by the alterhitance module.
```
Inherited = Alter(Permission).add_branch(View)
Inherited = Alter(LoginRequired).add_branch(Inherited)

class MyView(Inherited):
    ...
```

But this is not as nice an API as this proposal.

Pros:
 - it essentially extends the capacity of class definition.
 - it makes it very obvious which class specializes which, and produces the inheritances tree accordingly
 - it is consistent with the inheritance syntax we all know.
 - it isolates the feature from super + MRO more than today's solution, as the ability of super to target sideway, on the cases where we couldn't produce normal inheritance, is now covered
 - it replaces a multiple inheritance scenario with simple inheritance.



3) The Diamond problem

4) Proxy

5) Method resolution
