import inspect

class ConcurentMethodResolutionError(Exception):
    pass


def get_source_line_range(code_element):
    lines = inspect.getsourcelines(code_element)
    return range(lines[1], lines[1] + len(lines[0]))


class Parenting:
    def __mro_without_object_and_parenting(self):
        for cls in self.__class__.__mro__:
            if cls in [object, __class__]:
                continue
            yield cls

    def __caller_class(self):
        caller_frame = inspect.stack()[2].frame # 2 because the previous context is the __as_parent__ method, and the caller is __as_parent__ calling context, so we need two frames level 
        caller_lnum = caller_frame.f_lineno
        for cls in self.__mro_without_object_and_parenting():
            if caller_lnum not in get_source_line_range(cls):
                continue
            return cls
 
    def __as_parent__(self, parent_cls):
        caller_cls = self.__caller_class()
        if caller_cls == parent_cls:
            raise TypeError(f"{parent_cls} is not a parent of itself")
        if parent_cls not in caller_cls.__mro__:
            raise TypeError(f"{parent_cls} is not an ancestor of {caller_cls}. Available options are {caller_cls.__mro__}")
        current_mro = self.__class__.__mro__
        ancestor_index = current_mro.index(parent_cls)
        return super(current_mro[ancestor_index - 1], self)

    def __getattribute__(self, name):
        if name in ["recur_getattr", "__class__", "__dict__"]:
            return super().__getattribute__(name)
        if name in self.__dict__:
            return super().__getattribute__(name)
        if name in self.__class__.__dict__:
            return super().__getattribute__(name)
        return list(self.recur_getattr(self.__class__, name).values())[0]

    def recur_getattr(self, cls, name):
        res = {}
        for parent in cls.__bases__:
            if name in parent.__dict__:
                res[parent] = super().__getattribute__(name)
                continue
            try:
                res.update(self.recur_getattr(parent, name))
            except AttributeError:
                pass
        if len(res) >= 2:
            raise ConcurentMethodResolutionError
        if len(res) == 0:
            raise AttributeError
        return res

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

