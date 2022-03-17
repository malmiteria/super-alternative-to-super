import inspect

class ExplicitenessRequired(Exception):
    pass

class ConcurentMethodResolutionError(Exception):
    pass


def get_source_line_range(code_element):
    lines = inspect.getsourcelines(code_element)
    return range(lines[1], lines[1] + len(lines[0]))

def function_caller_frame(function):
    for frame_info in inspect.stack():
        if frame_info.function == function.__name__:
            return frame_info.frame.f_back


class AsParent:
    def __caller_class(self):
        caller_frame = function_caller_frame(self.__as_parent__)
        caller_lnum = caller_frame.f_lineno
        for cls in self.__class__.__mro__:
            if caller_lnum not in get_source_line_range(cls):
                continue
            return cls
 
    def __as_parent__(self, parent_cls=None):
        caller_cls = self.__caller_class()
        if caller_cls == parent_cls:
            raise TypeError(f"{parent_cls} is not a parent of itself")
        if parent_cls is None:
            if len(caller_cls.__bases__) != 1:
                raise ExplicitenessRequired
            parent_cls = caller_cls.__bases__[0]
        if parent_cls not in caller_cls.__mro__:
            raise TypeError(f"{parent_cls} is not an ancestor of {caller_cls}. Available options are {caller_cls.__mro__}")
        current_mro = self.__class__.__mro__
        ancestor_index = current_mro.index(parent_cls)
        return super(current_mro[ancestor_index - 1], self)

class ExplicitMethodResolution:
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

class Parenting(ExplicitMethodResolution, AsParent):
    pass
