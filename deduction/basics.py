MY_VERSION = 0.0


class Var:
    def __init__(self, variable_indicator):
        self.idx = variable_indicator

    def __repr__(self):
        return "Var(%s)" % (self.idx,)

    def bound(self, binding):
        return self.idx in binding

    def deref(self, binding):
        return binding[self.idx]

    def __lt__(self, other):
        assert isinstance(other, Var)
        return self.idx < other.idx

    def unify(self, other, bindings):
        if isinstance(other, Var):
            if self < other:
                return union_dict({self.idx: other}, bindings)
            elif self == other:
                return bindings
            else:
                return union_dict({other.idx: self}, bindings)
        else:
            return union_dict({self.idx: other}, bindings)


class MVar:
    def __init__(self, variable_indicator):
        self.idx = variable_indicator

    def session_var(self, session):
        return Var((session, self.idx))


def sessions_instance(_):
    pass


def term_is_empty(t):
    return t == ()

def unify(first_term, second_term, bindings):
    l1 = [first_term]
    l2 = [second_term]
    while len(l1) > 0 and len(l2) > 0:
        t1 = l1.pop()
        t2 = l2.pop()
        if term_is_empty(t1) and term_is_empty(t2):
            continue
        if isinstance(t1, Var):
            if t1.bound(bindings):
                l1.append(t1.deref(bindings))
                l2.append(t2)
            elif isinstance(t2, Var):
                if t2.bound(bindings):
                    l1.append(t1)
                    l2.append(t2.deref(bindings))
                else:
                    bindings = t1.unify(t2, bindings)
            else:
                bindings = t1.unify(t2, bindings)
        elif isinstance(t2, Var):
            if t2.bound(bindings):
                l1.append(t1)
                l2.append(t2.deref(bindings))
            else:
                bindings = t2.unify(t1, bindings)
        elif isinstance(t1, tuple):
            if isinstance(t2, tuple):
                if len(t1) == len(t2):
                    t1_l = list(t1)
                    t1_l.reverse()
                    l1 = l1 + t1_l
                    t2_l = list(t2)
                    t2_l.reverse()
                    l2 = l2 + t2_l
                else:
                    raise UnificationFailure(t1, t2, bindings)
        elif t1 == t2:
            continue
        else:
            raise UnificationFailure(t1, t2, bindings)
    if len(l1) != 0 or len(l2) != 0:
        raise UnificationFailure()
    return bindings


class UnificationFailure(Exception):
    def __init__(self, term1, term2, bindings):
        self.term1 = term1
        self.term2 = term2
        self.bindings = bindings

    def __repr__(self):
        return "%s(%s, %s, %s)" % ("UnificationFailure", self.term1, self.term2, self.bindings)


def union_dict(dict1, dict2):
    ret_value = {k: v for k, v in dict1.items()}
    for k, v in dict2.items():
        ret_value[k] = v
    return ret_value




