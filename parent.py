
class ConcurentMethodResolutionError(Exception):
    pass

class Parenting:
    @classmethod
    def __as_parent__(cls, parent_cls, instance):
        # raise error when instance.__class__ != cls?
        if parent_cls not in cls.__bases__:
            raise TypeError(f"{parent_cls} is not a parent of {cls}. Available options are {cls.__bases__}")
        ancestor_index = instance.__class__.__mro__.index(parent_cls)
        return super(instance.__class__.__mro__[ancestor_index - 1], instance)

    def __getattribute__(self, name):
        if name in ["recur_getattr", "__class__", "__dict__"]:
            return super().__getattribute__(name)
        if name in self.__dict__:
            return super().__getattribute__(name)
        if name in self.__class__.__dict__:
            return super().__getattribute__(name)
        return self.recur_getattr(self.__class__, name)

    def recur_getattr(self, cls, name):
        res = []
        for parent in cls.__bases__:
            if name in parent.__dict__:
                res.append(super().__getattribute__(name))
                continue
            try:
                res.append(self.recur_getattr(parent, name))
            except AttributeError:
                pass
        if len(res) >= 2:
            raise ConcurentMethodResolutionError
        if len(res) == 0:
            raise AttributeError
        return res[0]

# TODO:
# adding a __as_class__ which points to the context of the current element.
# in a method from parent P, __as_class__ is P.
# as soon as we're in the call of that method, __as_class__ is P
# as soon as we're out that method, __as_class__ is back to __class__
# in other term, we need to decorate all methods with that __as_class__ change
# do we do that in the __getattribute__?
# this decoration should or should not ???? apply to method accessed through super
# NB: shouldn't apply to dunder methods, only to method defined

# for all __setattribute__ when __as_class__ != __class__,
# set the attribute name to set_by_class_<__as_class__>_<name>
# when getting the attr name, use the same contextualised name, if uncontextualised name can't be found
# if no contextualised_name is found, try resolving in parents, if possible implicit resolution, do it
# if not, raise an explicit resolution required error
# (case where B.method sets name, but A.other_method access it, with A inherits B)

# This lookup can only take a look at __dict__ as it is set with all values, no need for recursions (except when trying to resolve the name)

