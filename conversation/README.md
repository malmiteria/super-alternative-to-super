
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

feature 3 (of super + MRO): dependency injection / inheritance tree alteration
If you wanna inject a class wherever in some pre existing class inheritance tree, you can through the use of some clever new classes.
If you wanna deny its parent to one class, and essentially prune of branch off the inheritance tree, you can too.

feature 4 (of MRO alone): method resolution
when trying to resolve a method / attribute of a class, if not present in its definition, looks up the parent(s) to come up with an answer.
If no parent can resolve it, you get the attribute error, if at least one does, you get it.
I'd argue that it makes it possible to silently ignore a parent method when multiple parent define such a method. Which makes it especially painfull to debug those scenarios, which makes it an incomplete feature.
On top of that, it renders some class definition invalid, when really, the method resolution shouldn't break more than the method resolution. This should be a gettribute error, not a class definition error.


Also, as mentionned, i'd argue that some of those feature aren't fully delivering what they promise.
Essentially, they compromise for the extra feature, which in the context of a lack of properly isolated implementation for those feature seems fair.


=====


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

### Today
CONTEXT : I'm talking here *exclusively* about the parent proxying feature.
I will talk about the other features I mentionned later on.
I'm describing the current state of this feature, to the best of my understanding.


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

The 'syntactic sugar' aspect of super's proxying feature is that calls to parent methods through super don't require to pass the instance as first argument, which makes for less redundant code.

There is a 'disconnect' between the argument passed to super (when needed) and the class it will target to be a proxy of.
super(Son) is not a proxy of class Son, it is a proxy on the next in MRO (it feels redundant saying MRO order, but weird just saying in MRO ...) So in cases where the automatic solve of the argumentless super doesn't suits our needs, such as in the exemples above, there is some mental gymnastic, and knowledge to be known to reach our goal.

### My proposal
CONTEXT : I propose an alternative to this proxying feature
This is not a final product, and your inputs are welcomed.
It is an alternative *exclusively* to the proxying feature.

I think the replacement to the proxying feature should:
 - Accept for argument the class it wants to be a proxy of (and eventually, self, too).
 - Allow for argumentless syntax in case of simple inheritance. (Since in this scenario, the only parent present is the only possible target)
 - Require argument in case of multiple inheritance
 - Account for possible remapping of a parent. In this case the targeted class would be the remap of the class passed as an argument.
 - Be allowed to target any class higher in the inheritance tree, not only direct parents.


For the sake of illustration, let's call this replacment ```__as_parent__``` but at the end of the day, the name 'super' is fine, it will just make it easier to understand what code is an example of my alternative, and what code is a description of today's state.
and let's assume it can take two optional arguments, first a class, second an instance.


This is a showcase of a simple case:
```
class Dad:
    age = 100
    def say_hi(self):
        print("back in my days...")

class Son(Dad):
    age = __as_parent__(Dad).age - 30 # Dad is already defined here, so no problem
    def say_hi(self):
        print("i'm not that old... yet...")
        __as_parent__().say_hi()
```

as you can see, __as_parent__ works basically the same as super here (in term of proxying only), except maybe for this little bonus ability to be used for class attribute (not that it's a common need). 

Let's look at how the different examples I described earlier would change with this new version:

#### Diamond tree, with a top non repeated
CONTEXT : This is a showcase of the proxying feature such as i intend it.
I'm under the assumption there is an alternative to all other features.

```
class HighGobelin:
    def scream(self):
        print("raAaaaAar")

class CorruptedGobelin(HighGobelin):
    def scream(self):
        print("my corrupted soul makes me wanna scream")
        __as_parent__().scream()

class ProudGobelin(HighGobelin):
    def scream(self):
        print("I ... can't ... contain my scream!")
        __as_parent__().scream()

class HalfBreed(ProudGobelin, CorrupteGobelin):
    def scream(self):
        # 50% chance to call ProudGobelin scream, 50% chance to call CorruptedGobelin scream
        if random.choices([True, False]):
            __as_parent__(ProudGobelin, self).scream()
        else:
            __as_parent__(CorrupteGobelin, self).scream()
```

This allows what we couldn't do with the old style super, in a pretty simple way.


Of course now, if you'd want a diamond case scenario which would call the grandparent method only once... You can't.

Oh and, there's no way to use the class.method syntax to get around this problem here.

No matter what strategy you choose, either call every time, or call only once, you'll end up making the other scenario impossible.

Except of course if we were to introduce a new feature that would allow developpers to choose that strategy.

We can think of a few things, but I don't have a solution for that yet. This is starting to be a big post, so i'll dive into that one at a later time.
Quickly tho :
 An enum could list all poossible behavior, we might want more than the 'call me on my last appearance' and 'call me every time' behaviors.
 It would be relevant to the overall attempt at unlinking the 4 features here, and super and MRO in more general term, to make this feature non reliant on super or MRO. Inspecting the inheritance tree first to spot the calls we wanna mute before actually running the call can be an option, the remap feature could be used to remap those call to a Mute object, either through today's use of dependency injection or my alternative __as_parent__ accounting for a remap.




#### Can't assume on parent's more specialised.
CONTEXT : This is a showcase of the proxying feature such as i intend it.
I'm under the assumption there is an alternative to all other features.

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
        __as_parent__(Wheel, self).push()
        __as_parent__(Glider, self).push()

    def jump(self):
        # calls Glider push method first
        # calls Wheel push method second
        __as_parent__(Glider, self).jump()
        __as_parent__(Wheel, self).jump()
```

As you can see, this is trivial.

#### Too big combinatory


