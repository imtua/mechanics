import math
from collections import OrderedDict

denominator_limit = 100


def get_fraction(value):
    differences = [1]
    for i in range(1, denominator_limit + 1):
        top = value * i
        differences.append(abs(top - round(top)))
    bottom = differences.index(min(differences))
    return round(value * bottom), bottom


def format_number(value):
    if not Expression.latex_mode:
        return str(value)

    n, d = get_fraction(value)
    if d == 1:
        return str(n)
    if n < 0:
        return "-\\frac{" + str(-n) + "}{" + str(d) + "}"
    else:
        return "\\frac{" + str(n) + "}{" + str(d) + "}"


def format_variable(name):
    if not Expression.latex_mode:
        return name

    subscript = ""
    if "_" in name:
        subscript = name[name.index("_"):]
        name = name[:name.index("_")]
    else:
        counter = 0
        while counter < len(name):
            if name[counter].isdigit():
                break
            counter += 1
        if counter < len(name):
            subscript = "_" + name[counter:]
            name = name[:counter]
    if len(name) > 1:
        name = "\\" + name
    return name + subscript


def cartesian_product(*iterables):
    pools = [tuple(pool) for pool in iterables]
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]

    for prod in result:
        yield prod


class Expression:
    context = []
    latex_mode = False

    def __str__(self):
        pass

    def key(self):
        pass

    def contains(self, name):
        return False

    def substitute(self, values):
        pass

    def evaluate(self, values):
        pass

    def deriv(self, respect):
        pass

    def differentiate(self, respect):
        return self.deriv(respect).substitute({})

    def __add__(self, other):
        if isinstance(other, Expression):
            return Sum([self, other])
        elif isinstance(other, (int, float)):
            return Sum([self, Literal(other)])
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Expression):
            return Sum([self, -other])
        elif isinstance(other, (int, float)):
            return Sum([self, Literal(-other)])
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Expression):
            return Term(1, [self, other])
        elif isinstance(other, (int, float)):
            return Term(other, [self])
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Term(other, [self])
        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, (int, float)):
            return Power(self, Literal(other))
        return NotImplemented

    def __neg__(self):
        return Term(-1, [self])


class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return format_number(self.value)

    def key(self):
        return ("literal", self.value)

    def contains(self, name):
        return False

    def substitute(self, values):
        return self

    def evaluate(self, values):
        return self.value

    def deriv(self, respect):
        return Literal(0)


class Constant(Expression):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        if Expression.latex_mode:
            return f"\\{self.name}"
        else:
            return self.name

    def key(self):
        return ("constant", self.name)

    def contains(self, name):
        return False

    def evaluate(self, values):
        return self.value

    def deriv(self, respect):
        return Literal(0)


Pi = Constant("pi", math.pi)


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        if Expression.latex_mode:
            if self.name.endswith("dotdot"):
                return f"\\ddot{{{format_variable(self.name[:-6])}}}"
            elif self.name.endswith("dot"):
                return f"\\dot{{{format_variable(self.name[:-3])}}}"
            return format_variable(self.name)

    def key(self):
        return ("variable", self.name)

    def contains(self, name):
        if name == self.name:
            return True
        elif name == "t" and self.name.replace("dot", "") in Expression.context:
            return True
        return False

    def evaluate(self, values):
        return values[self.name]

    def deriv(self, respect):
        if self.name == respect:
            return Literal(1)
        elif respect == "t":
            return Variable(self.name + "dot")
        return Literal(0)


Var = Variable


class Power(Expression):
    def __init__(self, base, exponent):
        self.base = base
        self.exponent = exponent
