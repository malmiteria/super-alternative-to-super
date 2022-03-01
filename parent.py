

class Parenting:
    def parent(self, parent_cls):
        return parent(self, self.__class__, parent_cls)

def parent(instance, child_cls, parent_cls):
    ancestors = build_parenting_order(child_cls)
    if parent_cls not in ancestors:
        raise TypeError(f"{parent_cls} is not an ancestor of {child_cls}. Available options are {ancestors[1:]}")
    ancestor_index = ancestors.index(parent_cls)
    return super(ancestors[ancestor_index - 1], instance)

def build_parenting_order(cls, res=None):
    if res is None:
        res = [cls]
    unvisited_bases = [el for el in cls.__bases__ if el not in res and el is not object and el is not Parenting]
    for b in unvisited_bases:
        res.append(b)
        build_parenting_order(b, res)
    return res
