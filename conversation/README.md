

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

feature 2 (of super + MRO): sideway specialization
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


I want everyone to take some time to realise that today's sideway specialization relies on the method resolution algorithm. Those feature should have nothing in common. One if for attribute lookup, one is essentially a glorified decorator
Same can be said about dependency injection / inheritance tree alteration.


Also, as mentionned, i'd argue that some of those feature aren't fully delivering what they promise.
Essentially, they compromise for the extra feature, which in the context of a lack of properly isolated implementation for those feature seems fair.


=====


What motivated me first here was the few problems with the feature 1 (proxying the parent) and feature 4 (method resolution) which I consider to be suboptimal.
Of course, the different use cases made out of the current super + MRO should be preserved.
Essentially, I do *not* intend to lose any strength / any use case of the langage
Listing all the use cases made out of current super + MRO matters then. And I think i already cover the most important ones with the 4 features i described.
If you feel I'm missing something, please let me know.

My goal :
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


===
From now, I'll try to tackle down each feature individually.
