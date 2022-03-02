

class Parenting:
    def parent(self, parent_cls):
        return parent(self, self.__class__, parent_cls)

def parent(instance, child_cls, parent_cls):
    if parent_cls not in child_cls.__mro__:
        raise TypeError(f"{parent_cls} is not an ancestor of {child_cls}. Available options are {child_cls.__mro__[1:]}")
    ancestor_index = child_cls.__mro__.index(parent_cls)
    return super(child_cls.__mro__[ancestor_index - 1], instance)
