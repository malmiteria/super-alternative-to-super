
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
            else:
                try:
                    res.append(self.recur_getattr(parent, name))
                except AttributeError:
                    pass
        if len(res) >= 2:
            raise ConcurentMethodResolutionError
        if len(res) == 0:
            raise AttributeError
        return res[0]
